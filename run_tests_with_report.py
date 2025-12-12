import subprocess
from datetime import datetime
from pathlib import Path


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / f"report_{timestamp}.html"

    cmd = [
        "pytest",
        "--html",
        str(report_path),
        "--self-contained-html",
        "--log-cli-level=INFO",
        "--log-level=INFO",
    ]

    print(f"Running: {' '.join(cmd)}")
    print(f"Reports will be saved to: {report_path}")
    print("Logs will be included in the HTML report")
    # Screenshots on failure are already handled by pytest hook in conftest.py
    subprocess.run(cmd, check=False)


if __name__ == "__main__":
    main()

