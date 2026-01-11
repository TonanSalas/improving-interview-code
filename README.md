# AI Skills Coding Interview

A pair programming exercise to evaluate AI-assisted development skills for senior/architect candidates.

## Overview

- **Duration**: 20-30 minutes
- **Format**: Pair programming with interviewer observing
- **AI Tools**: Use any AI assistant (Claude, ChatGPT, Copilot, Cursor, etc.)
- **Explain your thinking**: Brief explanations at key decision points

## Your Tasks

Choose your own order. Touch all 4 areas; depth over completion.

| Task | Goal |
|------|------|
| **Understand** | Use AI to explain how the quoting system works |
| **Refactor** | Use AI to identify and fix code quality issues |
| **Debug** | A discount is being applied incorrectly - find and fix it |
| **Extend** | Add a new "Comprehensive" coverage type following existing patterns |

## Getting Started

```bash
# Run the quote engine
python main.py

# Run tests
pytest test_quote.py -v
```

## What We're Evaluating

- **Context generation** - Can you get AI to explain unfamiliar code accurately?
- **Refactoring judgment** - Do you identify the right things to fix?
- **Pattern recognition** - Do you extend existing patterns vs. hack solutions?
- **Prompt iteration** - Do you refine prompts when AI gives incomplete answers?
- **Verification** - Do you validate AI suggestions before applying them?

## Project Structure

```
├── models.py          # Data classes (Customer, Vehicle, QuoteRequest, etc.)
├── quote_engine.py    # Core quoting logic with coverage calculators
├── main.py            # Entry point - runs a sample quote
└── test_quote.py      # Basic test suite
```
