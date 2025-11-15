"""
Code Fixer - Simulates CodeRabbit code review to fix errors

SIMPLICITY: Just send broken code + error to LLM with "fix this" prompt
Simulates CodeRabbit's AI code review capabilities
"""

from openai import OpenAI
from backend import config

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

# Initialize Galileo observer (optional - track fix generation)
GALILEO_ENABLED = False
galileo_workflows = None
try:
    from galileo_observe import Workflows
    galileo_workflows = Workflows()
    GALILEO_ENABLED = True
except Exception:
    pass  # Galileo already warned in generator.py

def fix_code(broken_code: str, error_message: str) -> str:
    """
    Fix broken code using AI code review (simulating CodeRabbit).

    Args:
        broken_code: The code that failed
        error_message: The error message from execution

    Returns:
        Fixed Python code
    """
    # Detect error type from message
    is_silent_failure = "no output" in error_message.lower() or "silent_failure" in error_message.lower()
    is_handled_exception = "handled exception" in error_message.lower() or "cannot divide by zero" in error_message.lower()

    # CodeRabbit-style review prompt with specific instructions based on error type
    if is_silent_failure:
        fix_prompt = f"""You are CodeRabbit, an AI code reviewer.

The following Python code executed successfully but produced NO OUTPUT:

```python
{broken_code}
```

Issue:
```
{error_message}
```

The code ran without errors but didn't print anything. This is a SILENT FAILURE.

Your task:
1. Fix any logical errors in the code
2. MOST IMPORTANTLY: Add print() statements to display results to the user
3. The code must produce visible output when executed as a script

Remember: In Python scripts, just writing a variable name (like `result`) doesn't print it.
You MUST use print() to show output.

Output ONLY the corrected Python code with print statements, no explanations or markdown.
"""
    elif is_handled_exception:
        fix_prompt = f"""You are CodeRabbit, an AI code reviewer.

The following Python code handled an exception but may not be working correctly:

```python
{broken_code}
```

Issue detected:
```
{error_message}
```

The code caught an exception (likely with try-except) but this indicates a logic error.

Your task:
1. Fix the underlying logic error (e.g., avoid division by zero instead of catching it)
2. Ensure the code produces the expected results
3. Add print() statements to display results

Output ONLY the corrected Python code, no explanations or markdown.
"""
    else:
        # Standard crash
        fix_prompt = f"""You are CodeRabbit, an AI code reviewer.

The following Python code crashed:

```python
{broken_code}
```

Error:
```
{error_message}
```

Analyze the error and provide a fixed version of the code.
Make sure the fixed code prints its results using print().

Output ONLY the corrected Python code, no explanations or markdown.
"""

    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": fix_prompt}]
    )

    fixed_code = response.choices[0].message.content

    # Strip markdown if present
    if "```python" in fixed_code:
        fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()
    elif "```" in fixed_code:
        fixed_code = fixed_code.split("```")[1].split("```")[0].strip()

    # Log to Galileo if enabled
    if GALILEO_ENABLED and galileo_workflows:
        try:
            from galileo_observe import Message, MessageRole
            galileo_workflows.add_llm_step(
                name="code_fixing",
                input=Message(role=MessageRole.user, content=fix_prompt),
                output=Message(role=MessageRole.assistant, content=fixed_code),
                model="gpt-4o"
            )
        except Exception as e:
            print(f"[galileo] Warning: Failed to log fix generation: {e}")

    return fixed_code
