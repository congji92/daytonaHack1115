"""
Automated Backend Testing - No user input required
"""

import sys
import traceback

def run_test(test_name, test_func):
    """Run a single test and report results."""
    print("\n" + "="*60)
    print(f"TEST: {test_name}")
    print("="*60)

    try:
        result = test_func()
        if result:
            print(f"\n✅ {test_name} PASSED")
        else:
            print(f"\n❌ {test_name} FAILED")
        return result
    except Exception as e:
        print(f"\n❌ {test_name} FAILED WITH EXCEPTION")
        print(f"Error: {e}")
        traceback.print_exc()
        return False

def test_config():
    """Test 1: Verify API keys are loaded"""
    from backend import config

    try:
        config.validate_config()
        print("✅ All API keys loaded successfully!")
        print(f"   - OPENAI_API_KEY: {'***' + config.OPENAI_API_KEY[-10:] if config.OPENAI_API_KEY else 'MISSING'}")
        print(f"   - SENTRY_DSN: {'***' + config.SENTRY_DSN[-20:] if config.SENTRY_DSN else 'MISSING'}")
        print(f"   - GALILEO_API_KEY: {'***' + config.GALILEO_API_KEY[-10:] if config.GALILEO_API_KEY else 'MISSING'}")
        print(f"   - DAYTONA_API_KEY: {'***' + config.DAYTONA_API_KEY[-10:] if config.DAYTONA_API_KEY else 'MISSING'}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_generator():
    """Test 2: Generate simple code"""
    from backend.generator import generate_code

    prompt = "Write a simple Python program that prints 'Hello World'"
    print(f"Prompt: {prompt}")
    print("\nGenerating code...")

    code = generate_code(prompt)
    print("\n✅ Code generated successfully!")
    print("\nGenerated code:")
    print("-" * 40)
    print(code)
    print("-" * 40)
    print("\n🔭 Check Galileo dashboard - LLM call should be tracked!")
    return True

def test_executor():
    """Test 3: Execute simple code in Daytona"""
    from backend.executor import execute_code

    test_code = """print("Hello from Daytona sandbox!")
x = 10 + 5
print(f"Calculation: 10 + 5 = {x}")"""

    print("Executing code in Daytona sandbox...")
    print("Code to execute:")
    print("-" * 40)
    print(test_code)
    print("-" * 40)

    success, output, error = execute_code(test_code, "test_simple.py")

    if success:
        print("\n✅ Execution successful!")
        print("\nOutput:")
        print(output)
        return True
    else:
        print("\n❌ Execution failed!")
        print("\nError:")
        print(error)
        return False

def test_error_capture():
    """Test 4: Execute code that will fail"""
    from backend.executor import execute_code
    from backend.sentry_helper import report_error

    broken_code = """# This will crash
x = 10 / 0
print("This won't print")"""

    print("Executing code that will crash...")
    print("Code:")
    print("-" * 40)
    print(broken_code)
    print("-" * 40)

    success, output, error = execute_code(broken_code, "test_broken.py")

    if not success:
        print("\n✅ Error captured as expected!")
        print("\nError message:")
        print(error[:300])

        print("\n🔴 Reporting to Sentry...")
        try:
            report_error(
                error_message=f"Test error: {error[:200]}",
                context={"test": "backend_testing", "code": broken_code}
            )
            print("✅ Error reported! Check your Sentry dashboard.")
        except Exception as e:
            print(f"⚠️  Sentry reporting may have failed (check DSN): {e}")

        return True
    else:
        print("\n❌ Code should have failed but didn't!")
        return False

def test_fixer():
    """Test 5: Fix broken code"""
    from backend.fixer import fix_code

    broken_code = """numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
average = total / len(numbers)
print(f"Average: {average}")

# This will crash
empty_list = []
bad_avg = sum(empty_list) / len(empty_list)"""

    error = "ZeroDivisionError: division by zero"

    print("Broken code:")
    print("-" * 40)
    print(broken_code)
    print("-" * 40)
    print(f"\nError: {error}")
    print("\n🐰 CodeRabbit is analyzing and fixing...")

    fixed_code = fix_code(broken_code, error)

    print("\n✅ Code fixed!")
    print("\nFixed code:")
    print("-" * 40)
    print(fixed_code)
    print("-" * 40)
    print("\n🔭 Check Galileo dashboard - fix generation should be tracked!")

    return True

def main():
    print("\n🧪 CodePhoenix Automated Backend Tests")
    print("="*60)

    tests = [
        ("Configuration Loading", test_config),
        ("Code Generation (OpenAI + Galileo)", test_generator),
        ("Code Execution (Daytona)", test_executor),
        ("Error Capture (Sentry)", test_error_capture),
        ("Code Fixing (CodeRabbit)", test_fixer),
    ]

    results = []
    for name, test_func in tests:
        result = run_test(name, test_func)
        results.append((name, result))

        # Add delay between tests
        if result:
            print(f"\n⏸  Waiting 2 seconds before next test...")
            import time
            time.sleep(2)

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    passed = sum(1 for _, r in results if r)
    total = len(results)

    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)

    if passed == total:
        print("\n🎉 All tests passed! Backend is ready.")
        print("\nNext step: Run the Streamlit app with:")
        print("  streamlit run streamlit_app.py")
    else:
        print("\n⚠️  Some tests failed. Review the errors above.")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
