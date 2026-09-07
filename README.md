# Demo 05 — Customising Copilot with AGENTS.md 🎛️

> **Difficulty:** ⭐⭐⭐⭐
> **GHCP surfaces:** Repository-level customisation:
> `AGENTS.md`, `.github/copilot-instructions.md`, **path-scoped** instructions,
> **prompt files** (reusable Chat templates).
> **Stack:** Python (FastAPI-ish billing service, no framework dependency)
> **Time:** ~30–45 minutes

By default Copilot follows generic conventions. In real repos that means it
keeps writing `print()` when you want `structlog`, uses `unittest` when you
mandate `pytest`, or formats dates as ISO when your codebase uses epoch
millis. This demo shows how to **teach Copilot your project's rules** so
suggestions land *inside* your conventions on the first try.

**Go deeper:** [WORKSHOP.md](WORKSHOP.md) provides a controlled comparison,
Decimal rounding cases, an instruction-discovery check, and a reusable review
rubric. Instructions improve context; they do not guarantee compliance.

---

## What you'll learn
1. The four customisation surfaces and **when each takes effect**:
   - `AGENTS.md` — agentic context (CLI, coding agent, agents in general).
   - `.github/copilot-instructions.md` — repo-wide guidance for Chat, not
     VS Code inline completions.
   - `.github/instructions/*.instructions.md` — **path-scoped** instructions
     (e.g., "in `src/billing/**`, always use Decimal not float").
   - `.github/prompts/*.prompt.md` — reusable Chat **prompt files** the team can
     invoke from the Chat picker.
2. How to confirm which instructions were loaded and remove conflicting rules.
3. A **before/after** experiment: same task and model, with instruction context
   as the variable. The output difference is measured, not guaranteed.

## Prerequisites
- VS Code + Copilot + Copilot Chat.
- Python 3.10+ (for the optional "run the tests" step).

## Setup
```bash
git clone https://github.com/xavierxmorris/ghcp-demo-05-agents-md-customization.git
cd ghcp-demo-05-agents-md-customization
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest    # baseline tests pass
```

---

## Layout

```
.
├── AGENTS.md                                   # agentic context (CLI / coding agent)
├── .github/
│   ├── copilot-instructions.md                 # repo-wide style + library rules
│   ├── instructions/
│   │   ├── billing.instructions.md             # path-scoped: src/billing/**
│   │   └── analytics.instructions.md           # path-scoped: src/analytics/**
│   └── prompts/
│       ├── add-feature.prompt.md
│       └── pre-commit-review.prompt.md
└── src/
    ├── billing/
    │   ├── invoices.py
    │   └── tax.py
    └── analytics/
        └── metrics.py
```

---

## Walkthrough

### Step 1 — The "before" experiment

> Use a separate scratch copy containing only `src/`, `tests/`,
> `requirements.txt`, and `pytest.ini`, opened as its own workspace. Do not
> rename or stash the original instructions. Disabling only the two root
> files leaves path-scoped billing instructions active and is not a clean
> comparison. See the workshop for the remaining controls.

Open `src/billing/invoices.py`. Highlight the empty `apply_tax_to_invoice`
function. In Chat:

```
/fix implement apply_tax_to_invoice — multiply each line item subtotal
by the tax rate from src/billing/tax.py and return the rounded grand total.
```

Record what you actually get. The source already uses Decimal and describes
rounding, so an instruction-free trial may still follow those conventions.

### Step 2 — Restore the instructions, re-run

Return to the original repository with its instructions intact. Start a new
chat with the same model and task. Inspect the loaded instruction references
or customization diagnostics; reload the window if discovery appears stale.

Re-issue the *exact same prompt*. Now you should see:
- `Decimal` from the stdlib `decimal` module instead of `float`.
- `Decimal.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)`.
- `structlog` logger instead of `print`.
- A type-annotated signature matching the rest of the file.

🎯 **Lesson:** Versioned instructions make expectations reusable. Their effect
must still be checked against the diff and tests.

### Step 3 — Path-scoped instructions

Open `src/analytics/metrics.py`. Ask Chat to add a `percentile(values, p)`
function. Watch it use **NumPy** — because `analytics.instructions.md` says
"in `src/analytics/**`, prefer NumPy and vectorised operations".

Now ask the same thing in `src/billing/invoices.py` (a place NumPy doesn't
belong). Copilot will use the stdlib `statistics` module instead — because
`billing.instructions.md` doesn't mention NumPy and the repo-wide rules
discourage adding dependencies.

🎯 **Lesson:** Path-scoped rules let you have *contradictory* conventions
that are correct for each part of your codebase. Express the scopes clearly
rather than relying on contradictory instructions to resolve predictably.

### Step 4 — Prompt files

In a supported **VS Code extension-host** chat session, open the `/` picker.
Your repo's prompt files
appear alongside the built-ins:

- `/add-feature` — guided template for adding a feature with tests + docs.
- `/pre-commit-review` — runs a structured self-review against your style.

Invoke `/pre-commit-review` on the function you just generated. It walks
through types, tests, error handling, and observability.

🎯 **Lesson:** Prompt files turn tribal "how we review code" knowledge into
a single click that every dev gets the same way.

Current Agent Host sessions do not use prompt files. Use a supported local
chat session, paste the prompt body with the relevant files attached, or
explicitly migrate the workflow to a skill. See the dated sources in the workshop.

### Step 5 — AGENTS.md for the CLI & coding agent

When you run the **Copilot CLI** (Demo 04) or assign an issue to the
**Copilot coding agent** (Demo 06) inside this repo, `AGENTS.md` supplies
repository context. Notice in this demo's `AGENTS.md` we tell agents:
- *Always run `pytest -q` before claiming a task is done.*
- *Never edit `migrations/` without explicit approval.*
- *Use `black src tests` and `ruff check src tests` for formatting/linting.*

These commands describe the charter's expectations; Black and Ruff are not
installed by this starter's `requirements.txt`. Do not claim they ran without
checking availability. The shipped baseline is the pytest subtotal test.

---

## Composition, not a universal precedence ladder

As checked on **7 September 2026**, VS Code combines applicable instruction
files without guaranteeing an order; Copilot CLI also combines applicable
instructions rather than using a fallback chain. Discovery and nested-file
support vary by surface and settings. Remove contradictions, inspect which
files loaded, and use tests for rules that must hold. A prompt is not a way
to override organization policy or turn a financial invariant into a suggestion.

---

## Try it yourself

1. Add `.github/instructions/tests.instructions.md` with
   `applyTo: "tests/**/*.py"`, mandating pytest and its existing fixtures.
   Ask Copilot to write tests for `apply_tax_to_invoice`; no new dependencies.
2. Add a `.github/prompts/release-notes.prompt.md` that drafts release notes
   from `git log`. Invoke it.
3. Stress-test by **intentionally** conflicting instructions — what wins?
4. Move `AGENTS.md` into a subdirectory (`src/billing/AGENTS.md`) and observe
   that it now only applies inside that subtree.

## Talking points
- This is the **single highest-ROI** investment you can make in Copilot
  quality at a team / org level. It compounds across every dev, forever.
- Keep instructions **short, declarative, and testable** — "use Decimal in
  billing" is great; "write good code" is useless.
- Commit them. Code-review them. **They are infrastructure**, not config.
- Pair this demo with your linter config — when both agree, Copilot
  *and* CI enforce the same rules.

## Next demo →
[Demo 06 — Coding Agent + Code Review](https://github.com/xavierxmorris/ghcp-demo-06-coding-agent-and-review)
— the customisations from this demo are exactly what make the autonomous
coding agent produce PRs that match your conventions.
