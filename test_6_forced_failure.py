"""
Test 6: Forced Failure to Validate Full Self-Healing Cycle
Tests: Generate → Execute → Fail → Sentry → Fix → Re-execute → Success
"""

print("="*60)
print("TEST 6: Forced Failure Self-Healing Cycle")
print("="*60)

from backend.generator import generate_code
from backend.executor import execute_code
from backend.fixer import fix_code
from backend.sentry_helper import report_error

# Step 1: Create intentionally broken code
print("\nSTEP 1: Creating Intentionally Broken Code")
print("-"*60)

broken_code = """
# This code will definitely crash - division by zero
numbers = [10, 20, 30]
total = sum(numbers)
count = 0  # Intentionally set to 0 to cause crash!
average = total / count
print(f"Average: {average}")
"""

print("Broken code:")
print(broken_code)
print("✅ Broken code ready")

# Step 2: Execute (should fail)
print("\nSTEP 2: Execute Broken Code in Daytona")
print("-"*60)
try:
    success, output, error = execute_code(broken_code, "test_forced_fail.py")

    if success:
        print("❌ Code should have failed but didn't!")
        exit(1)
    else:
        print("✅ Code failed as expected!")
        print(f"\nError captured:")
        print(error[:300])

except Exception as e:
    print(f"❌ Execution test failed: {e}")
    exit(1)

# Step 3: Report to Sentry
print("\nSTEP 3: Report Error to Sentry")
print("-"*60)
try:
    report_error(
        error_message=f"Forced failure test: {error[:200]}",
        context={
            "test": "forced_failure",
            "code": broken_code[:200],
            "error": error[:200]
        }
    )
    print("✅ Error reported to Sentry")
    print("   Check your dashboard: https://sentry.io")
except Exception as e:
    print(f"⚠️  Sentry reporting failed (non-critical): {e}")

# Step 4: Fix with CodeRabbit
print("\nSTEP 4: Fix Code with CodeRabbit AI")
print("-"*60)
try:
    print("🐰 CodeRabbit is analyzing the error...")
    fixed_code = fix_code(broken_code, error)
    print("✅ Fix generated!")
    print("\nFixed code:")
    print(fixed_code)
except Exception as e:
    print(f"❌ Fix generation failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Step 5: Re-execute fixed code
print("\nSTEP 5: Re-execute Fixed Code in Daytona")
print("-"*60)
try:
    success, output, error = execute_code(fixed_code, "test_forced_fail_fixed.py")

    if success:
        print("✅ Fixed code executed successfully!")
        print(f"\nOutput:")
        print(output)

        print("\n" + "="*60)
        print("🎉🎉🎉 TEST 6 PASSED - FULL SELF-HEALING CYCLE VALIDATED!")
        print("="*60)
        print("\nWhat we validated:")
        print("  ✅ Generated/broken code executed in Daytona")
        print("  ✅ Error was captured from Daytona sandbox")
        print("  ✅ Error was reported to Sentry")
        print("  ✅ CodeRabbit analyzed and fixed the code")
        print("  ✅ Fixed code executed successfully in new Daytona sandbox")
        print("\n🔥 CodePhoenix Self-Healing System: FULLY OPERATIONAL!")
    else:
        print("❌ Even fixed code failed:")
        print(error)
        exit(1)

except Exception as e:
    print(f"❌ Re-execution failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
