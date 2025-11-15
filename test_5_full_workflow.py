"""
Test 5: Full Workflow Integration
Tests the complete self-healing cycle: generate → execute → fix → re-execute
"""

print("="*60)
print("TEST 5: Full Self-Healing Workflow")
print("="*60)

from backend.generator import generate_code
from backend.executor import execute_code
from backend.fixer import fix_code
from backend.sentry_helper import report_error

# This prompt is likely to generate code with an edge case issue
prompt = "Write a function that calculates the average of a list of numbers and test it with an empty list"

print(f"User Prompt: {prompt}")
print("\n" + "="*60)

# Step 1: Generate
print("\nSTEP 1: Generate Code")
print("-"*60)
try:
    code = generate_code(prompt)
    print("Generated code:")
    print(code[:300] + "..." if len(code) > 300 else code)
    print("✅ Generation complete")
except Exception as e:
    print(f"❌ Generation failed: {e}")
    exit(1)

# Step 2: Execute
print("\nSTEP 2: Execute in Daytona")
print("-"*60)
try:
    success, output, error = execute_code(code, "test_workflow.py")

    if success:
        print("✅ Code executed successfully on first try!")
        print("Output:", output[:200])
        print("\n🎉 Perfect! No fix needed.")
        print("\nTest 5 PASSED - System works end-to-end!")
        exit(0)
    else:
        print("⚠️  Code failed (expected for demo)")
        print(f"Error: {error[:200]}")
        print("✅ Error captured")

except Exception as e:
    print(f"❌ Execution failed: {e}")
    exit(1)

# Step 3: Report to Sentry
print("\nSTEP 3: Report Error to Sentry")
print("-"*60)
try:
    report_error(error[:200], {"prompt": prompt, "code": code[:200]})
    print("✅ Reported to Sentry (if enabled)")
except Exception as e:
    print(f"⚠️  Sentry reporting failed (non-critical): {e}")

# Step 4: Fix
print("\nSTEP 4: Fix Code with CodeRabbit")
print("-"*60)
try:
    fixed_code = fix_code(code, error)
    print("Fixed code:")
    print(fixed_code[:300] + "..." if len(fixed_code) > 300 else fixed_code)
    print("✅ Fix generated")
except Exception as e:
    print(f"❌ Fix generation failed: {e}")
    exit(1)

# Step 5: Re-execute
print("\nSTEP 5: Re-execute Fixed Code")
print("-"*60)
try:
    success, output, error = execute_code(fixed_code, "test_workflow_fixed.py")

    if success:
        print("✅ Fixed code executed successfully!")
        print("Output:", output[:200])
        print("\n🎉🎉🎉 Test 5 PASSED - Full self-healing workflow works!")
        print("\n" + "="*60)
        print("ALL TESTS COMPLETE!")
        print("="*60)
        print("\nYour backend is ready!")
        print("Next step: Run streamlit app with:")
        print("  streamlit run streamlit_app.py")
    else:
        print("❌ Even fixed code failed")
        print(f"Error: {error[:200]}")
        print("\n❌ Test 5 FAILED")
        exit(1)

except Exception as e:
    print(f"❌ Re-execution failed: {e}")
    exit(1)
