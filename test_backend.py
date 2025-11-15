"""
Backend Testing Script - Test each module independently

Run this after adding API keys to .env file
"""

import sys

def test_config():
    """Test 1: Verify API keys are loaded"""
    print("\n" + "="*60)
    print("TEST 1: Configuration Loading")
    print("="*60)

    try:
        from backend import config
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
    print("\n" + "="*60)
    print("TEST 2: Code Generation (OpenAI + Galileo)")
    print("="*60)

    try:
        from backend.generator import generate_code

        prompt = "Write a simple hello world program"
        print(f"Prompt: {prompt}")
        print("\nGenerating code...")

        code = generate_code(prompt)
        print("\n✅ Code generated successfully!")
        print("\nGenerated code:")
        print("-" * 40)
        print(code)
        print("-" * 40)
        print("\n🔭 Check Galileo dashboard - you should see this LLM call tracked!")
        return True
    except Exception as e:
        print(f"❌ Generator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_executor():
    """Test 3: Execute simple code in Daytona"""
    print("\n" + "="*60)
    print("TEST 3: Code Execution (Daytona)")
    print("="*60)

    try:
        from backend.executor import execute_code

        # Simple working code
        test_code = """
print("Hello from Daytona sandbox!")
x = 10 + 5
print(f"Calculation: 10 + 5 = {x}")
"""

        print("Executing simple code in Daytona sandbox...")
        print("Code to execute:")
        print("-" * 40)
        print(test_code)
        print("-" * 40)

        success, output, error = execute_code(test_code, "test_simple.py")

        if success:
            print("\n✅ Execution successful!")
            print("\nOutput:")
            print(output)
        else:
            print("\n❌ Execution failed!")
            print("\nError:")
            print(error)
            return False

        return True
    except Exception as e:
        print(f"❌ Executor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_executor_with_error():
    """Test 4: Execute code that will fail (to test error capture)"""
    print("\n" + "="*60)
    print("TEST 4: Error Capture (Daytona + Sentry)")
    print("="*60)

    try:
        from backend.executor import execute_code
        from backend.sentry_helper import report_error

        # Code that will crash
        broken_code = """
# This will crash - division by zero
x = 10 / 0
print("This won't print")
"""

        print("Executing code that will crash...")
        print("Code:")
        print("-" * 40)
        print(broken_code)
        print("-" * 40)

        success, output, error = execute_code(broken_code, "test_broken.py")

        if not success:
            print("\n✅ Error captured as expected!")
            print("\nError message:")
            print(error)

            # Report to Sentry
            print("\n🔴 Reporting to Sentry...")
            report_error(
                error_message=f"Test error: {error[:200]}",
                context={"test": "backend_testing", "code": broken_code}
            )
            print("✅ Error reported! Check your Sentry dashboard.")
        else:
            print("\n❌ Code should have failed but didn't!")
            return False

        return True
    except Exception as e:
        print(f"❌ Error capture test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fixer():
    """Test 5: Fix broken code"""
    print("\n" + "="*60)
    print("TEST 5: Code Fixing (CodeRabbit Simulation + Galileo)")
    print("="*60)

    try:
        from backend.fixer import fix_code

        broken_code = """
# Calculate average
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
average = total / len(numbers)
print(f"Average: {average}")

# This will crash if list is empty
empty_list = []
bad_avg = sum(empty_list) / len(empty_list)
"""

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
        print("\n🔭 Check Galileo dashboard - you should see the fix generation LLM call!")

        return True
    except Exception as e:
        print(f"❌ Fixer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_workflow():
    """Test 6: Full workflow - generate, execute, fix, re-execute"""
    print("\n" + "="*60)
    print("TEST 6: Full Self-Healing Workflow")
    print("="*60)

    try:
        from backend.generator import generate_code
        from backend.executor import execute_code
        from backend.fixer import fix_code
        from backend.sentry_helper import report_error

        # This prompt should generate code that might have edge case issues
        prompt = "Write a function that calculates the average of a list of numbers"

        print(f"Step 1: Generate code from prompt")
        print(f"Prompt: {prompt}")
        code = generate_code(prompt)
        print("\n✅ Generated code:")
        print("-" * 40)
        print(code)
        print("-" * 40)

        print(f"\nStep 2: Execute in Daytona")
        success, output, error = execute_code(code, "test_workflow.py")

        if success:
            print("\n✅ Code executed successfully on first try!")
            print(output)
        else:
            print("\n⚠️  Code failed (expected for demo)")
            print(f"Error: {error[:200]}")

            print(f"\nStep 3: Report to Sentry")
            report_error(error, {"prompt": prompt, "code": code[:200]})
            print("✅ Reported to Sentry")

            print(f"\nStep 4: Fix with CodeRabbit")
            fixed_code = fix_code(code, error)
            print("✅ Fixed code:")
            print("-" * 40)
            print(fixed_code)
            print("-" * 40)

            print(f"\nStep 5: Re-execute fixed code")
            success, output, error = execute_code(fixed_code, "test_workflow_fixed.py")

            if success:
                print("\n🎉 Fixed code executed successfully!")
                print(output)
            else:
                print("\n❌ Even fixed code failed:")
                print(error)
                return False

        print("\n" + "="*60)
        print("✅ FULL WORKFLOW TEST COMPLETE!")
        print("="*60)
        print("\n📊 Check your dashboards:")
        print("   - Galileo: Should show 2-3 LLM calls")
        print("   - Sentry: Should show the error (if code failed)")
        print("   - Daytona: Check workspace logs")

        return True
    except Exception as e:
        print(f"❌ Full workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n🧪 CodePhoenix Backend Testing Suite")
    print("="*60)
    print("This will test each backend module independently")
    print("Make sure you've added API keys to .env file!")
    print("="*60)

    input("\nPress Enter to start tests...")

    tests = [
        ("Configuration", test_config),
        ("Code Generator", test_generator),
        ("Code Executor", test_executor),
        ("Error Capture", test_executor_with_error),
        ("Code Fixer", test_fixer),
        ("Full Workflow", test_full_workflow),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))

            if not result:
                print(f"\n⚠️  Test '{name}' failed. Continue anyway? (y/n)")
                response = input().strip().lower()
                if response != 'y':
                    print("\nStopping tests.")
                    break
        except KeyboardInterrupt:
            print("\n\nTests interrupted by user.")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results.append((name, False))

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
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("Make sure all API keys are correct in .env file.")

if __name__ == "__main__":
    main()
