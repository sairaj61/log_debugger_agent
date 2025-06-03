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
  "jira_id": "LE-3311",
  "heading": "Switch event submission fails intermittently",
  "description": "Network system fails to submit or retry switch events. Users also report missing event IDs.",
  "comments": ["Observed failures on SW-221", "User U-8821 reported missing event"],
  "date": "2025-06-03",
  "components": ["NetworkService", "SwitchManager", "EventListener"]
}'
```

### Example Response

```json
{
    "status": "completed",
    "matches": [
        "Match: 2025-06-03 09:45:01 INFO SwitchManager - Switch SW-221 initialized successfully\n2025-06-03 09:45:02 ERROR NetworkService - Failed to submit switch event for SW-221\n2025-06-03 09:45:03 WARNING EventListener - Event not reported for user ID U-8821\n2025-06-03 09:45:04 DEBUG MetricsLogger - Ping time to switch SW-221: 8ms\n2025-06-03 09:45:05 ERROR NetworkService - Retry failed for switch event SW-221\n2025-06-03 09:45:06 INFO CleanupService - Old event logs purged | Reason: YES, the JIRA ticket is justified. The logs provide clear evidence of the issues described in the ticket. Specifically:\n\n1. The log entry at `2025-06-03 09:45:02` shows an error in the `NetworkService` where it failed to submit a switch event for SW-221, which aligns with the ticket's description of submission failures.\n\n2. The log entry at `2025-06-03 09:45:03` indicates a warning from the `EventListener` that an event was not reported for user ID U-8821, which corresponds to the user-reported issue of missing event IDs mentioned in the ticket.\n\n3. The log entry at `2025-06-03 09:45:05` shows another error where a retry attempt to submit the switch event for SW-221 also failed, supporting the ticket's claim of failed retries.\n\nThese log entries collectively provide a valid technical basis for the issues reported in the JIRA ticket, justifying its creation.",
        "Match: 2025-06-03 09:45:07 INFO AuthService - Auth token refreshed for user U-8821\n2025-06-03 09:45:08 DEBUG EventProcessor - Processing event for switch SW-009\n2025-06-03 09:45:09 INFO EventProcessor - Event for switch SW-009 successfully submitted\n2025-06-03 09:45:10 ERROR NetworkService - Unexpected disconnect from switch SW-221 | Reason: YES, the JIRA ticket is justified. The logs show an \"ERROR\" entry from the NetworkService indicating an \"Unexpected disconnect from switch SW-221.\" This error aligns with the issue described in the JIRA ticket, where there are failures in submitting or retrying switch events. The specific mention of switch SW-221 in both the ticket and the logs suggests a correlation between the reported problem and the observed error, providing a valid technical reason for the creation of the ticket. Additionally, the user U-8821, who reported missing event IDs, is mentioned in the logs, further supporting the relevance of the ticket."
    ],
    "llm_final_reasoning": {
        "query": "Given the following JIRA context: {'id': 'LE-3311', 'heading': 'Switch event submission fails intermittently', 'description': 'Network system fails to submit or retry switch events. Users also report missing event IDs.', 'comments': ['Observed failures on SW-221', 'User U-8821 reported missing event'], 'date': '2025-06-03', 'components': ['NetworkService', 'SwitchManager', 'EventListener']}. Do the logs support this ticket? Explain.",
        "result": "Yes, the logs support the JIRA ticket LE-3311. The logs indicate several issues related to switch event submissions and user reports:\n\n1. There are multiple errors related to switch SW-221, including a failure to submit a switch event and a retry failure (2025-06-03 09:45:02 and 2025-06-03 09:45:05).\n2. There is a warning about an event not being reported for user ID U-8821 (2025-06-03 09:45:03), which aligns with the user report of missing event IDs mentioned in the JIRA ticket.\n3. An unexpected disconnect from switch SW-221 is logged (2025-06-03 09:45:10), which could contribute to the intermittent failures described in the ticket.\n\nThese log entries correspond to the issues described in the JIRA ticket, including the components involved (NetworkService, SwitchManager, and EventListener)."
    }
}


```
## File Structure
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
