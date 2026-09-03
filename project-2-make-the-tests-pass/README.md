# Project 2 — Make the Tests Pass, Then Stop

## Overview

This project demonstrates a **conditional loop** with a **maker-checker pattern** for automated test-driven development. The agent repeatedly inspects failing tests, makes fixes, runs the test command, and continues only while tests are still failing.

**Key Principle:** The test runner is the authority that decides whether the task is complete.

---

## What This Project Demonstrates

### 1. Conditional Loop

A conditional loop runs until a specific condition is met, rather than for a fixed number of iterations or time period. In this case:

```
LOOP UNTIL: tests pass (exit code 0)
SAFETY LIMIT: maximum 6 attempts
```

The loop checks a condition (test results) after each iteration and decides whether to continue or stop.

### 2. Maker-Checker Pattern

This project implements a **maker-checker pattern** where:

- **The MAKER** (implementation work):
  - Examines the current implementation
  - Identifies bugs by comparing expected vs actual behavior
  - Applies fixes to the code
  - Prepares the next attempt

- **The CHECKER** (test validation):
  - Runs the test command: `python -m pytest -q`
  - Captures exit code and output
  - Determines if the implementation is correct
  - **Has absolute authority** — the maker cannot override the checker

### 3. Test Runner as Source of Truth

The test runner (`pytest`) is the **single source of truth**:

```python
if exit_code == 0:
    # Tests passed — we're done
    STOP
else:
    # Tests failed — keep trying
    CONTINUE
```

The agent never declares success without running the tests. The exit code determines reality.

---

## Project Structure

```
project-2-make-the-tests-pass/
├── calculator.py          # Module with intentionally buggy implementations
├── watch_loop.py          # The conditional loop script
├── tests/
│   └── test_calculator.py # Test suite (the checker)
└── README.md              # This file
```

### Files Explained

#### `calculator.py`
Contains four functions with intentional bugs:
- `add(a, b)` — off-by-one error (returns `a + b + 1`)
- `subtract(a, b)` — off-by-one error (returns `a - b - 1`)
- `multiply(a, b)` — extra addition (returns `a * b + a`)
- `divide(a, b)` — extra multiplication (returns `a / b * 2`)

#### `tests/test_calculator.py`
12 test cases that define the correct behavior. These tests are **never modified** — they are the authority.

#### `watch_loop.py`
The conditional loop that:
1. Reads the implementation
2. Identifies and fixes bugs
3. Runs pytest
4. Checks exit code
5. Stops if tests pass, or continues if they fail
6. Enforces maximum 6 attempts

---

## Why the Test Runner is the Source of Truth

```
┌─────────────────────────────────────────────────────────┐
│                    THE TRUTH PYRAMID                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │          TEST RUNNER (pytest exit code)         │   │
│   │            ← Ultimate authority                 │   │
│   └─────────────────────────────────────────────────┘   │
│                         ▲                               │
│                         │                               │
│   ┌─────────────────────────────────────────────────┐   │
│   │              TESTS (test_calculator.py)         │   │
│   │            ← Define correct behavior            │   │
│   └─────────────────────────────────────────────────┘   │
│                         ▲                               │
│                         │                               │
│   ┌─────────────────────────────────────────────────┐   │
│   │        IMPLEMENTATION (calculator.py)           │   │
│   │            ← Being validated                    │   │
│   └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

- The **implementation** claims to do something
- The **tests** define what "correct" means
- The **test runner** decides if claims match reality

The agent (maker) can only influence the implementation — it cannot change the tests or the test runner's verdict.

---

## What the Maker Does

The maker is responsible for:

1. **Reading** the current implementation
2. **Comparing** expected behavior (from tests) with actual behavior
3. **Identifying** the specific bug
4. **Applying** a fix
5. **Preparing** for the next validation cycle

```python
def maker_fix(attempt: int) -> bool:
    """Examine implementation and apply a fix."""
    content = read_file("calculator.py")

    # Find and fix bugs
    for fix in BUG_FIXES:
        if fix["old"] in content:
            content = content.replace(fix["old"], fix["new"])
            write_file("calculator.py", content)
            return True

    return False  # No more fixes available
