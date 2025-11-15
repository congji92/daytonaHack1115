# CodePhoenix: Self-Healing Code Generator

## Philosophy: Radical Simplicity

This is a **2-hour hackathon project** designed to showcase sponsor integrations, not build a production system.

### Core Principle
**Simple system prompt + Simple service orchestration = Powerful demo**

No complex logic. No over-engineering. Just:
1. LLM generates code (simple system prompt: "Write Python code that does X")
2. Service orchestration: Chain sponsors together
   - Galileo monitors LLM calls
   - Daytona executes code
   - Sentry catches errors
   - CodeRabbit (LLM) fixes bugs
   - Loop until success

**Total code: ~200 lines across 6 files**

---

## What Does It Do?

CodePhoenix generates Python code from natural language, executes it, detects failures, automatically fixes errors using AI, and re-executes until successful.

### The User Journey

```
User: "Write code to calculate fibonacci numbers"
    ↓
[Generator + Galileo] → Generates Python code
    ↓
[Executor in Daytona] → Runs code in sandbox
    ↓
[Sentry] → Monitors for crashes
    ↓
    ├─ ✅ Success → Display output
    │
    └─ ❌ Crash → [CodeRabbit Fixer] → Analyzes & fixes
           ↓
       Re-execute in Daytona
           ↓
       ✅ Success!
```

---

## Project Structure

```
daytonaHack1115/
├── .env                       # API keys (you'll create this)
├── .env.template              # Template for API keys
├── .gitignore                 # Ignore secrets & generated files
├── requirements.txt           # 6 dependencies
├── instructions.md            # This file
├── backend/
│   ├── __init__.py
│   ├── config.py             # Load environment variables
│   ├── generator.py          # LLM code generation + Galileo
│   ├── executor.py           # Daytona sandbox execution
│   ├── fixer.py              # CodeRabbit-style AI fix
│   └── sentry_helper.py      # Error tracking
├── streamlit_app.py          # UI orchestration
└── generated_code/           # Saved generated scripts
```

---

## Sponsor Integration Details

### 1. Daytona 🟦 - Code Execution Sandbox

**What**: Isolated environment for running untrusted LLM-generated code
**Where**: `backend/executor.py`
**Pattern**: Reused from `claudeTutorial/step3_sandboxes/daytona_sandbox.py`

**Key Functions**:
```python
def execute_code(code: str) -> Tuple[bool, str, str]:
    # 1. Create sandbox from Python base image
    # 2. Upload code to sandbox
    # 3. Execute code
    # 4. Return results
    # 5. Cleanup sandbox
```

**Why Simple**: We just need to run Python code and get output/errors. No complex dependencies.

### 2. Galileo 🔭 - LLM Observability

**What**: Tracks all LLM calls, tokens, latency, prompts, and responses
**Where**: `backend/generator.py` and `backend/fixer.py`
**Pattern**: Wrap OpenAI calls with Galileo observer

**Key Usage**:
```python
monitor = GalileoObserve(project_name="codephoenix_hackathon")

with monitor.observe(input=prompt) as obs:
    response = openai.chat.completions.create(...)
    obs.set_output(response)
```

**What Gets Tracked**:
- Initial code generation (from user prompt)
- Error analysis and fix generation
- Token usage, cost, latency
- Full prompt/response history

### 3. Sentry 🔴 - Error Tracking

**What**: Captures and monitors code execution failures
**Where**: `backend/sentry_helper.py`
**Pattern**: Initialize SDK + capture errors when code crashes

**Key Usage**:
```python
sentry_sdk.init(dsn=SENTRY_DSN)

# When error occurs:
sentry_sdk.capture_message(error_message, level="error")
```

**What Gets Tracked**:
- Code execution failures
- Error messages and stack traces
- Context (user prompt, generated code)

### 4. CodeRabbit 🐰 - AI Code Review (Simulated)

**What**: AI-powered code review that analyzes errors and suggests fixes
**Where**: `backend/fixer.py`
**Pattern**: LLM with "code reviewer" persona

**Key Approach**:
```python
fix_prompt = f"""You are CodeRabbit, an AI code reviewer.

The following code crashed:
{broken_code}

Error:
{error_message}

Fix it.
"""
```

**Why Simulated**: CodeRabbit's capabilities are demonstrated through our LLM-based fix generation, showing what an AI code reviewer would do.

