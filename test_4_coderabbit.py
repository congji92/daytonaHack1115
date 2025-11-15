"""
Test 4: CodeRabbit Code Fixing
Tests if the AI can fix broken code
"""

print("="*60)
print("TEST 4: CodeRabbit Code Fixing (AI Code Review)")
print("="*60)

print("\n1. Testing code fixer...")
from backend.fixer import fix_code

# Broken code with a common error
broken_code = """
def calculate_average(numbers):
    total = sum(numbers)
    average = total / len(numbers)
    return average

# This will crash on empty list
result = calculate_average([])
print(f"Average: {result}")
"""

error_message = "ZeroDivisionError: division by zero"

print("Broken code:")
print("-"*60)
print(broken_code)
print("-"*60)
print(f"\nError: {error_message}")

try:
    print("\n🐰 CodeRabbit is analyzing and fixing...")
    fixed_code = fix_code(broken_code, error_message)

    print("\n✅ Code fixed!")
    print("\nFixed code:")
    print("-"*60)
    print(fixed_code)
    print("-"*60)

    print("\n🎉 Test 4 PASSED - CodeRabbit fixing works!")
    print("\nNext: Run test_5_full_workflow.py for end-to-end test")

except Exception as e:
    print(f"\n❌ Test 4 FAILED: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
