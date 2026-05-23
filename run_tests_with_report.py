"""Run all tests and write an HTML report plus Playwright traces on failure."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def main() -> int:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = Path("reports") / f"report_{timestamp}.html"

    command = [
        sys.executable,
        "-m",
        "pytest",
        "--html",
        str(report_path),
        "--self-contained-html",
    ]

    print("Running:", " ".join(command))
    print(f"HTML report: {report_path}")
    print("Traces on failure: test-results/  →  playwright show-trace <trace.zip>")
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
