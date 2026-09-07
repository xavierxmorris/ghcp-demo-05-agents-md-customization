---
agent: agent
description: Guided template for adding a new feature with tests and docs.
---

You are helping me add a new feature to this repo. Follow this checklist
exactly:

1. Restate the feature in one sentence and confirm scope with me before
   writing code.
2. Identify which area(s) of the codebase are affected (billing, analytics,
   shared). Read the relevant `.github/instructions/*.instructions.md` files
   and tell me which rules apply.
3. Sketch the public API (function signatures, types, errors) and wait for
   my approval.
4. Implement the feature in the smallest possible diff. Add `structlog`
   instrumentation if there's anything worth tracing.
5. Write `pytest` tests, including at least one edge case per code path.
6. Update the relevant README section.
7. Run `pytest -q` and `ruff check src tests` and report the result.

If at any step you're missing context, stop and ask — don't guess.
