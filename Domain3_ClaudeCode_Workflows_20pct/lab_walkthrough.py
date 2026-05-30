"""
Domain 3 — Claude Code Configuration & Workflows (20% of the cert)
===================================================================
A SINGLE step-by-step walkthrough that touches every Domain 3 sub-topic.

Run with:
    python Domain3_ClaudeCode_Workflows_20pct/lab_walkthrough.py

STEPS:
    STEP 1 — Build a project-level CLAUDE.md (Lab 3.1).
    STEP 2 — Conditional rules via .claude/rules/ (Lab 3.2).
    STEP 3 — Create a project slash-command / skill (Lab 3.3).
    STEP 4 — Plan mode vs direct execution (Lab 3.4).
    STEP 5 — Run Claude Code headlessly in CI (Lab 3.5).
    STEP 6 — Match each workload to the right Anthropic API (Lab 3.6).
    STEP 7 — Personal override of a team skill (Lab 3.7).
    STEP 8 — Session control: --resume / --continue / fresh (Lab 3.8).

This file is mostly NETWORK-FREE — it WRITES sample config files into a
demo_workspace/ subfolder so you can see exactly what each artifact looks like.
"""

from __future__ import annotations
from pathlib import Path
import textwrap

DEMO = Path(__file__).parent / "demo_workspace"
DEMO.mkdir(exist_ok=True)


def banner(step: int, title: str) -> None:
    print(f"\n{'=' * 70}\n=== STEP {step}: {title}\n{'=' * 70}")


def write(rel_path: str, content: str) -> Path:
    p = DEMO / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print(f"  wrote: {p.relative_to(DEMO.parent)}")
    return p


# ---------------------------------------------------------------------------
# STEP 1 — CLAUDE.md (project-level memory) (Lab 3.1)
# ---------------------------------------------------------------------------
banner(1, "Project-level CLAUDE.md (Lab 3.1)")
write("CLAUDE.md", """
    # Project: payments-api

    ## Conventions
    - Python 3.11. Use `uv` for venv + installs.
    - Async with `httpx`, never `requests`.
    - All public functions need type hints AND a one-line docstring.

    ## Testing
    - `pytest -q` to run tests.
    - New code without a test should fail review.

    ## Things NOT to do
    - Do NOT bump dependency versions in the same PR as a feature change.
    - Do NOT add print() in library code; use logging.
""")
print("""
HOW IT GETS LOADED:
  - Claude Code reads CLAUDE.md from the cwd at session start.
  - Sub-folder CLAUDE.md files extend (not replace) the root one.
  - User-level memory ~/.claude/CLAUDE.md is layered ABOVE the project file.
""")


# ---------------------------------------------------------------------------
# STEP 2 — Conditional rules in .claude/rules/ (Lab 3.2)
# ---------------------------------------------------------------------------
banner(2, "Conditional rules via .claude/rules/ (Lab 3.2)")
write(".claude/rules/python-pep8.md", """
    # When editing Python files
    Apply only when the changed file matches `*.py`.

    - Lines <= 100 cols (black default).
    - Use f-strings; never .format() or %.
    - Imports sorted: stdlib, third-party, local.
""")
write(".claude/rules/sql-migrations.md", """
    # When editing SQL migrations
    Apply only when the changed file is under `migrations/`.

    - Every migration must be REVERSIBLE; include the down-script.
    - Never DROP a column in the same release as renaming.
    - Always wrap in a transaction.
""")
print("""
Rules trigger by path/glob match. Use this instead of stuffing every rule into
CLAUDE.md, which would balloon every prompt's input tokens.
""")


# ---------------------------------------------------------------------------
# STEP 3 — Project skill / slash command (Lab 3.3)
# ---------------------------------------------------------------------------
banner(3, "Project skill / slash command (Lab 3.3)")
write(".claude/skills/run-migration/SKILL.md", """
    ---
    name: run-migration
    description: Run the latest Alembic migration in dev mode.
    ---

    ## Steps
    1. Confirm the user is on a feature branch (not main).
    2. Run `alembic upgrade head`.
    3. Run `pytest tests/db -q` to validate schema.
    4. Print the resulting head revision.

    ## Failure modes
    - If `alembic` not found: tell the user to `uv pip install -r requirements-dev.txt`.
    - If on `main`: REFUSE and tell the user to switch branches first.
""")
print("""
INVOCATION: in Claude Code, type `/run-migration` (or `/run_migration`).
SKILLS vs RULES: rules are passive guardrails; skills are named workflows the
                 user actively invokes.
""")


