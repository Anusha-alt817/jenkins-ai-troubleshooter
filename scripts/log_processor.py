import os

LOG_DIR = os.getenv("LOG_DIR", "logs")


def process_logs():

    for filename in os.listdir(LOG_DIR):

        if not filename.endswith(".log"):
            continue

        filepath = os.path.join(LOG_DIR, filename)

        print(f"\nAnalyzing log file: {filename}")
        print("-" * 50)

        with open(filepath, "r", encoding="utf-8") as file:
            logs = file.readlines()

        important_lines = []

        keywords = [
            "[ERROR]",
            "[WARNING]",
            "FAILURE",
            "Exception",
            "BUILD FAILURE"
        ]

        for line in logs:
            if any(keyword.lower() in line.lower() for keyword in keywords):
                important_lines.append(line.strip())

        if important_lines:
            print("\nImportant Messages:")
            for message in important_lines:
                print(message)
        else:
            print("No error or warning messages found.")


if __name__ == "__main__":
    process_logs()
