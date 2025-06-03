import os
from fastapi import FastAPI
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from pydantic import BaseModel

from src.analysis_engine import analyze_log_line
from src.jira_data import parse_jira_request
from src.llm import get_llm

app = FastAPI()
LOG_PATH = "logs/app.log"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


class JiraRequest(BaseModel):
    jira_id: str
    heading: str = ""
    description: str = ""
    comments: list = []
    date: str = ""
    components: list = []


@app.post("/analyze")
def analyze_jira(jira: JiraRequest):
    jira_context = parse_jira_request(jira.model_dump())
    report_lines = []

    # Step 1: Load log content
    loader = TextLoader(LOG_PATH)
    documents = loader.load()

    # Step 2: Chunk logs for vector DB
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    # Step 3: Create Vector Store
    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.from_documents(docs, embeddings)

    # Step 4: LLM + Retriever
    retriever = vectordb.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=get_llm(), retriever=retriever)

    # Step 5: Ask final LLM verdict
    final_reasoning = qa_chain.invoke(
        f"Given the following JIRA context: {jira_context}. Do the logs support this ticket? Explain.")

    # Step 6: Line-by-line analysis
    for doc in docs:
        result = analyze_log_line(doc.page_content, jira_context)
        if result:
            report_lines.append(result)

    return {
        "status": "completed",
        "matches": report_lines,
        "llm_final_reasoning": final_reasoning
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
