"""
watch.py
--------
Part 2 of Project 1 — A Watch Loop.

This script repeatedly checks whether the long-running task has finished by
looking for task_status/completed.txt.

It follows the pattern:
    Check -> Wait -> Check -> Wait -> ... -> Detect completion -> Notify once -> Stop

Run it in its own terminal (separate from long_task.py):
    python watch.py
"""

import os
import sys
import time
from datetime import datetime

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
# Interval in seconds between checks.
CHECK_INTERVAL_SECONDS = 60

# Safety limit: stop after this many checks so the watcher can never run
# forever, even if the completion file is never created.
MAX_CHECKS = 10

# Location of the completion file the watcher is waiting for.
STATUS_DIR = "task_status"
COMPLETION_FILE = "completed.txt"
# ---------------------------------------------------------------------------


def read_completion(path):
    """Read the completion file and return its lines."""
    with open(path, "r") as f:
        return f.read().splitlines()


def main():
    completed_path = os.path.join(STATUS_DIR, COMPLETION_FILE)

    print(f"[watch] Watching for {completed_path} ...")
    print(f"[watch] Checking every {CHECK_INTERVAL_SECONDS}s, "
          f"up to {MAX_CHECKS} times.")

    for attempt in range(1, MAX_CHECKS + 1):
        if os.path.exists(completed_path):
            # The task is done. Read the completion information, report it
            # once, and exit immediately. No further checks.
            lines = read_completion(completed_path)
            print()
            print(f"[watch] >>> TASK HAS FINISHED (check #{attempt}) <<<")
            for line in lines:
                print(f"[watch]   {line}")
            print("[watch] Exiting cleanly.")
            return  # stop here: notify once, then quit

        # File not there yet: report the check and wait before trying again.
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[watch] Check #{attempt}/{MAX_CHECKS} at {now}: "
              f"not done yet, waiting {CHECK_INTERVAL_SECONDS}s...")
        time.sleep(CHECK_INTERVAL_SECONDS)

    # If we get here, the safety limit was reached without the task finishing.
    print()
    print(f"[watch] Stopping: reached the safety limit of "
          f"{MAX_CHECKS} checks and the task is still not complete.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully: no traceback, just a short message.
        print()
        print("[watch] Watch loop stopped by user.")
        sys.exit(0)
