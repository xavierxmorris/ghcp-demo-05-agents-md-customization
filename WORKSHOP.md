# Workshop: instructions as a testable team contract

**Audience:** developers and technical leads. **Time:** 60 minutes.
**Outcome:** a controlled instruction experiment, a correct Decimal implementation,
and evidence showing which conventions were actually followed.

## 1. Identify the mechanisms - 8 minutes

| Artifact | Purpose in this repository | How to evaluate it |
| --- | --- | --- |
| [AGENTS.md](AGENTS.md) | Operational charter and approval boundaries | Compare the agent's actions with allowed scope |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | Types, logging, errors, tests | Review generated code against explicit rules |
| [Billing instructions](.github/instructions/billing.instructions.md) | Decimal and HALF_EVEN in `src/billing/**` | Monetary boundary tests |
| [Analytics instructions](.github/instructions/analytics.instructions.md) | NumPy and empty-array handling | Scope-specific behavior |
| [Prompt files](.github/prompts/) | Manually invoked task templates | Confirm invocation and attached context |

As of **2026-09-07**, VS Code's documentation says custom instructions are
not used for inline suggestions, and applicable instruction files are combined
without a guaranteed order. Do this experiment in **Chat**, not by judging
ghost-text completions.

The source targets **Python 3.10+**. Follow the README setup and run:

```powershell
python -m pytest -q
```

The shipped baseline has one passing subtotal test, observed with Python 3.14.2
on 2026-09-07. `apply_tax_to_invoice` still raises `NotImplementedError`.
A green baseline therefore does not mean the exercise is already solved.

## 2. Make the comparison fair - 10 minutes

Create a new scratch directory and copy only `src`, `tests`, `requirements.txt`,
and `pytest.ini` into it. Open that directory as its own workspace, outside the
original repository's instruction tree. Keep the original checkout intact.

Use the same model, source snapshot, prompt, and task context in both trials.
Start a fresh chat for each. Personal/organization instructions may still apply;
record them as shared context rather than claiming the baseline is instruction-free.

```text
Implement apply_tax_to_invoice using the existing country tax rates.
Return the grand total after rounding once to two decimal places.
Do not change public types, dependency pins, or unrelated modules.
Show the relevant conventions and run the focused tests.
```

Trial A uses the scratch copy. Trial B uses the original workspace with
instructions. Inspect Chat customization diagnostics or references; in Copilot
CLI, `/instructions` and `/env` help inspect the loaded environment.

The code and docstrings already mention Decimal. A correct Trial A is not a
failed demo, and a different Trial B is not proof of universal improvement.
Repeat only if useful and record the observed results rather than promising
that an instruction file always changes the answer.

## 3. Score the output against independent criteria - 15 minutes

| Criterion | Evidence |
| --- | --- |
| Decimal throughout money calculations | No float conversion at input, arithmetic, or rounding |
| Country rates reused | Calls the existing `rate_for`; no duplicated tax table |
| Grand total rounded once | Boundary tests distinguish line rounding from total rounding |
| HALF_EVEN explicit | `quantize` uses the required rounding rule |
| Public API preserved | Existing `Invoice` and `LineItem` shapes unchanged |
| Dependencies unchanged | Diff contains no dependency edits |
| No library `print` | Diagnostics, if justified, follow the logging convention |

Ask for tests in `tests/test_invoices.py` before accepting a tax implementation.
Use Decimal values constructed from strings:

| Input | Expected result | Why |
| --- | --- | --- |
| Existing 21.48 subtotal, AU | 23.63 | Ordinary calculation |
| Empty invoice | 0.00 | Decimal identity and quantization |
| US item priced 0.005 | 0.00 | HALF_EVEN down to the even cent |
| US item priced 0.015 | 0.02 | HALF_EVEN up to the even cent |
| Three AU lines of 0.05 each | 0.16 | Round 0.165 once, not three separate 0.055 values |

The fractional-cent inputs deliberately exercise rounding; they are not a new
claim about what prices a production billing system permits.
`rate_for` currently maps unknown country codes to zero tax. Preserve or
explicitly discuss that existing rule; do not silently invent a new exception.

```powershell
python -m pytest -q tests\test_invoices.py
```

**Failure drill:** temporarily use per-line rounding. The three-line case must
distinguish 0.18 from the contract's 0.16. Restore the correct implementation.

## 4. Demonstrate path scope - 10 minutes

In [src/analytics/metrics.py](src/analytics/metrics.py), request
`percentile(values, p)`, using the existing NumPy dependency, linear interpolation,
and the subtree's empty-input convention.

```text
Identify the instructions applicable to src/analytics/metrics.py, then add
percentile(values, p). Specify the valid p range, empty-array behavior, and
return type before implementing. Use the existing NumPy dependency and tests.
Do not add NumPy to billing or change dependency pins.
```

Review the scope explanation as well as the output. "Use Decimal everywhere"
is not the rule; the billing scope is financial arithmetic, while analytics
has a different numeric contract.

If you deliberately create an instruction conflict, ask the agent to identify
it and stop before changing code. Resolve the conflicting documents; do not
turn a single stochastic result into a precedence rule.

## 5. Invoke a reusable review - 10 minutes

The prompt frontmatter uses `agent: ask` or `agent: agent`. In a supported
VS Code extension-host session, invoke `/pre-commit-review` with the changed
file attached, then try `/add-feature` for a small follow-on task.

Current Agent Host sessions do not use prompt files. In that surface, either
use a supported local session, paste the prompt body, or plan an explicit
conversion to a skill. A missing prompt-picker entry is not a Python bug.

The repository charter mentions Black and Ruff, but `requirements.txt` does
not install them. Report unavailable tooling honestly. Do not claim a clean
lint run or introduce extra dependencies merely to satisfy a narrative.

## 6. Debrief and deliverables - 7 minutes

Keep both prompts and diffs, loaded-instruction evidence, the scoring table,
and actual test output. Explain one rule whose enforcement belongs in code
or CI rather than in prose.

A useful extension is `.github/instructions/tests.instructions.md` with
`applyTo: "tests/**/*.py"` and rules for existing pytest fixtures. A generic
`tests/instructions.md` is not automatically a recognized instruction file.

## Troubleshooting and reset

| Symptom | First check |
| --- | --- |
| Both trials behave identically | Source conventions may already be sufficient |
| Billing rules seem absent | Workspace root, `applyTo`, loaded references, fresh session |
| NumPy appears in billing | Conflicting context or scope violation; review the diff |
| Prompt missing | Extension host versus Agent Host and prompt discovery |
| All tests green but tax still unimplemented | Only subtotal was covered |

Use fresh scratch copies for additional trials. Do not delete or move the
original instruction files, and do not clear unrelated personal configuration.

## Current sources

Checked **2026-09-07**:
[VS Code instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions),
[prompt files and Agent Host limits](https://code.visualstudio.com/docs/agent-customization/prompt-files),
[CLI instruction composition](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli).
Record your installed editor/CLI version; discovery support is surface-dependent.
