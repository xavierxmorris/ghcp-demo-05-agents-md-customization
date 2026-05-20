# AGENTS.md — Project Charter for AI Agents

This file is the ambient context for any AI agent operating in this repo
(GitHub Copilot CLI, Copilot coding agent, other agentic tools). Keep it
short and authoritative.

## Repository purpose
A small, opinionated **billing + analytics** library used by a fictional
SaaS company. Code quality and numerical correctness matter more than raw
performance.

## How to run things
- Install deps: `pip install -r requirements.txt`
- Run tests: `pytest -q`
- Format: `black src tests`
- Lint: `ruff check src tests`

## Definition of done (for any agent task)
1. `pytest -q` passes.
2. `ruff check` is clean.
3. New public functions have type hints and a docstring.
4. No new third-party dependencies without an explicit ADR note in the PR.

## Things agents must NOT do without explicit approval
- Modify any file under `migrations/` (we don't have one yet — if you create
  it, surface it).
- Change `requirements.txt` pins.
- Touch CI workflows under `.github/workflows/`.
- Commit secrets, API keys, or `.env` files.

## House style
- Python 3.10+ type hints everywhere.
- Functions over classes when state isn't required.
- `structlog` for logging — never `print` outside of CLIs.
- Errors are domain-specific exceptions in `src/<area>/errors.py`, not bare
  `Exception`.

## When in doubt
Stop and ask. A small clarifying question beats a 600-line PR that misses
the intent.
