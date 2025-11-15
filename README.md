# CodePhoenix 🔥

**Self-Healing Code Generator** - Automatically generates, executes, and fixes Python code using AI.

## Quick Start

1. **Setup**:
   ```bash
   # Activate environment
   conda activate daytonaHack1115

   # Install dependencies
   pip install -r requirements.txt

   # Create .env from template
   cp .env.template .env
   # Edit .env and add your API keys
   ```

2. **Run**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Use**:
   - Enter a prompt: "Write a function that calculates fibonacci numbers"
   - Click "Generate & Run"
   - Watch it generate, execute, auto-fix (if needed), and succeed!

## What It Does

```
User Prompt → [Generate Code] → [Execute in Daytona] → Success ✅
                                          ↓ Error
                                    [Sentry Logs]
                                          ↓
                                 [CodeRabbit Fixes]
                                          ↓
                                    [Re-execute] → Success ✅
```

## Sponsor Integration

- **Daytona** 🟦: Executes code in isolated sandboxes
- **Galileo** 🔭: Monitors all LLM calls and metrics
- **Sentry** 🔴: Tracks errors and failures
- **CodeRabbit** 🐰: AI code review for auto-fixing

## Architecture

Ultra-simple: **~200 lines of code**

- `backend/generator.py` - LLM code generation (+ Galileo)
- `backend/executor.py` - Daytona sandbox execution
- `backend/fixer.py` - AI-powered code fixing (+ Galileo)
- `backend/sentry_helper.py` - Error tracking
- `streamlit_app.py` - UI orchestration

## Documentation

See [instructions.md](instructions.md) for:
- Complete setup guide
- Sponsor integration details
- Reused patterns from claudeTutorial
- Demo script for presentation
- Example use cases

## Philosophy

**Simple system prompt + Simple service orchestration = Powerful demo**

No complex logic. Just wire the sponsors together and let them do what they do best.

Built in under 2 hours for a hackathon. Focused on showcasing integrations, not over-engineering.

---

**License**: MIT | **Built for**: Hackathon Demo
