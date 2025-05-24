def parse_jira_request(data):
    return {
        "id": data["jira_id"],
        "heading": data.get("heading", ""),
        "description": data.get("description", ""),
        "comments": data.get("comments", []),
        "date": data.get("date", ""),
        "components": data.get("components", [])
    }
