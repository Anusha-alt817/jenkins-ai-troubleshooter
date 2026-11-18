
import os
import requests
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"

LOG_DIR = os.getenv("LOG_DIR", "logs")
REPORT_DIR = "reports"
BUILD_NUMBER = os.getenv("BUILD_NUMBER")


def analyze_logs():

    if not BUILD_NUMBER:
        raise ValueError("BUILD_NUMBER environment variable is missing")

    log_file = os.path.join(
        LOG_DIR,
        f"jenkins-build-{BUILD_NUMBER}.log"
    )

    if not os.path.exists(log_file):
        raise FileNotFoundError(f"Log file not found: {log_file}")

    with open(log_file, "r", encoding="utf-8") as file:
        logs = file.readlines()

    keywords = [
        "[ERROR]",
        "[WARNING]",
        "FAILURE",
        "Exception",
        "BUILD FAILURE"
    ]

    important_logs = [
        line.strip()
        for line in logs
        if any(keyword.lower() in line.lower() for keyword in keywords)
    ]

    if not important_logs:
        print("No errors or warnings found. AI analysis skipped.")
        return

    log_text = "\n".join(important_logs[-50:])

    prompt = f"""
You are a DevOps troubleshooting assistant.

Analyze these Jenkins pipeline log messages.

Provide:
1. Error summary
2. Evidence from the logs
3. Likely root cause
4. Recommended troubleshooting steps

Do not invent facts. If evidence is insufficient, say so.

JENKINS LOGS:
{log_text}
"""

    print("\nSending Jenkins errors to Qwen AI...")

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()

    ai_analysis = response.json().get(
        "response",
        "No AI response received."
    )

    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    report = f"""
JENKINS AI INCIDENT ANALYSIS REPORT
===================================

Build Number: {BUILD_NUMBER}
Analysis Time: {timestamp}
Log File: {log_file}
AI Model: {MODEL}

ERROR EVIDENCE
==============

{log_text}

AI ROOT CAUSE ANALYSIS
======================

{ai_analysis}
"""

    os.makedirs(REPORT_DIR, exist_ok=True)

    report_file = os.path.join(
        REPORT_DIR,
        f"incident_report_build_{BUILD_NUMBER}.txt"
    )

    with open(report_file, "w", encoding="utf-8") as file:
        file.write(report)

    print("\nAI INCIDENT ANALYSIS")
    print("=" * 50)
    print(ai_analysis)

    print(f"\nIncident report saved: {report_file}")


if __name__ == "__main__":
    analyze_logs()