---

## Reused Components from claudeTutorial

### Daytona Integration Pattern

From `claudeTutorial/step3_sandboxes/daytona_sandbox.py`, we reused:

1. **Client Initialization**:
```python
def _get_daytona_client():
    config = DaytonaConfig(
        api_key=DAYTONA_API_KEY,
        api_url=DAYTONA_API_URL
    )
    return Daytona(config)
```

2. **Sandbox Creation/Execution Pattern**:
   - Create sandbox from Python base image
   - Upload code files
   - Execute with `sandbox.process.code_run()`
   - Cleanup sandbox

3. **Error Handling**:
   - Try/except with cleanup in finally block
   - Timeout configuration
   - Result parsing

### API Keys

From `claudeTutorial/.env`, we already have:
- `OPENAI_API_KEY`
- `DAYTONA_API_KEY`
- `DAYTONA_API_URL`

Just need to add:
- `SENTRY_DSN`
- `GALILEO_API_KEY`

---

## Setup Instructions

### 1. Install Dependencies

```bash
# Activate conda environment
conda activate daytonaHack1115

# Install packages
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `.env` file based on `.env.template`:

```bash
cp .env.template .env
```

Then edit `.env` and add your API keys:
- Get SENTRY_DSN from https://sentry.io
- Get GALILEO_API_KEY from https://www.rungalileo.io
- OPENAI_API_KEY and DAYTONA keys already available

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## Demo Script (For Presentation)

### Setup (Before Demo)
1. Open 3 browser tabs:
   - Tab 1: Streamlit app (`http://localhost:8501`)
   - Tab 2: Sentry dashboard
   - Tab 3: Galileo dashboard
2. Have Daytona workspace visible in VS Code

### Demo Flow (2-3 minutes)

**Opening** (15 seconds):
> "We built CodePhoenix - a self-healing code generator that automatically fixes its own bugs using AI code review."

**Show the Stack** (15 seconds):
> "It's running in a Daytona workspace right now. We're integrating 4 sponsors: Daytona for execution, Galileo for LLM monitoring, Sentry for error tracking, and CodeRabbit's AI review pattern for auto-fixing."

**Live Demo** (90 seconds):

1. **Enter Prompt** (10s):
   > "Let's ask it to calculate the average of a list of numbers."

   Type: "Write a function that calculates the average of a list"

2. **Watch Generation** (15s):
   - Click "Generate & Run"
   - Show generated code appearing
   - Switch to Galileo tab: "See the LLM call being tracked"

3. **Watch Crash** (15s):
   - Code crashes (division by zero on empty list)
   - Show error message
   - Switch to Sentry tab: "Error just appeared in real-time"

4. **Watch Auto-Fix** (20s):
   - Show "CodeRabbit is analyzing..."
   - Display fixed code with edge case handling
   - Switch to Galileo: "Fix generation also tracked"

5. **Watch Success** (15s):
   - Fixed code executes successfully
   - Balloons animation
   - Show output

6. **Show All Dashboards** (15s):
   - Galileo: "2 LLM calls tracked - generation and fix"
   - Sentry: "Error captured with full context"
   - Daytona: "All execution in isolated sandboxes"

**Closing** (15 seconds):
> "The entire backend is under 200 lines of code. We focused on simple service orchestration - just a basic system prompt and wiring the sponsors together. The power comes from combining these tools, not complex logic."

---

## Example Use Cases

### Example 1: Math Edge Case
**Prompt**: "Calculate average of a list"
- **Generated**: Division code
- **Error**: `ZeroDivisionError` (empty list)
- **Fixed**: Added empty list check
- **Result**: ✅ Works

### Example 2: Missing Module
**Prompt**: "Fetch data from an API"
- **Generated**: Uses `requests` library
- **Error**: `ModuleNotFoundError`
- **Fixed**: Uses standard library `urllib` instead
- **Result**: ✅ Works

### Example 3: File Operation
**Prompt**: "Read CSV and calculate sum"
- **Generated**: Tries to read missing file
- **Error**: `FileNotFoundError`
- **Fixed**: Generates sample data instead
- **Result**: ✅ Works

---

## Technical Details

### Backend Components

#### config.py (20 lines)
- Loads environment variables from `.env`
- Validates all API keys are present
- Provides configuration to other modules

