# Project 1 — A Watch Loop

A small, throwaway project that demonstrates an **in-session watch loop** with
Claude Code.

## What this project demonstrates

How a program can keep checking for a condition in a loop, wait between checks,
and stop as soon as the condition is met — *without* running forever. This is
the same idea Claude Code uses to watch for something to happen in a session
(e.g. waiting for a build to finish, a file to appear, or a background task to
complete).

## What the long-running task does

`long_task.py` simulates something that takes a while. It:

1. Prints that it has started.
2. Waits (`time.sleep`) for a configurable number of seconds
   (`TASK_DURATION_SECONDS`, default **120** seconds ≈ 2–3 minutes).
3. Writes a completion file at `task_status/completed.txt` containing:
   - completion status
   - completion timestamp
4. Prints that it has completed.

## What the watcher does

`watch.py` sits in a loop and watches for the task to finish:

1. Checks whether `task_status/completed.txt` exists.
2. If it does **not** exist: prints a short waiting message, waits
   (`CHECK_INTERVAL_SECONDS`, default **60** seconds), then checks again.
3. If it **does** exist: reads the completion information, prints a clear
   "task has finished" message, prints the completion timestamp, notifies
   **only once**, and exits.
4. It has a safety limit (`MAX_CHECKS`, default **10**) so it can never run
   forever even if the task never completes.

## How the loop works

The watcher follows this simple pattern:

```
Check -> Wait -> Check -> Wait -> ... -> Detect completion -> Notify once -> Stop
```

- Each pass checks if `completed.txt` exists.
- If not, it waits and tries again.
- The moment the file exists, it reports completion once and exits.
- `MAX_CHECKS` is the stopping condition that guarantees the loop terminates.

## Why this is an example of an in-session loop

The watcher is a *loop that runs until a condition is met*. It is "in-session"
in the sense that it stays active and keeps checking during the session, rather
than running the logic once and finishing immediately. It demonstrates the
core idea of a watch/check loop: **repeat a check, sleep, repeat — then stop
cleanly at the first success or after a safety limit.**

## Commands

Use two terminals. In **Terminal 1**, start the long task:

```bash
python long_task.py
```

In **Terminal 2**, start the watcher:

```bash
python watch.py
```

The watcher will keep checking while the task runs. When the task creates
`task_status/completed.txt`, the watcher detects it, reports completion once,
and exits.

To stop the watcher early at any time, press **Ctrl+C** — it prints
`Watch loop stopped by user.` and exits cleanly.

## Notes

- Both durations and the safety limit are configurable as variables at the top
  of each file; there are no other dependencies.
- The project uses a throwaway Git repository and touches nothing outside
  this folder.
