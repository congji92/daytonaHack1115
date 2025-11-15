"""
Test 3: Sentry Error Tracking
Tests if Sentry can capture and report errors
"""

print("="*60)
print("TEST 3: Sentry Error Tracking")
print("="*60)

print("\n1. Initializing Sentry...")
from backend.sentry_helper import report_error, SENTRY_ENABLED

if not SENTRY_ENABLED:
    print("⚠️  Sentry is not enabled!")
    print("   To enable Sentry:")
    print("   1. Go to https://sentry.io")
    print("   2. Go to Settings > Projects > Your Project > Client Keys (DSN)")
    print("   3. Copy the DSN (starts with https://)")
    print("   4. Update SENTRY_DSN in .env file")
    print("\n⏭  Skipping test (not critical for demo)")
    exit(0)

print("✅ Sentry is enabled")

print("\n2. Reporting test error...")
test_error = "Test error from CodePhoenix backend testing"
test_context = {
    "test": "sentry_integration",
    "component": "error_reporting"
}

try:
    report_error(test_error, test_context)

    print("\n✅ Error reported to Sentry!")
    print("\n🔴 Check your Sentry dashboard:")
    print("   https://sentry.io")
    print("   You should see the test error appear")

    print("\n🎉 Test 3 PASSED - Sentry works!")
    print("\nNext: Run test_4_coderabbit.py to test code fixing")

except Exception as e:
    print(f"\n❌ Test 3 FAILED: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
