import os
import time

from fastapi import FastAPI
from pydantic import BaseModel

from src.analysis_engine import analyze_log_line
from src.jira_data import parse_jira_request
from src.log_stream_listener import LogStreamListener

app = FastAPI()
LOG_PATH = "logs/app.log"
OUTPUT_DIR = "output"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


class JiraRequest(BaseModel):
    jira_id: str
    heading: str = ""
    description: str = ""
    comments: list = []
    date: str = ""
    components: list = []


@app.post("/analyze")
def analyze_jira(jira: JiraRequest):
    jira_context = parse_jira_request(jira.dict())
    report_lines = []

    def handle_line(line):
        result = analyze_log_line(line, jira_context)
        if result:
            print(f"LOG MATCH: {result}")
            report_lines.append(result)

    listener = LogStreamListener(LOG_PATH, handle_line)
    listener.read_old_logs()
    listener.start_streaming()

    # Let stream run for 10 seconds, then stop (for simplicity)
    time.sleep(10)
    listener.stop()

    report_file = os.path.join(OUTPUT_DIR, f"{jira_context['id']}.txt")
    with open(report_file, 'w') as f:
        f.write("\n".join(report_lines))

    return {"status": "completed", "output_file": report_file, "matches": report_lines}
