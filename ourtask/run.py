import subprocess
import os

def run_pynguin():
    os.environ['PYNGUIN_DANGER_AWARE'] = 'true'

    os.makedirs("generated_tests", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    cmd = [
        "python",
        "-m",
        "pynguin",
        "--project-path", "./",
        "--module-name", "numpy_example",
        "--output-path", "./generated_tests",
        "--assertion-generation", "SIMPLE",
        "--algorithm", "DYNAMOSA",
        "--population", "50",
        "--maximum-search-time", "60",
        "--report-dir", "./reports",
        "--statistics-backend", "CSV"
    ]

    subprocess.run(cmd)


if __name__ == "__main__":
    run_pynguin()