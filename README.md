# Log Debugger Agent

A FastAPI-based tool to analyze application logs and match them against Jira tickets using OpenAI's GPT models.

## Features

- Real-time and historical log analysis.
- Matches Jira ticket context with relevant log lines using GPT (OpenAI API).
- Outputs a report file with matched log lines and reasoning.
- Modular and extensible architecture.

## Requirements

- Python 3.9+
- OpenAI API Key

## Installation

```bash
git clone <your-repo-url>
cd log_debugger_agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Running the App

1. Start the FastAPI server:

```bash
uvicorn src.main:app --reload
```

2. Send a POST request to `/analyze` with Jira data:

Example JSON:

```json
{
  "jira_id": "LE-1234",
  "heading": "Null pointer issue",
  "description": "App crashes on null pointer access",
  "comments": ["Check null condition", "Occurs during login"],
  "date": "2025-05-24",
  "components": ["LoginModule", "NullHandler"]
}
```

## API Usage Example

You can analyze logs against a Jira ticket using the following `curl` command:

```bash
curl --location 'http://localhost:8000/analyze' \
--header 'Content-Type: application/json' \
--data '{
    "jira_id": "LE-1234",
    "heading": "App crash on login",
    "description": "Login fails intermittently",
    "comments": [],
    "date": "2025-05-24",
    "components": ["LoginModule"]
  }'
```

### Example Response

```json
{
  "status": "completed",
  "matches": [
    "Match: 2025-05-24 08:00:01 INFO Application started\n2025-05-24 08:00:02 ERROR NullPointerException at line 56\n2025-05-24 08:00:03 ERROR NumberFormatException at line 103\n2025-05-24 08:00:05 INFO User logged in\n2025-05-24 08:00:06 ERROR NullPointerException at line 72 | Reason: YES, the JIRA ticket is justified. The logs indicate multiple errors occurring during the application's operation, specifically during the login process. The presence of `NullPointerException` and `NumberFormatException` errors suggests that there are underlying issues in the code that could lead to the app crashing or login failures. These errors align with the description in the JIRA ticket that mentions intermittent login failures, providing a valid technical reason for the ticket's creation."
  ],
  "llm_final_reasoning": {
    "query": "Given the following JIRA context: {'id': 'LE-1234', 'heading': 'App crash on login', 'description': 'Login fails intermittently', 'comments': [], 'date': '2025-05-24', 'components': ['LoginModule']}. Do the logs support this ticket? Explain.",
    "result": "Yes, the logs do support the JIRA ticket. The ticket describes an issue with the application crashing or failing during login, and the logs show that there are multiple errors occurring around the time of a user login. Specifically, there are two NullPointerExceptions and a NumberFormatException logged just before and after a user logs in at 08:00:05 on 2025-05-24. These errors could potentially cause the login process to fail intermittently, as described in the ticket."
  }
}
## File Structure

```
.
├── src/
│   ├── analysis_engine.py     # Log analysis logic using OpenAI
│   ├── jira_data.py           # Parses Jira JSON
│   ├── log_stream_listener.py # Monitors and streams log file
│   └── main.py                # FastAPI app entrypoint
├── logs/app.log               # Sample log file
├── output/                    # Output directory for reports
├── requirements.txt
├── generate_dummy_logs.py     # Creates sample log entries
└── README.md
```

## Output

After analysis, a file is saved to `output/{jira_id}.txt` containing all matched log lines and reasons.

Example output:

```
Match: 2025-05-24 08:00:02 ERROR NullPointerException at line 56 | Reason: This error may relate to a null pointer crash described in the Jira ticket.
```

## Powered By

- [LangChain](https://www.langchain.com/)
- [OpenAI](https://platform.openai.com/)
- [FastAPI](https://fastapi.tiangolo.com/)

## Notes

- Uses `gpt-3.5-turbo` by default.
- Requires a valid OpenAI key.
- Designed for basic log relevance detection, extendable for deeper analysis.
