---
agent: ask
description: Structured pre-commit self-review against this repo's conventions.
---

Review the currently open file (or the highlighted selection) against this
repo's conventions. Produce a short, blunt report with one section per
heading below. Skip a section if you have nothing useful to say.

### 1. Correctness
Bugs, off-by-ones, wrong rounding, missed edge cases.

### 2. Conventions
Violations of `.github/copilot-instructions.md` or the relevant
`.github/instructions/*.instructions.md` (cite the rule).

### 3. Types & errors
Missing / weak type hints; bare `Exception` / `ValueError` from public
APIs; lost stack traces.

### 4. Observability
Missing `structlog` calls where they'd help debug a production issue;
stray `print()`s.

### 5. Tests
Untested branches; missing parametrize cases; tests that assert on
implementation details instead of behaviour.

End with a one-line verdict: ✅ ship it / ⚠️ fix some things / ❌ not yet.
