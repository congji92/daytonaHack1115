"""
Code Generator - Uses LLM to generate Python code from natural language

SIMPLICITY: Just a simple system prompt + OpenAI call + Galileo monitoring
No complex prompt engineering - keep it straightforward for hackathon demo
"""

import time
from typing import Tuple, Dict
from openai import OpenAI
from backend import config

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

# Initialize Galileo context (optional - with error handling)
GALILEO_ENABLED = False
try:
    from galileo import galileo_context

    # Initialize Galileo with project and log stream
    galileo_context.init(
        project="codephoenix_hackathon",
        log_stream="code_generation"
    )
    GALILEO_ENABLED = True
    print("[galileo] ✅ Galileo monitoring enabled (project: codephoenix_hackathon, stream: code_generation)")
except Exception as e:
    print(f"[galileo] ⚠️  Galileo initialization failed: {str(e)[:100]}")
    print("[galileo]    LLM monitoring will be disabled but code generation will continue")

def generate_code(user_prompt: str) -> Tuple[str, Dict]:
    """
    Generate Python code from a natural language prompt.

    Args:
        user_prompt: What the user wants the code to do

    Returns:
        Tuple of (generated_code: str, metrics: dict)
        metrics contains: model, tokens, latency_ms, estimated_cost
    """
    # Simple system prompt - no overthinking
    system_prompt = (
        "You are a Python expert. Write ONLY executable Python code. "
        "No markdown formatting, no explanations, no comments. "
        "Just pure Python code that can be run directly. "
        "If you need libraries, assume they are installed."
    )

    # Start timing
    start_time = time.time()

    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Calculate latency
    latency_ms = (time.time() - start_time) * 1000

    code = response.choices[0].message.content

    # Strip markdown if LLM added it despite instructions
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()

    # Extract performance metrics
    usage = response.usage
    metrics = {
        "model": "gpt-4o",
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
        "latency_ms": round(latency_ms, 2),
        # GPT-4o pricing: $2.50 per 1M input tokens, $10.00 per 1M output tokens
        "estimated_cost": round(
            (usage.prompt_tokens / 1_000_000 * 2.50) +
            (usage.completion_tokens / 1_000_000 * 10.00),
            4
        )
    }

    # Note: Galileo auto-instruments OpenAI when galileo_context.init() is called
    # No manual logging needed - traces are automatically captured!

    return code, metrics