# ---------------------------------------------------------------------------
# STEP 4 — Plan mode vs direct execution (Lab 3.4)
# ---------------------------------------------------------------------------
banner(4, "Plan mode vs direct execution (Lab 3.4)")
DECISION = [
    ("Rename a single variable across 1 file",            "DIRECT — trivial, fully reversible"),
    ("Migrate test suite from unittest to pytest",        "PLAN — large blast radius, want approval"),
    ("Fix a typo in a docstring",                          "DIRECT"),
    ("Refactor authentication across 30 files",           "PLAN — must surface the strategy first"),
    ("Implement a feature spanning DB + API + UI",        "PLAN — multi-layer changes deserve a plan"),
]
for change, mode in DECISION:
    print(f"  {change:48}  -> {mode}")
print("""
RULE OF THUMB: PLAN MODE when (a) >5 files changed, (b) any DB migration,
               (c) anything that talks to prod, (d) anything irreversible.
""")


# ---------------------------------------------------------------------------
# STEP 5 — Headless / CI usage (Lab 3.5)
# ---------------------------------------------------------------------------
banner(5, "Headless Claude Code in CI (Lab 3.5)")
write(".github/workflows/claude-review.yml", """
    name: Claude code review
    on: [pull_request]
    jobs:
      review:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Run Claude headlessly
            env:
              ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
            run: |
              claude --print --output-format json \\
                  --allowedTools 'Read,Bash(git diff:*)' \\
                  "Review this PR diff. Output JSON {severity, file, line, comment}." \\
                > review.json
          - name: Post comment
            run: gh pr comment $PR_NUMBER --body-file review.json
""")
print("""
KEY FLAGS for CI:
  --print              non-interactive, single-shot
  --output-format json  machine-parseable
  --allowedTools '...'  least-privilege tool allow-list (NEVER pass --dangerously-skip-permissions in CI)
""")


# ---------------------------------------------------------------------------
# STEP 6 — Map workload to API (Lab 3.6)
# ---------------------------------------------------------------------------
banner(6, "Pick the right Anthropic API for each workload (Lab 3.6)")
MAP = [
    ("Latency-sensitive UI chat",                       "Messages API + streaming"),
    ("60K classification jobs, no latency need",        "Batch API (50% cheaper)"),
    ("Long-running orchestration on Anthropic's infra", "Agent SDK / Agent API"),
    ("Strict-schema classifier",                        "Messages API + tool_use as formatter"),
    ("Embed-and-rerank pipeline component",             "Messages API for the generation step only; use a separate embedding/rerank service"),
]
for workload, api in MAP:
    print(f"  {workload:40}  -> {api}")


# ---------------------------------------------------------------------------
# STEP 7 — Personal override of a team skill (Lab 3.7)
# ---------------------------------------------------------------------------
banner(7, "Personal override of a team skill (Lab 3.7)")
write(".claude/skills/run-migration/SKILL.md",
      open(DEMO / ".claude/skills/run-migration/SKILL.md").read())
# Personal override file (in ~/.claude/), simulated here:
write("USER_HOME_claude/skills/run-migration/SKILL.md", """
    ---
    name: run-migration
    description: My personal version — adds a dry-run preview first.
    ---

    ## Steps
    1. `alembic upgrade head --sql` -> print SQL but do NOT execute.
    2. Pause for me to read.
    3. Then run the real `alembic upgrade head`.
""")
print("""
PRECEDENCE: user (~/.claude/) > project (.claude/) > built-in.
USE CASE: you want extra safety steps without forcing them on the rest of the team.
""")


# ---------------------------------------------------------------------------
# STEP 8 — Session control (Lab 3.8)
# ---------------------------------------------------------------------------
banner(8, "Session control: --continue, --resume, fresh (Lab 3.8)")
SCENARIOS = [
    ("Yesterday's debugging session, same bug today",   "--resume <session-id>"),
    ("Picking up the exact LAST session",                 "--continue"),
    ("Switching from 'debug bug 123' to 'design feature X'", "fresh session (no flag)"),
    ("Branch a session to try a risky refactor",          "--resume and then fork mentally; commit before risky steps"),
]
for s, cmd in SCENARIOS:
    print(f"  {s:50}  -> {cmd}")
print("""
WHY NOT JUST KEEP ONE SESSION OPEN FOREVER?
  - Old context pollutes future answers (wrong facts cached).
  - Token cost grows with conversation length.
  - Prompt-injection that landed earlier persists.
START FRESH when the task changes.
""")


# ---------------------------------------------------------------------------
# SELF-CHECK
# ---------------------------------------------------------------------------
print(f"\n{'=' * 70}\n=== SELF-CHECK\n{'=' * 70}")
print("""
  1. Difference between CLAUDE.md and .claude/rules/*.md?
  2. Precedence order of user vs project vs built-in skills?
  3. Two CI flags that make Claude Code safe in headless mode?
  4. When to choose Batch API over Messages API?
  5. Why is plan mode preferred for >5-file changes?
  6. Which session command picks up exactly the last session?
  7. Where does the API key go in a CI workflow?

When you can answer all 7 from memory, tick the checklist in
  Domain3_ClaudeCode_Workflows_20pct/exam_prep/final_checklist.md
""")
print(f"\nSample artifacts written under: {DEMO}")
