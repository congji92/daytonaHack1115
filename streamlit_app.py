"""
CodePhoenix - Self-Healing Code Generator

SIMPLE SERVICE ORCHESTRATION:
1. User enters prompt
2. Generate code (LLM + Galileo)
3. Execute in Daytona
4. If error: Report to Sentry + Fix with CodeRabbit + Re-execute
5. Display results

That's it. No complex logic, just wiring sponsors together.
"""

import streamlit as st
from datetime import datetime
from backend import config
from backend.generator import generate_code
from backend.executor import execute_code
from backend.fixer import fix_code
from backend.sentry_helper import report_error

# Page config
st.set_page_config(
    page_title="CodePhoenix - gen-repair-execute",
    page_icon="🔥",
    layout="wide"
)

# Animated gradient background + liquid glass sidebar
st.markdown("""
<style>
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Liquid glass sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    /* Sidebar text color - white for visibility */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Sidebar headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }

    /* Top header bar - transparent background */
    header[data-testid="stHeader"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Streamlit toolbar in header */
    [data-testid="stToolbar"] {
        background: transparent !important;
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🔥 CodePhoenix: gen-repair-execute")
st.caption("Running in **Daytona Workspace** | Powered by OpenAI, Galileo, Sentry & CodeRabbit")

# Validate config
try:
    config.validate_config()
except ValueError as e:
    st.error(f"Configuration Error: {e}")
    st.info("Please create a .env file with all required API keys. See .env.template for reference.")
    st.stop()

# Sidebar - Dashboard links
st.sidebar.header("📊 Sponsor Dashboards")
st.sidebar.markdown("Monitor the system in real-time:")
st.sidebar.markdown("- **Galileo**: LLM call traces & metrics")
st.sidebar.markdown("- **Sentry**: Error tracking & monitoring")
st.sidebar.markdown("- **Daytona**: Workspace & sandbox status")
st.sidebar.markdown("- **CodeRabbit**: AI code review (simulated)")

st.sidebar.divider()
st.sidebar.header("🎯 How It Works")
st.sidebar.markdown("""
1. **Generate**: LLM creates code from your prompt
2. **Execute**: Daytona runs code in sandbox
3. **Monitor**: Sentry catches any errors
4. **Fix**: CodeRabbit analyzes and fixes
5. **Retry**: Re-execute fixed code
""")

# Main interface
st.header("✍️ What code should I generate?")

user_prompt = st.text_area(
    "Enter your request:",
    placeholder="Example: Write a function that calculates fibonacci numbers up to n",
    height=100
)

col1, col2 = st.columns([1, 4])
with col1:
    generate_btn = st.button("🚀 Generate & Run", type="primary", use_container_width=True)

if generate_btn and user_prompt:
    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_{timestamp}.py"

    # STEP 1: Generate Code
    with st.status("Generating code with LLM...", expanded=True) as status:
        st.write("🔭 Galileo is monitoring this LLM call...")
        try:
            code = generate_code(user_prompt)
            st.code(code, language='python', line_numbers=True)
            status.update(label="✅ Code generated successfully!", state="complete")
        except Exception as e:
            st.error(f"Generation failed: {e}")
            st.stop()

    # STEP 2: Execute in Daytona
    with st.status("Executing code in Daytona sandbox...", expanded=True) as status:
        st.write("🟦 Running in isolated Daytona workspace...")
        success, output, error, error_type = execute_code(code, filename)

        # Display execution results based on error type
        if error_type == "success":
            st.success("✅ Execution successful!")
            st.write("**Output:**")
            if output.strip():
                st.code(output, language='text')
            else:
                st.info("(No output produced - code may only define functions/classes)")
            status.update(label="✅ Code executed successfully!", state="complete")

        elif error_type == "silent_failure":
            st.warning("⚠️ Code executed but produced no output!")
            st.write("**Issue:** The code ran without crashing but didn't print anything.")
            st.write("This might indicate a problem with the generated code.")
            status.update(label="⚠️ Silent failure detected - starting auto-fix...", state="error")

            # Report to Sentry
            st.write("🔴 Reporting silent failure to Sentry...")
            report_error(
                error_message=f"Silent failure: Code produced no output for prompt: {user_prompt[:100]}",
                error_type="silent_failure",
                context={
                    "user_prompt": user_prompt,
                    "generated_code": code[:500],
                    "output": output,
                    "error": error
                }
            )

        elif error_type == "handled_exception":
            st.warning("⚠️ Code handled an exception but may not be working correctly!")
            st.write("**Output/Error:**")
            st.code(output + error, language='text')
            st.write("Detected error patterns in output (e.g., 'Cannot divide by zero', exception handling)")
            status.update(label="⚠️ Handled exception detected - starting auto-fix...", state="error")

            # Report to Sentry
            st.write("🔴 Reporting handled exception to Sentry...")
            report_error(
                error_message=f"Handled exception detected: {(output + error)[:200]}",
                error_type="handled_exception",
                context={
                    "user_prompt": user_prompt,
                    "generated_code": code[:500],
                    "output": output[:500],
                    "error": error[:500]
                }
            )

        else:  # crash
            # STEP 3: Hard Crash Detected - Report to Sentry
            st.error("❌ Execution crashed!")
            st.write("**Error:**")
            st.code(error, language='text')
            status.update(label="❌ Execution failed - starting auto-fix...", state="error")

            # Report to Sentry
            st.write("🔴 Reporting crash to Sentry...")
            report_error(
                error_message=f"Code execution crashed: {error[:200]}",
                error_type="crash",
                context={
                    "user_prompt": user_prompt,
                    "generated_code": code[:500],
                    "error": error[:500]
                }
            )

        # Trigger auto-fix for ANY non-success error type
        needs_fix = error_type in ["silent_failure", "handled_exception", "crash"]

        if needs_fix:

            # STEP 4: Fix with CodeRabbit
            with st.status("CodeRabbit is analyzing and fixing...", expanded=True) as fix_status:
                st.write("🐰 AI code review in progress...")
                try:
                    # Create detailed error message for fixer
                    error_detail = error if error else f"Code produced no output. Type: {error_type}. Output: {output}"
                    fixed_code = fix_code(code, error_detail)
                    st.write("**Fixed Code:**")
                    st.code(fixed_code, language='python', line_numbers=True)
                    fix_status.update(label="✅ Code fixed by CodeRabbit!", state="complete")
                except Exception as e:
                    st.error(f"Fix generation failed: {e}")
                    st.stop()

            # STEP 5: Re-execute Fixed Code
            with st.status("Re-executing fixed code...", expanded=True) as retry_status:
                st.write("🟦 Running fixed code in Daytona...")
                fixed_filename = f"fixed_{timestamp}.py"
                success_retry, output_retry, error_retry, error_type_retry = execute_code(fixed_code, fixed_filename)

                if error_type_retry == "success":
                    st.balloons()
                    st.success("🎉 Fixed code executed successfully!")
                    st.write("**Output:**")
                    if output_retry.strip():
                        st.code(output_retry, language='text')
                    else:
                        st.info("(No output produced - code may only define functions/classes)")
                    retry_status.update(label="✅ Self-healing complete!", state="complete")
                else:
                    st.error(f"❌ Fixed code still has issues (type: {error_type_retry})")
                    if error_retry:
                        st.code(error_retry, language='text')
                    elif output_retry:
                        st.code(output_retry, language='text')
                    retry_status.update(label=f"❌ Fix attempt resulted in: {error_type_retry}", state="error")

    # Summary
    st.divider()
    st.success("✅ Process complete! Check the sponsor dashboards for detailed metrics.")

elif generate_btn:
    st.warning("Please enter a prompt first!")

# Footer
st.divider()
st.caption("Built for the Hackathon | Integrating: Daytona + Galileo + Sentry + CodeRabbit")
