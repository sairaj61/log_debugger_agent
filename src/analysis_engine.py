def analyze_log_line(line, context):
    keywords = ["NullPointerException", "NumberFormatException", "ERROR"]
    for kw in keywords:
        if kw in line:
            return f"Detected {kw} at line: {line}"
    return None
