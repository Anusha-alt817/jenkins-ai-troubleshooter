import os
import requests

JENKINS_URL = os.getenv("JENKINS_URL", "http://localhost:8080")
JOB_NAME = os.getenv("JOB_NAME")
BUILD_NUMBER = os.getenv("BUILD_NUMBER")

JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")


def collect_logs():

    if not all([JOB_NAME, BUILD_NUMBER, JENKINS_USER, JENKINS_TOKEN]):
        raise ValueError("Required Jenkins environment variables are missing")

    console_url = (
        f"{JENKINS_URL}/job/{JOB_NAME}/{BUILD_NUMBER}/consoleText"
    )

    response = requests.get(
        console_url,
        auth=(JENKINS_USER, JENKINS_TOKEN),
        timeout=30
    )

    response.raise_for_status()

    os.makedirs("logs", exist_ok=True)

    log_file = f"logs/jenkins-build-{BUILD_NUMBER}.log"

    with open(log_file, "w", encoding="utf-8") as file:
        file.write(response.text)

    print(f"Jenkins logs collected successfully: {log_file}")


if __name__ == "__main__":
    collect_logs()