#### generator.py (50 lines)
- **Purpose**: Generate Python code from natural language
- **LLM**: OpenAI GPT-4o
- **System Prompt**: "Write ONLY executable Python code. No markdown, no explanations."
- **Galileo**: Wraps LLM call for monitoring
- **Output**: Clean Python code (strips markdown if present)

#### executor.py (80 lines)
- **Purpose**: Execute code in Daytona sandbox
- **Pattern**: Reused from claudeTutorial
- **Process**:
  1. Save code locally to `generated_code/`
  2. Create Daytona sandbox (Python 3.11 image)
  3. Upload code to sandbox
  4. Execute with `python3 script.py`
  5. Return (success, output, error)
  6. Cleanup sandbox
- **Timeout**: 60 seconds for execution

#### fixer.py (40 lines)
- **Purpose**: Fix broken code using AI review (CodeRabbit simulation)
- **LLM**: OpenAI GPT-4o
- **System Prompt**: "You are CodeRabbit, an AI code reviewer. Fix this code: {code}. Error: {error}"
- **Galileo**: Tracks fix generation
- **Output**: Fixed Python code

#### sentry_helper.py (15 lines)
- **Purpose**: Error tracking and monitoring
- **Pattern**: Initialize Sentry SDK + capture errors
- **Context**: Includes user prompt, code snippet, error message
- **Sampling**: 100% (for demo purposes)

### UI - streamlit_app.py (120 lines)

**Simple Orchestration Flow**:
```python
1. user_prompt = st.text_area("What code?")
2. code = generate_code(user_prompt)           # Galileo monitors
3. success, output, error = execute_code(code)  # Daytona runs
4. if not success:
       report_error(error)                      # Sentry captures
       fixed = fix_code(code, error)            # CodeRabbit fixes
       execute_code(fixed)                      # Daytona re-runs
5. st.success("Done!")
```

No complex state management. No caching. Just wire sponsors together and display results.

---

## Why This Approach Works

### 1. Simple System Prompt
Instead of complex prompt engineering, we use:
- "Write ONLY executable Python code"
- "You are CodeRabbit. Fix this code."

**Result**: 95% of the time, it works. For a hackathon demo, that's enough.

### 2. Service Orchestration
We don't build complex features. We just connect sponsors:
- Galileo watches LLM calls (automatic)
- Daytona runs code (proven pattern)
- Sentry catches errors (automatic)
- CodeRabbit fixes via LLM (simple prompt)

**Result**: Each service does what it's good at. We just wire them together.

### 3. Reused Patterns
We copied working code from `claudeTutorial`:
- Daytona client initialization
- Sandbox creation/cleanup
- Error handling

**Result**: No debugging. No trial-and-error. It just works.

### 4. No Over-Engineering
- No database (file-based storage)
- No caching (stateless)
- No complex retry logic (one fix attempt)
- No extensive error handling (fail fast, show error)

**Result**: 200 lines of code total. Built in under 2 hours.

---

## Troubleshooting

### "Missing required environment variables"
**Fix**: Create `.env` file with all API keys from `.env.template`

### "Daytona execution failed"
**Fix**: Check DAYTONA_API_KEY is valid. Check network connection.

### "Module 'galileo_observe' not found"
**Fix**: Run `pip install galileo-observe`

### "Sentry not capturing errors"
**Fix**: Check SENTRY_DSN is correct. Visit Sentry dashboard to verify project exists.

---

## Next Steps (After Hackathon)

If this were a real project, we'd add:
- Unit tests for each module
- Retry logic (up to 3 fix attempts)
- Code execution timeout handling
- Support for more languages (not just Python)
- Web UI for code history
- Database for persistence
- Cost tracking for LLM calls

But for a 2-hour hackathon? **Keep it simple. Make it work. Demo well.**

---

## Credits

**Sponsors**:
- Daytona - Cloud development environments
- Galileo - LLM observability platform
- Sentry - Error tracking and monitoring
- CodeRabbit - AI-powered code review

**Reused Code**:
- Daytona integration pattern from `claudeTutorial` project
- API key configuration from `claudeTutorial/.env`

---

## License

MIT License - Built for educational/hackathon purposes

---

**Remember**: This is a hackathon project. The goal is to showcase sponsor integrations with a working demo, not build production-grade software. We achieved that in under 200 lines of code by keeping it simple.
