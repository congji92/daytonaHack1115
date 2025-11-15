"""
Test 2: Daytona Execution Only
Tests if we can execute simple code in Daytona sandbox
"""

print("="*60)
print("TEST 2: Daytona Code Execution")
print("="*60)

print("\n1. Testing Daytona executor...")
from backend.executor import execute_code

# Simple test code that should work
test_code = """
print("Hello from Daytona!")
x = 10 + 5
print(f"Calculation: 10 + 5 = {x}")
for i in range(3):
    print(f"  Loop {i+1}")
print("Done!")
"""

print("Code to execute:")
print("-"*60)
print(test_code)
print("-"*60)

try:
    print("\nExecuting in Daytona sandbox...")
    success, output, error = execute_code(test_code, "test_daytona.py")

    if success:
        print("\n✅ Execution successful!")
        print("\nOutput:")
        print("-"*60)
        print(output)
        print("-"*60)

        print("\n🎉 Test 2 PASSED - Daytona execution works!")
        print("\nNext: Run test_3_sentry.py to test error tracking")
    else:
        print("\n❌ Execution failed!")
        print("\nError:")
        print("-"*60)
        print(error)
        print("-"*60)
        print("\n❌ Test 2 FAILED")
        exit(1)

except Exception as e:
    print(f"\n❌ Test 2 FAILED: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