```

---

## What the Checker Does

The checker is responsible for:

1. **Running** the test command
2. **Capturing** exit code and output
3. **Reporting** results
4. **Deciding** whether to continue or stop

```python
def checker_run() -> tuple[int, str]:
    """Run tests and return results."""
    result = subprocess.run(
        ["python", "-m", "pytest", "-q"],
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout + result.stderr
```

**Exit code interpretation:**
- `0` = All tests passed → STOP
- Non-zero = Tests failed → CONTINUE

---

## Why This is a Maker-Checker Pattern

The maker-checker pattern separates concerns:

| Role | Responsibility | Authority |
|------|---------------|-----------|
| **Maker** | Write/fix code | Can modify implementation only |
| **Checker** | Validate code | Decides pass/fail (exit code) |

**Critical rule:** The maker cannot override the checker.

```python
# BAD - Maker declaring success without checker
"I think the code is fixed now. We're done."

# GOOD - Maker waits for checker's verdict
exit_code, output = checker_run()
if exit_code == 0:
    STOP  # Checker says we're done
```

---

## Stopping Conditions

### Primary: Tests Pass

```python
if exit_code == 0:
    print("SUCCESS")
    print(f"All tests passed on attempt {attempt}.")
    STOP
```

This is the **happy path** — the loop achieved its goal.

### Secondary: Maximum Attempts Reached

```python
for attempt in range(1, MAX_ATTEMPTS + 1):
    # ... fix and test ...

# If we reach here, loop completed without success
print("LIMIT REACHED")
print(f"Tests are still failing after {MAX_ATTEMPTS} attempts.")
```

This is the **safety limit** — prevents infinite loops.

---

## Why Maximum 6 Attempts?

1. **Prevents infinite loops** — A broken implementation could loop forever
2. **Forces reflection** — If 6 attempts aren't enough, something is fundamentally wrong
3. **Conserves resources** — Avoids wasting compute on hopeless cases
4. **Clear failure signal** — Distinguishes "tried but failed" from "gave up"

---

## Two Possible Outcomes

### Outcome 1: SUCCESS

```
Tests passed → STOP
```

- The loop achieved its goal
- All tests are passing
- The implementation is correct

### Outcome 2: FAILURE

```
6 attempts reached + tests still failing → STOP → Report failure
```

- The safety limit was reached
- Tests are still failing
- **Do NOT claim success**
- Report the failure clearly

**The distinction is critical:**
- Success = tests actually passed (verified by test runner)
- Failure = gave up after maximum attempts (tests still failing)

---

## Usage

### Run Tests Only

```bash
python -m pytest -q
```

### Run the Watch Loop

```bash
python watch_loop.py
```

### Expected Output (Successful Run)

```
============================================================
WATCH LOOP - Conditional Loop with Maker-Checker Pattern
============================================================

Configuration:
  Max attempts: 6
  Test command: python -m pytest -q
  Target file: calculator.py

------------------------------------------------------------
Attempt 1/6
------------------------------------------------------------

[Step 1: MAKER]
  [MAKER] Examining implementation...
  [MAKER] Found bug: Fix add() function - remove off-by-one error
  [MAKER] Applied fix.

[Step 2: CHECKER]
  [CHECKER] Running: python -m pytest -q

  Result:
    Passed: 3
    Failed: 9

  Exit code: 1

[Step 3: CHECK CONDITION]
  Checker says: FAIL ✗

  Continuing to next attempt...

------------------------------------------------------------
Attempt 2/6
... (continues fixing and testing)
------------------------------------------------------------
Attempt 5/6
------------------------------------------------------------

[Step 1: MAKER]
  [MAKER] Examining implementation...
  [MAKER] Found bug: Fix divide() function - remove extra multiplication
  [MAKER] Applied fix.

[Step 2: CHECKER]
  [CHECKER] Running: python -m pytest -q

  Result:
    Passed: 12

  Exit code: 0

[Step 3: CHECK CONDITION]
  Checker says: PASS ✓

============================================================
SUCCESS
============================================================
All tests passed on attempt 5.
Stopping loop.
============================================================
```

---

## Key Concepts

### Heartbeat
The test run (`pytest -q`) is the heartbeat of this system. Each beat checks: "Is the code correct yet?"

### Maker
The code examination and fixing logic. It tries to improve the implementation based on knowledge of common bugs.

### Checker
The test runner. It has absolute authority. Its exit code is the truth.

### Success Condition
`exit_code == 0` — All tests passed.

### Safety Limit
`MAX_ATTEMPTS = 6` — Prevents infinite loops and forces reflection.

### Conditional Loop
Runs until a condition is met (tests pass), not for a fixed duration or count.

---

## Why This Matters

This pattern is fundamental to autonomous systems:

1. **Reliability** — The system stops when the goal is achieved
2. **Safety** — The system stops when it can't achieve the goal
3. **Transparency** — Clear distinction between success and failure
4. **Authority** — The test runner (not the agent) decides success

Without this pattern, an agent might:
- Declare success without verification
- Loop forever on impossible tasks
- Confuse "I think it's fixed" with "tests pass"

---

## License

This project is part of the Loop Engineering course.
