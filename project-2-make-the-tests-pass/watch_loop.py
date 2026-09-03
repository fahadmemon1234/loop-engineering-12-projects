"""
Watch Loop - Conditional Loop with Maker-Checker Pattern

This script demonstrates:
1. A conditional loop that runs until a condition is met (tests pass)
2. A maker-checker pattern where:
   - The "maker" examines and fixes the implementation
   - The "checker" (pytest) validates whether the fix worked
3. The test runner as the source of truth
4. Maximum attempt safety limit

The loop continues fixing and testing until either:
- All tests pass (SUCCESS)
- Maximum attempts reached (FAILURE)
"""

import subprocess
import sys
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

MAX_ATTEMPTS = 6  # Safety limit - maximum number of fix/test cycles
TEST_COMMAND = ["python", "-m", "pytest", "-q"]  # The checker command
CALCULATOR_FILE = "calculator.py"  # The file to fix

# ============================================================================
# MAKER - Examines and fixes the implementation
# ============================================================================

# Bug fixes mapping: maps incorrect code patterns to correct replacements
# In a real autonomous system, this would be done by an AI agent
# examining the failing tests and the implementation.
BUG_FIXES = [
    {
        "description": "Fix add() function - remove off-by-one error",
        "old": "return a + b + 1  # BUG: should be a + b",
        "new": "return a + b",
    },
    {
        "description": "Fix subtract() function - remove off-by-one error",
        "old": "return a - b - 1  # BUG: should be a - b",
        "new": "return a - b",
    },
    {
        "description": "Fix multiply() function - remove extra addition",
        "old": "return a * b + a  # BUG: should be a * b",
        "new": "return a * b",
    },
    {
        "description": "Fix divide() function - remove extra multiplication",
        "old": "return a / b * 2  # BUG: should be a / b",
        "new": "return a / b",
    },
]


def read_file(filepath: str) -> str:
    """Read the contents of a file."""
    with open(filepath, "r") as f:
        return f.read()


def write_file(filepath: str, content: str) -> None:
    """Write content to a file."""
    with open(filepath, "w") as f:
        f.write(content)


def maker_fix(attempt: int) -> bool:
    """
    MAKER: Examine the implementation and apply a fix.

    This function simulates what an AI agent would do:
    1. Read the current implementation
    2. Identify a bug
    3. Apply a fix

    Returns True if a fix was applied, False if no more fixes available.
    """
    print(f"  [MAKER] Examining implementation...")

    content = read_file(CALCULATOR_FILE)

    # Try to apply fixes in order
    for fix in BUG_FIXES:
        if fix["old"] in content:
            print(f"  [MAKER] Found bug: {fix['description']}")
            content = content.replace(fix["old"], fix["new"])
            write_file(CALCULATOR_FILE, content)
            print(f"  [MAKER] Applied fix.")
            return True

    print(f"  [MAKER] No more known bugs found in code.")
    return False


# ============================================================================
# CHECKER - Runs tests to validate the implementation
# ============================================================================

def checker_run() -> tuple[int, str]:
    """
    CHECKER: Run the test command and capture results.

    Returns:
        tuple: (exit_code, output_text)
    """
    print(f"  [CHECKER] Running: {' '.join(TEST_COMMAND)}")

    result = subprocess.run(
        TEST_COMMAND,
        capture_output=True,
        text=True,
        cwd="."
    )

    output = result.stdout + result.stderr
    return result.returncode, output


def parse_test_results(output: str) -> dict:
    """Parse pytest output to extract test counts."""
    results = {"passed": 0, "failed": 0, "errors": 0}

    # Look for patterns like "3 passed", "1 failed", "2 passed, 1 failed"
    passed_match = re.search(r"(\d+) passed", output)
    failed_match = re.search(r"(\d+) failed", output)
    error_match = re.search(r"(\d+) error", output)

    if passed_match:
        results["passed"] = int(passed_match.group(1))
    if failed_match:
        results["failed"] = int(failed_match.group(1))
    if error_match:
        results["errors"] = int(error_match.group(1))

    return results


# ============================================================================
# LOOP - Conditional loop with safety limit
# ============================================================================

def run_loop():
    """
    Run the conditional loop: fix → test → fix → test → ...

    The loop continues until:
    - Tests pass (exit code 0) → SUCCESS
    - Maximum attempts reached → FAILURE
    """
    print("=" * 60)
    print("WATCH LOOP - Conditional Loop with Maker-Checker Pattern")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Max attempts: {MAX_ATTEMPTS}")
    print(f"  Test command: {' '.join(TEST_COMMAND)}")
    print(f"  Target file: {CALCULATOR_FILE}")
    print()

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print("-" * 60)
        print(f"Attempt {attempt}/{MAX_ATTEMPTS}")
        print("-" * 60)

        # STEP 1: MAKER - Fix the implementation
        print(f"\n[Step 1: MAKER]")
        fix_applied = maker_fix(attempt)

        if not fix_applied:
            print(f"\n  No fixes to apply. Moving to checker anyway...")
        print()

        # STEP 2: CHECKER - Run tests
        print(f"[Step 2: CHECKER]")
        exit_code, output = checker_run()

        # Parse results
        results = parse_test_results(output)

        # Display results
        print(f"\n  Result:")
        if results["passed"] > 0:
            print(f"    Passed: {results['passed']}")
        if results["failed"] > 0:
            print(f"    Failed: {results['failed']}")
        if results["errors"] > 0:
            print(f"    Errors: {results['errors']}")

        print(f"\n  Exit code: {exit_code}")

        # STEP 3: CHECK CONDITION
        print(f"\n[Step 3: CHECK CONDITION]")

        if exit_code == 0:
            # SUCCESS - Tests passed
            print(f"  Checker says: PASS [OK]")
            print()
            print("=" * 60)
            print("SUCCESS")
            print("=" * 60)
            print(f"All tests passed on attempt {attempt}.")
            print(f"Stopping loop.")
            print("=" * 60)
            return True
        else:
            # FAIL - Tests still failing
            print(f"  Checker says: FAIL [X]")
            print(f"\n  Continuing to next attempt...")
            print()

    # MAX ATTEMPTS REACHED
    print()
    print("=" * 60)
    print("LIMIT REACHED")
    print("=" * 60)
    print(f"Tests are still failing after {MAX_ATTEMPTS} attempts.")
    print(f"The loop stopped because the safety limit was reached.")
    print(f"Do NOT claim success.")
    print("=" * 60)
    return False


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    success = run_loop()
    sys.exit(0 if success else 1)
