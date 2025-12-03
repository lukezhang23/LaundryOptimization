import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    result = subprocess.run(
        [sys.executable, script_path],
        cwd=BASE_DIR   # <<— force working directory
    )
    if result.returncode != 0:
        print(f"Error: {script_name} failed with exit code {result.returncode}")
        sys.exit(result.returncode)


if __name__ == "__main__":
    run_script("generate_final_chart.py")
    run_script("pdf_to_png.py")

    print("All scripts ran successfully!")
