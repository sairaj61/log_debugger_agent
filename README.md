# Log Debugger Agent

A lightweight FastAPI-based tool to automatically analyze application logs and match them against specific Jira tickets using OpenAI's language model.

## 🔍 Features

* Real-time and historical log stream analysis.
* Matches Jira ticket context with relevant log lines using GPT (via OpenAI API).
* Outputs a report file containing matched log lines with reasoning.
* Modular architecture for easy extension.

## 📆 Requirements

* Python 3.9+
* OpenAI API Key

## 🧪 Installation

```bash
git clone https://github.com/your-username/log-debugger-agent.git
cd log-debugger-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🔐 Environment Setup

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🚀 Running the App

1. **Start the FastAPI server**:

```bash
uvicorn src.main:app --reload
```

2. **Send a POST request to** `/analyze` with Jira data:

Example JSON:

```json
{
  "jira_id": "LE-123",
  "heading": "Null pointer issue",
  "description": "App crashes on null pointer access",
  "comments": ["Check null condition", "Occurs during login"],
  "date": "2025-05-24",
  "components": ["LoginModule", "NullHandler"]
}
```

## 📁 File Structure

```
.
├── src/
│   ├── analysis_engine.py     # Core log analysis logic using OpenAI
│   ├── jira_data.py           # Parses incoming Jira JSON
│   ├── log_stream_listener.py # Monitors and streams log file
│   └── main.py                # FastAPI app entrypoint
├── logs/app.log               # Sample log file
├── output/                    # Output directory for match reports
├── requirements.txt
├── generate_dummy_logs.py     # Creates sample log entries
└── README.md
```

## 📄 Output

After 10 seconds of analysis, a file is saved to `output/{jira_id}.txt` containing all matched log lines and reasons.

## ✅ Example Output

```
Match: 2025-05-24 08:00:02 ERROR NullPointerException at line 56 | Reason: This error may relate to a null pointer crash described in the Jira ticket.
```

## 🧠 Powered By

* [LangChain](https://www.langchain.com/)
* [OpenAI](https://platform.openai.com/)
* [FastAPI](https://fastapi.tiangolo.com/)

## 📌 Notes

* Uses `gpt-3.5-turbo` by default.
* Requires a valid OpenAI key with sufficient quota.
* Designed for basic log relevance detection, extendable to deeper analysis.
