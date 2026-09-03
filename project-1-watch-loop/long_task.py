"""
long_task.py
-------------
Part 1 of Project 1 — A Watch Loop.

This script simulates a long-running task. It sleeps for a while, then writes a
completion file that the watcher (watch.py) is waiting for.

Run it in its own terminal:
    python long_task.py
"""

import os
import time
from datetime import datetime

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
# Change this to make the task longer or shorter. The duration is used only
# here, so there is just one place to edit it.
TASK_DURATION_SECONDS = 120

# Directory that holds the completion file.
STATUS_DIR = "task_status"

# Name of the completion file the watcher looks for.
COMPLETION_FILE = "completed.txt"
# ---------------------------------------------------------------------------


def main():
    # Make sure the status directory exists before we write into it.
    os.makedirs(STATUS_DIR, exist_ok=True)

    completed_path = os.path.join(STATUS_DIR, COMPLETION_FILE)

    print(f"[long_task] Long-running task started. It will run for "
          f"{TASK_DURATION_SECONDS} seconds...")

    # Simulate doing work by sleeping for the configured duration.
    time.sleep(TASK_DURATION_SECONDS)

    # Record the moment the work finished.
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write useful information into the completion file.
    with open(completed_path, "w") as f:
        f.write("completion status: DONE\n")
        f.write(f"completion timestamp: {completion_time}\n")

    print(f"[long_task] Task completed! Wrote {completed_path}")
    print(f"[long_task] Completion time: {completion_time}")


if __name__ == "__main__":
    main()
