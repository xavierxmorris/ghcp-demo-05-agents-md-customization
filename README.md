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

---

## What you'll learn
1. The four customisation surfaces and **when each takes effect**:
   - `AGENTS.md` — agentic context (CLI, coding agent, agents in general).
   - `.github/copilot-instructions.md` — repo-wide guidance for Chat & completions.
   - `.github/instructions/*.instructions.md` — **path-scoped** instructions
     (e.g., "in `src/billing/**`, always use Decimal not float").
   - `.github/prompts/*.prompt.md` — reusable Chat **prompt files** the team can
     invoke from the Chat picker.
2. The precedence order when these conflict.
3. A reproducible **before/after** experiment: same prompt, vastly different
   output once instructions are loaded.

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

> ⚠️ **Temporarily disable** the customisation files so you can see Copilot's
> default behaviour. Either rename `AGENTS.md` → `AGENTS.md.bak` and
> `.github/copilot-instructions.md` → `…bak`, or stash them.

Open `src/billing/invoices.py`. Highlight the empty `apply_tax_to_invoice`
function. In Chat:

```
/fix implement apply_tax_to_invoice — multiply each line item subtotal
by the tax rate from src/billing/tax.py and return the rounded grand total.
```

Note what you get: probably floats, `round(x, 2)`, no Decimal, maybe
`print()` for debug.

### Step 2 — Restore the instructions, re-run

Restore the renamed files. **Reload window** (Cmd+Shift+P → "Reload Window")
so Copilot picks them up.

Re-issue the *exact same prompt*. Now you should see:
- `Decimal` from the stdlib `decimal` module instead of `float`.
- `Decimal.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)`.
- `structlog` logger instead of `print`.
- A type-annotated signature matching the rest of the file.

🎯 **Lesson:** That delta is *free*. One markdown file taught Copilot your
billing standards in perpetuity.

### Step 3 — Path-scoped instructions

Open `src/analytics/metrics.py`. Ask Chat to add a `percentile(values, p)`
function. Watch it use **NumPy** — because `analytics.instructions.md` says
"in `src/analytics/**`, prefer NumPy and vectorised operations".

Now ask the same thing in `src/billing/invoices.py` (a place NumPy doesn't
belong). Copilot will use the stdlib `statistics` module instead — because
`billing.instructions.md` doesn't mention NumPy and the repo-wide rules
discourage adding dependencies.

🎯 **Lesson:** Path-scoped rules let you have *contradictory* conventions
that are correct for each part of your codebase.

### Step 4 — Prompt files

Open the Chat view. Click the `/` prompt picker. Your repo's prompt files
appear alongside the built-ins:

- `/add-feature` — guided template for adding a feature with tests + docs.
- `/pre-commit-review` — runs a structured self-review against your style.

Invoke `/pre-commit-review` on the function you just generated. It walks
through types, tests, error handling, and observability.

🎯 **Lesson:** Prompt files turn tribal "how we review code" knowledge into
a single click that every dev gets the same way.

### Step 5 — AGENTS.md for the CLI & coding agent

When you run the **Copilot CLI** (Demo 04) or assign an issue to the
**Copilot coding agent** (Demo 06) inside this repo, `AGENTS.md` is read
*first* as ambient context. Notice in this demo's `AGENTS.md` we tell agents:
- *Always run `pytest -q` before claiming a task is done.*
- *Never edit `migrations/` without explicit approval.*
- *Use `make fmt && make lint` for formatting.*

The CLI and coding agent will honour these without you re-stating them per
task.

---

## Precedence (when files conflict)

1. **The user's chat message** wins over instructions ("just this once,
   use float").
2. **Path-scoped instructions** beat repo-wide instructions for files inside
   the matched glob.
3. **`AGENTS.md`** governs agentic flows (CLI, coding agent) and is also a
   strong signal for Chat.
4. **Repo-wide `copilot-instructions.md`** is the default fallback.
5. **Personal `~/.vscode` settings** can layer on top for your own taste.

Conflicts are surfaced — Copilot Chat shows which instruction files were
applied at the top of each reply.

---

## Try it yourself

1. Add a `tests/instructions.md` mandating `pytest` (no `unittest`), `freezegun`
   for time, `factory_boy` for fixtures. Ask Copilot to write tests for
   `apply_tax_to_invoice`.
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
[Demo 06 — Coding Agent + Code Review](../ghcp-demo-06-coding-agent-and-review)
— the customisations from this demo are exactly what make the autonomous
coding agent produce PRs that match your conventions.
