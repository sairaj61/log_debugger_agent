from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import PromptTemplate

from src.llm import get_llm

prompt_template = PromptTemplate(
    input_variables=["jira_id", "heading", "description", "comments", "date", "components", "logs"],
    template=
    """
                Given the following JIRA ticket and logs, determine if there is a valid technical reason in the logs that justifies the creation of the JIRA ticket.
                
                JIRA Ticket:
                ID: {jira_id}
                Heading: {heading}
                Description: {description}
                Comments: {comments}
                Date: {date}
                Components: {components}
                
                Logs:
                {logs}
                
                Based on the logs, is this JIRA ticket justified? Provide a clear YES/NO and reasoning.
                """
)

chain = prompt_template | get_llm() | StrOutputParser()


def analyze_log_line(line: str, context: dict) -> str | None:
    result = chain.invoke({
        "jira_id": context.get("id", ""),
        "heading": context.get("heading", ""),
        "description": context.get("description", ""),
        "comments": ", ".join(context.get("comments", [])),
        "date": context.get("date", ""),
        "components": ", ".join(context.get("components", [])),
        "logs": line
    }).strip()

    if result.lower() == "no match":
        return None
    return f"Match: {line.strip()} | Reason: {result}"
