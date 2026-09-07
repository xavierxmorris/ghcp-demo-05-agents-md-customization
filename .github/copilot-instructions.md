# Copilot Instructions — repo-wide

These rules provide repository-wide Copilot Chat guidance. Applicable
`.github/instructions/*.instructions.md` files add path-specific guidance.
Keep the files consistent rather than relying on an ordering guarantee.
VS Code inline completions do not use these custom instructions.

## Language & version
- Python 3.10+. Use modern syntax (`|` union types, `match` where it reads
  cleanly, walrus `:=` sparingly).

## Style
- Format with `black`. Lint with `ruff`.
- Type hints on every public function. Prefer `from __future__ import annotations`
  at the top of new modules.
- 100-char soft line limit (not a hard cap — readability wins).

## Logging
- Use `structlog`. Get a logger with `log = structlog.get_logger(__name__)`.
- **Never** use `print()` in library code. CLI entry points can use `print`
  for user-facing output.

## Errors
- Define domain exceptions in `src/<area>/errors.py`.
- Never raise bare `Exception` or `ValueError` from public APIs.

## Testing
- `pytest` only — no `unittest`.
- One assert per test where reasonable; many small tests beats one big one.
- Use `pytest.mark.parametrize` for table-driven tests.
- Fixtures live in `tests/conftest.py`.

## Dependencies
- Stdlib-first. Don't add a dependency without an obvious win.
- If you must, add it to `requirements.txt` AND note why in the PR description.

## Documentation
- Google-style docstrings (`Args:`, `Returns:`, `Raises:`).
- Update the relevant section of the README when adding user-visible features.
