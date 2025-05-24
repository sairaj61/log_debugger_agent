# analysis_engine.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt_template = ChatPromptTemplate.from_template(
    """Given the Jira context:
Heading: {heading}
Description: {description}
Comments: {comments}
Components: {components}

Evaluate the following log line:
"{line}"

Does this log line relate to the Jira context? If yes, return a short reason; otherwise return "No match".
"""
)
chain = prompt_template | llm | StrOutputParser()

def analyze_log_line(line: str, context: dict) -> str | None:
    result = chain.invoke({
        "heading": context.get("heading", ""),
        "description": context.get("description", ""),
        "comments": ", ".join(context.get("comments", [])),
        "components": ", ".join(context.get("components", [])),
        "line": line
    }).strip()

    if result.lower() == "no match":
        return None
    return f"Match: {line.strip()} | Reason: {result}"
