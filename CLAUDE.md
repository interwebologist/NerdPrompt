# CLAUDE.md

NerdPrompt: terminal AI chat client with ANSI colors, emojis, ASCII dividers, syntax highlighting, and threading.

## Commands

```bash
# Setup
source .venv/bin/activate

# Run
./.venv/bin/python nerdprompt.py "question"
./.venv/bin/python nerdprompt.py  # interactive

# Lint
./.venv/bin/pylint nerdprompt.py
```

## Architecture

**PerplexityWrapper (45-167):** API communication, threading, markdown→ANSI conversion
**CodeProcesser (168-205):** Code extraction, Pygments highlighting, custom dividers
**ConfigEater (207-254):** YAML config loading, Cerberus validation, ANSI management

## Features

**Terminal:** ANSI colors (6 header levels), ASCII dividers, emoji bullets, text styling
**Code:** Pygments highlighting (40+ themes), custom dividers, auto language detection
**Threading:** Context retention, clear context option, follow-up questions

**Config:** `config.yaml` controls LLM settings, colors, ASCII art, prompts

**Dependencies:** openai, pygments, cerberus, python-dotenv, pyyaml

**Environment:** `.env` with `API_KEY=your_api_key_here`

## Documentation

**README Updates:**
- Update README.md for new features/options
- Add CLI flags to Options section
- Include usage examples for new workflows

## Git Guidelines

**Workflow:**
- Create branch for features/fixes when user requests changes
- Complete work with branch + PR creation

**File Management:**
- Use `git add` only for modified/relevant files, not `git add .`
- Use `trash` command instead of `rm` for file deletion

**Requirements:**
- No AI attribution in commits/PRs
- Standard commit format
- Concise messages

## AI Agent Notes

**Token Efficiency:**
- Minimal tokens in CLAUDE.md while preserving logic
- Concise technical language only
- Essential info for code maintenance