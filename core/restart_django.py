import os
import sys
import time
import subprocess


if __name__ == "__main__":
    time.sleep(1)  # ✅ Wait for 1000ms (1 second)
    print("🚀 Restarting Django...")

    python_executable = sys.executable
    manage_py = os.path.abspath("manage.py")

    # ✅ Start Django server in a new process
    subprocess.Popen(
        [python_executable, manage_py, "runserver", "0.0.0.0:8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )