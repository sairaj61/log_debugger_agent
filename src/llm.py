import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def get_llm():
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    print("Environment variables set for OpenAI.")
    return ChatOpenAI(model="gpt-4o", temperature=0)
