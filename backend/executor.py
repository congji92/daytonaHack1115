"""
Code Executor - Runs generated Python code in Daytona sandbox

REUSED PATTERN: Based on claudeTutorial/step3_sandboxes/daytona_sandbox.py
Simplified for hackathon - just the essentials for code execution
"""

import tempfile
import os
import re
from typing import Tuple
from daytona import Daytona, DaytonaConfig, CreateSandboxFromImageParams
from backend import config

def _get_daytona_client():
    """
    Initialize Daytona client (reused pattern from claudeTutorial).
    """
    if not config.DAYTONA_API_KEY:
        raise ValueError("DAYTONA_API_KEY not found in environment")

    daytona_config = DaytonaConfig(
        api_key=config.DAYTONA_API_KEY,
        api_url=config.DAYTONA_API_URL
    )

    return Daytona(daytona_config)

def _classify_error(exit_code: int, stdout: str, stderr: str) -> str:
    """
    Classify execution outcome for better error handling.

    Returns:
        - "success": Normal execution with output
        - "silent_failure": Succeeded but no output (likely handled exception)
        - "handled_exception": Succeeded but exception patterns in output
        - "crash": Hard failure with non-zero exit code
    """
    # Hard crash
    if exit_code != 0:
        return "crash"

    # Check for exception patterns even if caught
    exception_patterns = [
        r'ZeroDivisionError',
        r'ValueError',
        r'TypeError',
        r'KeyError',
        r'IndexError',
        r'AttributeError',
        r'FileNotFoundError',
        r'Exception',
        r'Error:',
        r'Traceback',
        r'Cannot divide by zero'
    ]

    combined_output = stdout + stderr
    for pattern in exception_patterns:
        if re.search(pattern, combined_output, re.IGNORECASE):
            return "handled_exception"

    # Success but no output (suspicious)
    if not stdout.strip() and not stderr.strip():
        return "silent_failure"

    return "success"

def execute_code(code: str, filename: str = "generated_script.py") -> Tuple[bool, str, str, str]:
    """
    Execute Python code in a Daytona sandbox.

    Args:
        code: Python code to execute
        filename: Name for the generated file (for saving locally)

    Returns:
        Tuple of (success: bool, output: str, error: str, error_type: str)
        error_type can be: "success", "silent_failure", "handled_exception", "crash"
    """
    daytona = _get_daytona_client()
    sandbox = None

    try:
        # Save code locally for reference
        output_path = os.path.join("generated_code", filename)
        with open(output_path, "w") as f:
            f.write(code)
        print(f"[executor] Saved code to {output_path}")

        # Create Daytona sandbox
        print("[executor] Creating Daytona sandbox...")
        params = CreateSandboxFromImageParams(image="python:3.11-slim")
        sandbox = daytona.create(params, timeout=150)
        print(f"[executor] ✓ Sandbox created")

        # Upload code to sandbox
        print("[executor] Uploading code...")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            sandbox.fs.upload_file(temp_file, "script.py")
        finally:
            os.unlink(temp_file)

        # Execute code in sandbox
        print("[executor] Executing code in Daytona...")

        # code_run() expects Python code, not shell commands
        # So we create a Python wrapper that executes the uploaded script
        exec_wrapper = """
import sys
import io
import json

# Capture stdout and stderr
old_stdout = sys.stdout
old_stderr = sys.stderr
stdout_capture = io.StringIO()
stderr_capture = io.StringIO()

sys.stdout = stdout_capture
sys.stderr = stderr_capture

exit_code = 0
try:
    exec(open('script.py').read(), {'__name__': '__main__'})
except Exception as e:
    import traceback
    stderr_capture.write(f"ERROR: {e}\\n")
    stderr_capture.write(traceback.format_exc())
    exit_code = 1
finally:
    sys.stdout = old_stdout
    sys.stderr = old_stderr

# Output results
result = {
    'stdout': stdout_capture.getvalue(),
    'stderr': stderr_capture.getvalue(),
    'exit_code': exit_code
}
print('__RESULT__')
print(json.dumps(result))
"""

        response = sandbox.process.code_run(exec_wrapper, timeout=60)

        # Parse results
        output = response.result if hasattr(response, 'result') else str(response)

        # Extract JSON result
        if '__RESULT__' in output:
            import json
            json_part = output.split('__RESULT__')[1].strip()
            try:
                result = json.loads(json_part)
                exit_code = result.get('exit_code', 1)
                stdout = result.get('stdout', '')
                stderr = result.get('stderr', '')
            except json.JSONDecodeError:
                exit_code = 1
                stdout = output
                stderr = "Failed to parse execution result"
        else:
            exit_code = response.exit_code if hasattr(response, 'exit_code') else 1
            stdout = output
            stderr = ""

        success = exit_code == 0

        # Classify the error type
        error_type = _classify_error(exit_code, stdout, stderr)
        print(f"[executor] Execution complete (success={success}, type={error_type})")

        if success:
            return True, stdout, "", error_type
        else:
            return False, "", stderr if stderr else stdout, error_type

    except Exception as e:
        error_msg = f"Daytona execution failed: {str(e)}"
        print(f"[executor] ERROR: {error_msg}")
        return False, "", error_msg, "crash"

    finally:
        # Cleanup sandbox
        if sandbox is not None:
            try:
                print("[executor] Cleaning up sandbox...")
                sandbox.delete()
                print("[executor] ✓ Sandbox deleted")
            except Exception as e:
                print(f"[executor] Warning: Failed to delete sandbox: {e}")
