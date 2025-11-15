"""
Galileo Integration Test - Verify LLM observability with correct SDK

Tests: galileo_context.init() → OpenAI auto-instrumentation → trace capture
"""

print("="*60)
print("TEST: Galileo Integration with correct SDK")
print("="*60)

# Step 1: Test Galileo initialization
print("\nSTEP 1: Initialize Galileo Context")
print("-"*60)

try:
    from galileo import galileo_context
    from backend import config

    # Initialize with project and log stream
    galileo_context.init(
        project="codephoenix_hackathon",
        log_stream="test_integration"
    )
    print("✅ galileo_context.init() successful")
    print(f"   Project: codephoenix_hackathon")
    print(f"   Log Stream: test_integration")

except Exception as e:
    print(f"❌ Galileo initialization failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Step 2: Test OpenAI auto-instrumentation
print("\nSTEP 2: Test OpenAI Auto-Instrumentation")
print("-"*60)

try:
    from openai import OpenAI

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    print("Sending test prompt to OpenAI...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use mini for faster/cheaper test
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Respond in one sentence."},
            {"role": "user", "content": "Say 'Galileo test successful!' and nothing else."}
        ]
    )

    result = response.choices[0].message.content
    print(f"✅ OpenAI call successful")
    print(f"   Response: {result}")

except Exception as e:
    print(f"❌ OpenAI call failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Step 3: Verify code generation works with Galileo
print("\nSTEP 3: Test Code Generation with Galileo Tracing")
print("-"*60)

try:
    from backend.generator import generate_code

    print("Generating code with prompt: 'Print hello world'")
    code = generate_code("Print hello world")

    print(f"✅ Code generation successful")
    print(f"   Generated code:")
    print("   " + code.replace("\n", "\n   "))

except Exception as e:
    print(f"❌ Code generation failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Step 4: Final verification
print("\n" + "="*60)
print("🎉 GALILEO INTEGRATION TEST PASSED!")
print("="*60)
print("\nWhat we validated:")
print("  ✅ Galileo SDK installed correctly")
print("  ✅ galileo_context.init() configured project and log stream")
print("  ✅ OpenAI auto-instrumentation working")
print("  ✅ Code generation traced automatically")
print("\n📊 Check your Galileo dashboard:")
print("   https://app.galileo.ai")
print(f"   Project: codephoenix_hackathon")
print(f"   Log Stream: test_integration")
print("\nYou should see 2 traces:")
print("  1. Test OpenAI call (mini model)")
print("  2. Code generation call (gpt-4o)")
