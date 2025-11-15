"""
Test 1: LLM Code Generation Only (OpenAI)
Tests the most basic functionality without any other dependencies
"""

print("="*60)
print("TEST 1: LLM Code Generation (OpenAI Only)")
print("="*60)

# Test config
print("\n1. Loading configuration...")
from backend import config

try:
    config.validate_config()
    print("✅ Config loaded")
    print(f"   OpenAI Key: ***{config.OPENAI_API_KEY[-10:]}")
except Exception as e:
    print(f"❌ Config failed: {e}")
    exit(1)

# Test code generation
print("\n2. Testing code generation...")
from backend.generator import generate_code

prompt = "Write a Python program that prints 'Hello from CodePhoenix!'"
print(f"   Prompt: {prompt}")

try:
    print("   Calling OpenAI...")
    code = generate_code(prompt)

    print("\n✅ Code generated successfully!")
    print("\n" + "-"*60)
    print("GENERATED CODE:")
    print("-"*60)
    print(code)
    print("-"*60)

    print("\n🎉 Test 1 PASSED - LLM generation works!")
    print("\nNext: Run test_2_daytona.py to test code execution")

except Exception as e:
    print(f"\n❌ Test 1 FAILED: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
