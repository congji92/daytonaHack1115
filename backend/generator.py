"""
Code Generator - Uses LLM to generate Python code from natural language

SIMPLICITY: Just a simple system prompt + OpenAI call + Galileo monitoring
No complex prompt engineering - keep it straightforward for hackathon demo
"""

from openai import OpenAI
from backend import config

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

# Initialize Galileo observer (optional - with error handling)
GALILEO_ENABLED = False
galileo_workflows = None
try:
    from galileo_observe import Workflows
    galileo_workflows = Workflows()
    # Create a workflow for logging
    galileo_workflows.add_workflow(name="codephoenix_workflow", project_name="codephoenix_hackathon")
    GALILEO_ENABLED = True
    print("[galileo] ✅ Galileo monitoring enabled")
except Exception as e:
    print(f"[galileo] ⚠️  Galileo initialization failed: {str(e)[:100]}")
    print("[galileo]    LLM monitoring will be disabled but code generation will continue")

def generate_code(user_prompt: str) -> str:
    """
    Generate Python code from a natural language prompt.

    Args:
        user_prompt: What the user wants the code to do

    Returns:
        Generated Python code as a string
    """
    # Simple system prompt - no overthinking
    system_prompt = (
        "You are a Python expert. Write ONLY executable Python code. "
        "No markdown formatting, no explanations, no comments. "
        "Just pure Python code that can be run directly. "
        "If you need libraries, assume they are installed."
    )

    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    code = response.choices[0].message.content

    # Strip markdown if LLM added it despite instructions
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()

    # Log to Galileo if enabled
    if GALILEO_ENABLED and galileo_workflows:
        try:
            from galileo_observe import Message, MessageRole
            galileo_workflows.add_llm_step(
                name="code_generation",
                input=[
                    Message(role=MessageRole.system, content=system_prompt),
                    Message(role=MessageRole.user, content=user_prompt)
                ],
                output=Message(role=MessageRole.assistant, content=code),
                model="gpt-4o"
            )
        except Exception as e:
            print(f"[galileo] Warning: Failed to log LLM call: {e}")

    return code
