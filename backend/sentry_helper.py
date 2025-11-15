"""
Sentry Integration - Error tracking and monitoring

SIMPLICITY: Initialize Sentry and provide helper to report errors
"""

import sentry_sdk
from backend import config

# Initialize Sentry SDK (with error handling)
SENTRY_ENABLED = False
try:
    if config.SENTRY_DSN and config.SENTRY_DSN.startswith('https://'):
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            traces_sample_rate=1.0  # Capture 100% of transactions for demo
        )
        SENTRY_ENABLED = True
        print("[sentry] ✅ Sentry initialized successfully")
    else:
        print("[sentry] ⚠️  Sentry DSN format incorrect (should start with https://)")
        print("[sentry]    Get correct DSN from: Sentry Dashboard > Settings > Client Keys")
except Exception as e:
    print(f"[sentry] ⚠️  Failed to initialize Sentry: {e}")
    print("[sentry]    Error tracking will be disabled")

def report_error(error_message: str, error_type: str = "crash", context: dict = None):
    """
    Report an error to Sentry dashboard with classification.

    Args:
        error_message: The error message to report
        error_type: Type of error ("crash", "silent_failure", "handled_exception", "success")
        context: Optional additional context (code, user prompt, etc.)
    """
    if not SENTRY_ENABLED:
        print(f"[sentry] ⚠️  Sentry not enabled, skipping error report")
        print(f"[sentry]    Error ({error_type}): {error_message[:100]}...")
        return

    # Don't report successful executions
    if error_type == "success":
        return

    # Add error type to context
    if context is None:
        context = {}
    context["error_type"] = error_type

    # Set context
    sentry_sdk.set_context("execution_context", context)

    # Choose severity level based on error type
    severity_map = {
        "crash": "error",              # Hard failures - high priority
        "handled_exception": "warning", # Caught exceptions - medium priority
        "silent_failure": "warning"     # No output - medium priority
    }
    level = severity_map.get(error_type, "error")

    # Capture the error
    sentry_sdk.capture_message(error_message, level=level)

    print(f"[sentry] ✅ {error_type.upper()} reported to dashboard (level={level})")
    print(f"[sentry]    Message: {error_message[:100]}...")
