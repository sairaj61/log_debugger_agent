import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# os.environ['LANGCHAIN_TRACING_V2'] = 'true'
# os.environ['LANGCHAIN_ENDPOINT'] = os.getenv('LANGCHAIN_ENDPOINT', 'https://api.langchain.com')
print("Environment variables set for OpenAI and LangChain.")

llm = ChatOpenAI(model="gpt-4o", temperature=0)
log_debugger_prompt = ChatPromptTemplate.from_template(
    """You are a log debugger agent. Your task is to analyze the following log line in the context of the provided system information.

System Context:
- Application: {application}
- Environment: {environment}
- Recent Changes: {recent_changes}
- Known Issues: {known_issues}

Log Line:
"{log_line}"

Instructions:
1. Determine if the log line indicates an error, warning, or abnormal behavior.
2. If yes, explain the possible root cause based on the context.
3. Suggest actionable next steps for debugging or resolving the issue.
4. If the log line is normal, respond with "No issue detected".

Respond concisely and clearly.
"""
)
chain = log_debugger_prompt | llm
result = chain.invoke({
    "application": "MyApp",
    "environment": "production",
    "recent_changes": "Updated logging module",
    "known_issues": "Intermittent timeout errors",
    "log_line": "ERROR: Connection timed out after 10 seconds"
})
print(result)
