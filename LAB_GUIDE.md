# Claude Certified Architect — Foundations: Lab Guide

> A domain-by-domain, hands-on lab guide for the **Claude Certified Architect — Foundations** exam, mapped against the official syllabus weighting and built on the code already in this `Claude_Learning/` workspace.
>
> **External reference used to structure this guide:** [paullarionov/claude-certified-architect — guide_en.MD](https://github.com/paullarionov/claude-certified-architect/blob/main/guide_en.MD)

---

## 0. How to use this guide

1. **Setup once** — follow [Section 0.1](#01-environment-setup) then leave the venv activated for all labs.
2. **Work through the 5 domains in order.** Each domain has:
   - *Theory recap* — the 6–10 ideas the exam tests.
   - *Anchor file* — the existing script in this repo that already implements the concept.
   - *Lab steps* — numbered, runnable instructions; "stretch" steps push beyond the anchor file.
   - *Self-check* — questions you must be able to answer before moving on.
3. **Track your weights.** The exam weights are 27 / 18 / 20 / 20 / 15. Spend study time roughly in proportion.

```
| Domain                                       | Weight | Anchor phase(s)             |
|----------------------------------------------|--------|-----------------------------|
| 1. Agent architecture and orchestration      | 27%    | Phase 7, Phase 10           |
| 2. Tool design and MCP integration           | 18%    | Phase 4, Phase 6            |
| 3. Claude Code configuration and workflows   | 20%    | Phase 8 + .claude/* configs |
| 4. Prompt engineering and structured output  | 20%    | Phase 2, Phase 3            |
| 5. Context management and reliability        | 15%    | Phase 5, Phase 10           |
```

---

## 0.1 Environment setup

```powershell
cd C:\Scripts\Send-escalationEmail\Claude_Learning
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env   # paste ANTHROPIC_API_KEY=sk-ant-...
```

Verify:

```powershell
python Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/01_first_message.py
```

A short Claude reply confirms the API key, network, and SDK are all wired up.

---

# DOMAIN 1 — Agent Architecture & Orchestration (27%)

> Single biggest slice of the exam. Master the agent loop, the 5 workflow patterns, hub-and-spoke multi-agent design, hooks, and session control.

## 1.A Theory recap

- An **agent loop** keeps calling Claude while `stop_reason == "tool_use"`; it stops on `"end_turn"`. Never use "did the assistant write text?" as a stop signal.
- Five workflow patterns: **chain, route, parallelize (sectioning / voting), orchestrator-workers, evaluator-optimizer**. Prefer workflows; reach for a true autonomous agent only when steps cannot be enumerated.
- Safety knobs every autonomous agent must have: `max_steps`, cost budget, tool allow-list, sandbox, human-in-the-loop on irreversible ops.
- **Hub-and-spoke**: the coordinator owns all inter-agent communication, errors, and routing; subagents have **isolated context** (no inherited history).
- **Hooks vs prompt instructions**: hooks give *deterministic* (100%) guarantees; prompts give *probabilistic* (>90%, not 100%) compliance. Use hooks for financial / legal / safety rules.
- **Session control**: `--resume <name>` to continue, `fork_session` to branch from shared context.

## 1.B Anchor files in this repo

| Pattern | File |
|---|---|
| Chain | [Domain1_AgentArchitecture_27pct/02_chain_workflow.py](Domain1_AgentArchitecture_27pct/02_chain_workflow.py) |
| Router | [Domain1_AgentArchitecture_27pct/03_router_workflow.py](Domain1_AgentArchitecture_27pct/03_router_workflow.py) |
| Parallel (sectioning + voting) | [Domain1_AgentArchitecture_27pct/04_parallel_workflow.py](Domain1_AgentArchitecture_27pct/04_parallel_workflow.py) |
| Orchestrator-workers | [Domain1_AgentArchitecture_27pct/05_orchestrator_workers.py](Domain1_AgentArchitecture_27pct/05_orchestrator_workers.py) |
| Evaluator-optimizer | [Domain1_AgentArchitecture_27pct/06_evaluator_optimizer.py](Domain1_AgentArchitecture_27pct/06_evaluator_optimizer.py) |
| Minimal ReAct loop | [Domain1_AgentArchitecture_27pct/07_react_agent.py](Domain1_AgentArchitecture_27pct/07_react_agent.py) |
| Loop + structured errors + interceptor/escalation | [Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py](Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py) |
| Composed system | [Domain1_AgentArchitecture_27pct/mini_project_research_agent.py](Domain1_AgentArchitecture_27pct/mini_project_research_agent.py) |

## Lab 1.1 — Drive the loop off `stop_reason` (not text)

1. Open [Domain2_ToolDesign_MCP_18pct/tool_use/02_multi_turn_tools.py](Domain2_ToolDesign_MCP_18pct/tool_use/02_multi_turn_tools.py) and locate the `while` loop.
2. Run it: `python Domain2_ToolDesign_MCP_18pct/tool_use/02_multi_turn_tools.py` — note how `stop_reason` decides the next iteration.
3. **Break it intentionally**: change the exit condition to `if "done" in last_text:` and rerun. Observe at least one of: infinite loop, wrong stop, missed tool. Revert.
4. **Self-check**: name the *only* reliable completion signal.

## Lab 1.2 — Walk through every workflow pattern

Run, in order:

```powershell
python Domain1_AgentArchitecture_27pct\02_chain_workflow.py
python Domain1_AgentArchitecture_27pct\03_router_workflow.py
python Domain1_AgentArchitecture_27pct\04_parallel_workflow.py
python Domain1_AgentArchitecture_27pct\05_orchestrator_workers.py
python Domain1_AgentArchitecture_27pct\06_evaluator_optimizer.py
```

For each, write one sentence answering: *what changes if I removed this pattern?* Match each to a real scenario from the exam guide (e.g., router → support-ticket triage; evaluator-optimizer → legal NDA drafting).

## Lab 1.3 — Build an autonomous ReAct agent with all 3 safety knobs

1. Read [Domain1_AgentArchitecture_27pct/07_react_agent.py](Domain1_AgentArchitecture_27pct/07_react_agent.py). It already has `max_steps`.
2. Add a **cost budget** (exercise 7-2): estimate `$/call` from `usage.input_tokens` and `usage.output_tokens` using approximate per-million pricing, break when exceeded.
3. Add a **tool allow-list per step** (exercise 7H-4): for the first 2 steps allow only read tools (`list_files`, `read_file`); after that, allow `count_lines`.
4. Demonstrate each safety knob firing by lowering the threshold (max_steps=2, budget=$0.001, allow-list missing required tool).

## Lab 1.4 — Hooks for deterministic enforcement (Domain 1.5)

Use [Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py](Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py) — already implements a `policy_interceptor` (a PreToolUse-style hook).

1. Run all four built-in test cases. Confirm T1 ($750) escalates and T2 ($49) executes.
2. Add a **PostToolUse-style normalizer**: a function called after every successful dispatch that converts any Unix timestamp into ISO 8601. Demonstrate it by adding a `last_seen_unix` field to the `CUSTOMERS` mock and showing the agent now sees ISO dates.
3. **Self-check**: when *must* you use a hook instead of a prompt instruction? (Answer: financial, legal, or safety rules where you need 100% compliance.)

## Lab 1.5 — Hub-and-spoke multi-agent with explicit context passing

1. Read [Domain1_AgentArchitecture_27pct/mini_project_research_agent.py](Domain1_AgentArchitecture_27pct/mini_project_research_agent.py).
2. Identify: (a) where the coordinator decomposes the task, (b) where it passes context into subagents (it must be in the prompt — subagents do NOT inherit), (c) where it aggregates.
3. **Inject the "narrow decomposition" bug** from exam Question 7 / Practice Q4: have the coordinator decompose "AI in creative industries" into only visual subtopics. Observe the final report missing music/literature/film. **Fix by partitioning the topic space explicitly** (Practice Q11).
4. **Self-check**: why is direct subagent-to-subagent communication an anti-pattern? (Loss of observability, uniform error handling, and context control — Practice Q8.)

## Lab 1.6 — Task decomposition strategies

| Strategy | File / scenario |
|---|---|
| Fixed pipeline (chain) | [Domain1_AgentArchitecture_27pct/02_chain_workflow.py](Domain1_AgentArchitecture_27pct/02_chain_workflow.py) |
| Dynamic adaptive | [Domain1_AgentArchitecture_27pct/05_orchestrator_workers.py](Domain1_AgentArchitecture_27pct/05_orchestrator_workers.py) |
| Multi-pass code review | [Phase10_Advanced_Capstone/04_code_review_agent.py](Phase10_Advanced_Capstone/04_code_review_agent.py) |

Lab: take the multi-pass review and add an **integration pass** that runs after all per-file passes (exam Q12 / Practice Q27 — fixes attention dilution).

## Lab 1.7 — Sessions: resume vs fork vs restart

Conceptual exercise — write a 1-paragraph answer for each:

- When is `--resume <name>` correct?
- When is `fork_session` correct?
- When should you start a *new* session with a summary instead?

(Reference: Chapter 5.10 of the external guide.)

## Domain 1 self-check

- [ ] I can sketch the agent loop and name the only valid stop signal.
- [ ] I can pick the right workflow pattern given a one-sentence scenario.
- [ ] I know why hooks beat prompts for refund caps, and where to install one.
- [ ] I can explain why subagents need explicit context passing.

---

# DOMAIN 2 — Tool Design & MCP Integration (18%)

## 2.A Theory recap

- **Tool descriptions are the primary selection mechanism.** When the model picks the wrong tool, the *first* fix is to expand descriptions with: what it does, input format, examples, edge cases, and *when to use it vs similar tools*. (Exam Q2, Q46, Q57.)
- **Rename to remove overlap.** `analyze_content` vs `analyze_document` will be misrouted — rename one to `extract_web_results` (Practice Q7).
- **Constrain capability at the interface level**: replace `fetch_url` with `load_document` that validates document MIME types (Practice Q10) — *least privilege*.
- **`tool_choice` options**: `"auto"` (default), `"any"` (must call some tool), `{"type":"tool","name":"..."}` (force a specific one).
- **Structured MCP errors**: `isError: true` + `{errorCategory, isRetryable, message, attempted_query, partial_results}`. Generic `"Operation failed"` is an anti-pattern.
- **MCP scopes**: project `.mcp.json` (VCS, team) vs user `~/.claude.json` (personal). Use `${ENV_VAR}` for tokens (Practice Q44).
- **Too many tools** (e.g., 18 vs 4–5) tanks selection reliability. Scope each subagent's toolset to its role.
- **Built-in tools**: `Glob` (filenames), `Grep` (content), `Read`/`Write`/`Edit`, `Bash`. If `Edit` fails on non-unique match → `Read` + `Write` fallback.

## 2.B Anchor files

| Concept | File |
|---|---|
| Basic tool definition + dispatch | [Domain2_ToolDesign_MCP_18pct/tool_use/01_function_calling.py](Domain2_ToolDesign_MCP_18pct/tool_use/01_function_calling.py) |
| Multi-turn loop with tools | [Domain2_ToolDesign_MCP_18pct/tool_use/02_multi_turn_tools.py](Domain2_ToolDesign_MCP_18pct/tool_use/02_multi_turn_tools.py) |
| Parallel tool calls in one turn | [Domain2_ToolDesign_MCP_18pct/tool_use/03_parallel_tools.py](Domain2_ToolDesign_MCP_18pct/tool_use/03_parallel_tools.py) |
| Realistic 3-tool triage | [Domain2_ToolDesign_MCP_18pct/tool_use/04_it_triage_agent.py](Domain2_ToolDesign_MCP_18pct/tool_use/04_it_triage_agent.py) |
| Built-in web_search | [Domain2_ToolDesign_MCP_18pct/tool_use/05_builtin_web_search.py](Domain2_ToolDesign_MCP_18pct/tool_use/05_builtin_web_search.py) |
| MCP server (stdio) | [Domain2_ToolDesign_MCP_18pct/mcp/02_mcp_server.py](Domain2_ToolDesign_MCP_18pct/mcp/02_mcp_server.py) |
| MCP client | [Domain2_ToolDesign_MCP_18pct/mcp/03_mcp_client.py](Domain2_ToolDesign_MCP_18pct/mcp/03_mcp_client.py) |
| Bridge MCP → Claude | [Domain2_ToolDesign_MCP_18pct/mcp/04_bridge_mcp_to_claude.py](Domain2_ToolDesign_MCP_18pct/mcp/04_bridge_mcp_to_claude.py) |
| SOC MCP mini project | [Domain2_ToolDesign_MCP_18pct/mcp/mini_project_soc_mcp.py](Domain2_ToolDesign_MCP_18pct/mcp/mini_project_soc_mcp.py) |
| **All 4 concepts together** | [Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py](Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py) |

## Lab 2.1 — Write descriptions that disambiguate similar tools

1. Open [Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py](Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py). Find `search_kb_articles` and `search_support_tickets` — deliberately similar tools.
2. Run test case **T4** ("How do I reset MFA?") — should hit `search_kb_articles`.
3. Run a synthetic case: `"Has customer E1042 reported this before?"` — should hit `search_support_tickets`.
4. **Sabotage**: shorten both descriptions to "Searches" and rerun. Note the misrouting rate climb.
5. **Fix**: restore detailed descriptions. Confirm correct routing.

## Lab 2.2 — Structured MCP error responses

`08_agent_loop_with_escalation.py` already returns `{errorCategory, isRetryable, description}`. Inspect `make_error()` and the 6 canonical categories. Then:

1. Force a `NOT_FOUND` (T3 already does this for `E9999`). Observe `isRetryable=false` — the model doesn't retry.
2. Force a `UPSTREAM_TIMEOUT` by lowering the random-timeout probability to 1.0 inside `issue_refund`. Observe `isRetryable=true` — the model retries once per the system prompt rule.
3. Add a new category `RATE_LIMITED` (retryable=true) and trigger it after the 2nd successful refund. Confirm the model backs off and retries.

## Lab 2.3 — `tool_choice` modes

Modify [Domain2_ToolDesign_MCP_18pct/tool_use/01_function_calling.py](Domain2_ToolDesign_MCP_18pct/tool_use/01_function_calling.py) to call once each with:

- `tool_choice={"type": "auto"}` — the model may respond in text.
- `tool_choice={"type": "any"}` — the model **must** call some tool (use for guaranteed structured output).
- `tool_choice={"type": "tool", "name": "<your_tool>"}` — forced first action (e.g., always call `extract_metadata` first).

Record what changes in `stop_reason` and `content` for each.

## Lab 2.4 — Allocate tools by role (least privilege)

In [Domain1_AgentArchitecture_27pct/mini_project_research_agent.py](Domain1_AgentArchitecture_27pct/mini_project_research_agent.py):

1. List every tool each subagent receives. Verify each list is the minimum needed.
2. Hand the document-analysis subagent a *general* `fetch_url`; observe (per Practice Q10) how it starts doing web searches it shouldn't.
3. **Fix**: replace with a constrained `load_document(path_or_url, expected_mime=["application/pdf","text/html","text/markdown"])`.

## Lab 2.5 — Build a tiny MCP server + client + bridge

```powershell
python Domain2_ToolDesign_MCP_18pct/mcp/02_mcp_server.py    # in one terminal
python Domain2_ToolDesign_MCP_18pct/mcp/03_mcp_client.py    # in another
python Domain2_ToolDesign_MCP_18pct/mcp/04_bridge_mcp_to_claude.py
```

Then study [Domain2_ToolDesign_MCP_18pct/mcp/mini_project_soc_mcp.py](Domain2_ToolDesign_MCP_18pct/mcp/mini_project_soc_mcp.py) — a server exposing 3 tools, 2 resources (URI-templated), 1 prompt. Confirm:

- All 3 tools are discovered automatically.
- Resources show up as content the agent can read for context (reducing exploratory tool calls).
- Errors propagate with `isError: true`.

## Lab 2.6 — Configure MCP servers correctly

Create a project `.mcp.json` at the workspace root:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

- Commit `.mcp.json`; do **not** commit `GITHUB_TOKEN`. Each dev exports it in their shell.
- Put any personal experiment server in `~/.claude.json`, NOT in the project file.

## Lab 2.7 — Built-in tool selection drill

Given each task, write down which built-in tool is correct:

| Task | Tool |
|---|---|
| Find every `*.test.tsx` under `src/components/` | `Glob` |
| Find every call site of `processPayment(` | `Grep` |
| Replace a unique snippet in one file | `Edit` |
| `Edit` failed because match is not unique | `Read` + `Write` |
| Run `npm test` | `Bash` |

## Domain 2 self-check

- [ ] I can write a tool description that disambiguates from a similar tool.
- [ ] I know the 3 `tool_choice` modes and when each is right.
- [ ] I can identify an MCP `isError` payload that gives the coordinator enough info to recover.
- [ ] I know `${ENV_VAR}` substitution belongs in project `.mcp.json`.

---

# DOMAIN 3 — Claude Code Configuration & Workflows (20%)

> Claude Code-specific: CLAUDE.md hierarchy, `.claude/rules/`, `.claude/commands/`, `.claude/skills/`, planning mode, `/compact`, `--resume`, CI/CD via `-p` flag.

## 3.A Theory recap

- **CLAUDE.md hierarchy**: user (`~/.claude/CLAUDE.md`, personal) → project (`.claude/CLAUDE.md` or root `CLAUDE.md`, VCS-shared) → directory (`CLAUDE.md` in subdirs). **Project-level is what teammates inherit.** Personal preferences in user-level. (Practice Q37, Q41.)
- **`@path` imports** modularize CLAUDE.md: `@./standards/testing.md`, `@README.md`. Max nesting depth = 5.
- **`.claude/rules/`** — topic files with YAML frontmatter `paths: ["src/api/**/*"]` for **conditional, path-based** loading. Use when conventions span many dirs (tests, migrations). Directory-level CLAUDE.md when conventions are bound to one dir. (Practice Q40, Q42.)
- **Slash commands / Skills**: project `.claude/commands/` and `.claude/skills/<name>/SKILL.md` are VCS-shared. Personal copies in `~/.claude/`. Personal skill with the **same name** overrides the project skill (Practice Q36).
- **SKILL.md frontmatter**: `context: fork` (isolated subagent — keeps verbose output out of main session, Practice Q35, Q43), `allowed-tools: [...]` (least privilege), `argument-hint: "..."` (Practice Q39).
- **Planning mode** for: large changes (45+ files), multiple plausible approaches, architectural decisions, unfamiliar codebases. **Direct execution** for: single-file fix with clear stack trace, adding one validation. (Exam Q5, Practice Q32, Q34.)
- **CI/CD**: use `-p` / `--print` for non-interactive (Exam Q10, Practice Q26). Use `--output-format json` + `--json-schema` for parseable PR comments (Practice Q16). Re-runs must include prior findings to avoid duplicate comments (Practice Q25). Independent instance reviews better than the generator (Practice Q17).
- **Batch API** suits overnight / weekly workloads, **not** blocking pre-merge checks (Exam Q11, Practice Q19, Q21, Q30). No multi-turn tool calling inside one batch request (Practice Q18).
- **`/compact`** condenses history (risks losing exact numbers). **`/memory`** opens CLAUDE.md to save persistent notes.

## 3.B Anchor file

[Domain3_ClaudeCode_Workflows_20pct/README.md](Domain3_ClaudeCode_Workflows_20pct/README.md) is theory-only. The labs below build the configs you'd find in a real Claude Code repo.

## Lab 3.1 — Build a project-level CLAUDE.md

Create `.claude/CLAUDE.md` (or root `CLAUDE.md`) in this workspace:

```markdown
# Project standards

@./standards/coding-style.md
@./standards/testing.md

This project uses Python 3.12, the Anthropic Python SDK, and stdio MCP servers.
Run tests with: `pytest -q`.
Lint with:    `ruff check .`.
Never commit `.env`. Use environment variable substitution in `.mcp.json`.
```

Create `standards/coding-style.md` and `standards/testing.md` and verify `@path` loads them. **Self-check**: why is putting the team's "always use type hints" rule in `~/.claude/CLAUDE.md` (user-level) a bug? (New teammate won't get it — Practice Q37.)

## Lab 3.2 — Conditional rules via `.claude/rules/`

Create three files:

`.claude/rules/api-conventions.md`
```markdown
---
paths: ["src/api/**/*.ts"]
---
For API files use async/await with explicit error handling.
Each endpoint must return a standard response wrapper.
```

`.claude/rules/tests.md`
```markdown
---
paths: ["**/*.test.ts", "**/*.test.tsx"]
---
Use describe/it blocks. Use data factories instead of hardcoded values.
Do not mock the database — use the test database.
```

`.claude/rules/migrations.md`
```markdown
---
paths: ["**/migrations/*.sql"]
---
Migrations are forward-only. Each migration must include a rollback comment.
```

**Self-check**: which beats directory-level CLAUDE.md when test files are scattered across `src/`, `lib/`, and `apps/`? (Path-globbed rules — Practice Q40.)

## Lab 3.3 — Create a project slash command / skill

`.claude/skills/review/SKILL.md`
```markdown
---
context: fork
allowed-tools: ["Read", "Grep", "Glob"]
argument-hint: "Path to the directory or PR to review"
---

Perform a code review using our project conventions.
Output for each finding:
{ "file": "...", "line": N, "severity": "critical|high|medium|low", "issue": "...", "fix": "..." }
Report at most 10 findings ordered by severity.
```

**Why `context: fork`?** Verbose review output stays out of the main session (Practice Q35, Q43).
**Why `allowed-tools`?** A review skill must never `Write` or `Bash` (Practice Q39).
**Why `argument-hint`?** Prevents running without a target (Practice Q39).

## Lab 3.4 — Plan vs direct execution

For each task below, decide planning mode vs direct:

| Task | Choice | Why |
|---|---|---|
| Add a null check to one file with a clear stack trace | Direct | Single, unambiguous change |
| Migrate 47 files to a new logging library | Planning | Many files, architectural decision |
| Decide microservice boundaries | Planning | Multiple plausible approaches |
| Fix a typo in a docstring | Direct | Trivial |
| Add Slack as a new notification channel (webhooks vs bot tokens vs Slack App) | Planning | Multiple valid integrations (Practice Q32) |

## Lab 3.5 — Run Claude Code headlessly in CI

```bash
# bash / GitHub Actions
claude -p "Review this pull request for security issues" \
  --output-format json \
  --json-schema '{
    "type":"object",
    "properties":{
      "findings":{
        "type":"array",
        "items":{
          "type":"object",
          "required":["file","line","severity","issue","fix"],
          "properties":{
            "file":{"type":"string"},
            "line":{"type":"integer"},
            "severity":{"enum":["critical","high","medium","low"]},
            "issue":{"type":"string"},
            "fix":{"type":"string"}
          }
        }
      }
    },
    "required":["findings"]
  }' \
  > findings.json

# Then a small script posts each finding as an inline PR comment via the GitHub API.
```

**Why `-p`?** Without it the CLI waits for interactive input and the CI job hangs (Practice Q26). **Why `--json-schema`?** Guarantees parseable structured output (Practice Q16).

## Lab 3.6 — Match each workload to the right API

| Workload | Sync or Batch? | Why |
|---|---|---|
| Pre-merge PR check (developer waiting) | **Sync** | Batch can take 24h |
| Nightly test-debt report | **Batch** | 50% cost saving, can wait |
| Weekly security audit | **Batch** | Same |
| Interactive PR review tool with tool-calls per file | **Sync** | Batch has no multi-turn tool use (Practice Q18) |

## Lab 3.7 — Personal override of a team skill

If the team ships `.claude/skills/commit/SKILL.md`, place YOUR personal version at `~/.claude/skills/commit/SKILL.md` (same name). Personal scope overrides project scope and you keep typing `/commit` (Practice Q36).

## Lab 3.8 — Session control

| Goal | Command |
|---|---|
| Continue named long investigation | `claude --resume investigation-auth-bug` |
| Explore two competing approaches | `fork_session` from a shared discovery context |
| Files have changed a lot since the prior session | **Start new** session with a one-paragraph summary, do NOT resume stale tool results |

## Domain 3 self-check

- [ ] I can place a rule at user / project / directory / `.claude/rules/` / skill scope and justify each choice.
- [ ] I know exactly which CLI flags make Claude Code CI-safe (`-p`, `--output-format json`, `--json-schema`).
- [ ] I can pick planning vs direct in 5 seconds for any task.
- [ ] I know which workloads can move to Batch and which cannot.

---

# DOMAIN 4 — Prompt Engineering & Structured Output (20%)

## 4.A Theory recap

- **Explicit criteria beat vague instructions.** "Flag a comment only when it contradicts code behavior" beats "check comment accuracy" (Practice Q22).
- **Few-shot examples** are the most effective fix for inconsistent output format and ambiguous routing (Exam Q3, Practice Q20, Q47, Q49, Q60).
- **`tool_use` with JSON schema** is the only reliable way to guarantee syntactically valid JSON; it does NOT guarantee semantic correctness.
- **Schema design**: required only if always present; use `"type": ["string","null"]` for absent data; include `"other"` + a detail field for extensible enums; include `"unclear"` for honest uncertainty.
- **Retry-with-feedback** works for format / arithmetic errors; does NOT help when info is simply not in the source.
- **Self-correction**: extract both `stated_total` and `calculated_total`, set `conflict_detected: true` when they differ.
- **Message Batches**: 50% cheaper, ≤24h, `custom_id` correlates request/response, no multi-turn tool calling.
- **Multi-pass review**: per-file + integration pass (Exam Q12 / Practice Q27). A larger context window does NOT fix attention dilution.
- **Independent reviewer instance** beats self-review (Practice Q17).
- **System-prompt drift**: in long sessions, periodic user-role reminders or replacing verbose rules with few-shot examples (Practice Q69, Q70).
- **Prefilling** the assistant message removes repetitive openings ("Certainly!") more reliably than prompting against them (Practice Q72).

## 4.B Anchor files

| Concept | File |
|---|---|
| XML tags for structure | [Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/01_xml_tags.py](Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/01_xml_tags.py) |
| Few-shot | [Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/02_few_shot.py](Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/02_few_shot.py) |
| Chain-of-thought | [Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/03_chain_of_thought.py](Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/03_chain_of_thought.py) |
| Prefilling | [Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/04_prefilling.py](Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/04_prefilling.py) |
| Eval framework | [Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/05_eval_framework.py](Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/05_eval_framework.py) |
| LLM judge | [Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/06_llm_judge.py](Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/06_llm_judge.py) |
| Structured output via tool | [Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/05_structured_output.py](Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/05_structured_output.py) |
| `stop_reason` reference | [Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/07_stop_reasons_and_errors.py](Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/07_stop_reasons_and_errors.py) |
| Evaluator-optimizer (multi-pass quality) | [Domain1_AgentArchitecture_27pct/06_evaluator_optimizer.py](Domain1_AgentArchitecture_27pct/06_evaluator_optimizer.py) |
| Compliance RAG extractor | [Phase10_Advanced_Capstone/02_compliance_rag_production.py](Phase10_Advanced_Capstone/02_compliance_rag_production.py) |
| Code review (multi-pass) | [Phase10_Advanced_Capstone/04_code_review_agent.py](Phase10_Advanced_Capstone/04_code_review_agent.py) |
| Eval harness | [Phase10_Advanced_Capstone/05_eval_harness.py](Phase10_Advanced_Capstone/05_eval_harness.py) |

## Lab 4.1 — Explicit criteria for code review

Take the vague review prompt in [Phase10_Advanced_Capstone/04_code_review_agent.py](Phase10_Advanced_Capstone/04_code_review_agent.py). Tighten it like this:

```
Flag a comment ONLY if:
1. The comment describes behavior that CONTRADICTS the actual code behavior, OR
2. The comment references a non-existent function or variable, OR
3. A TODO/FIXME refers to a bug already fixed in code.
Do NOT flag stylistically outdated comments or minor wording issues.

Severity:
- CRITICAL: runtime failure for users (e.g., NullPointerException in payment path)
- HIGH:     security vulnerability (SQLi, XSS, missing authz)
- MEDIUM:   logic bug without immediate impact
- LOW:      code quality (duplication, suboptimal small-N algorithm)
```

Run before and after on the same PR; measure false-positive rate drop.

## Lab 4.2 — Few-shot to fix ambiguous tool selection

Start from [Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/02_few_shot.py](Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/02_few_shot.py). Add 4–6 examples that target ambiguous cases for the support agent (Practice Q60), e.g.:

```
Request: "check my recent purchase"
Action: lookup_order  (NOT get_customer — they're asking about the order, not their profile)

Request: "I want to update my saved address"
Action: get_customer first (the address lives on the profile)
```

## Lab 4.3 — Structured output via `tool_use`

Open [Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/05_structured_output.py](Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/05_structured_output.py). Use a tool schema like:

```json
{
  "type": "object",
  "properties": {
    "category":   {"type": "string", "enum": ["bug","feature","docs","unclear","other"]},
    "category_detail": {"type": ["string","null"], "description": "details if other/unclear"},
    "severity":   {"type": "string", "enum": ["critical","high","medium","low"]},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "optional_field": {"type": ["string","null"]}
  },
  "required": ["category","severity"]
}
```

Use `tool_choice: {"type":"any"}` to *guarantee* a tool call → structured output, regardless of whether the model wanted to chat.

## Lab 4.4 — Retry-with-feedback loop

Build a small extractor that:

1. Calls Claude with a document + schema.
2. Validates with `pydantic` (`model_validate(json.loads(...))`).
3. On `ValidationError`, retries up to N=2 with: original document + previous (wrong) output + the exact validation message.
4. Stops retrying if the missing info is clearly absent — don't loop forever.

Skeleton ([Phase10_Advanced_Capstone/02_compliance_rag_production.py](Phase10_Advanced_Capstone/02_compliance_rag_production.py)) has the shape.

## Lab 4.5 — Self-correction for arithmetic

Add to the extractor:

```python
"line_items": [...],
"stated_total":     {"type":"number"},
"calculated_total": {"type":"number"},
"conflict_detected":{"type":"boolean"}
```

The model returns both totals; you set `conflict_detected = abs(stated-calc) > 0.01` in code, then surface it for human review.

## Lab 4.6 — Multi-instance review (independent reviewer)

In [Phase10_Advanced_Capstone/04_code_review_agent.py](Phase10_Advanced_Capstone/04_code_review_agent.py):

1. Pass 1 — instance A generates code.
2. Pass 2 — instance B reviews WITHOUT seeing A's reasoning (just the final diff). This avoids confirmation bias (Practice Q17).
3. Compare findings.

## Lab 4.7 — Multi-pass review (per-file + integration)

In the same script: split a 14-file PR into per-file passes, then run one integration pass that only looks at imports and shared types between files (Practice Q27). Compare bug count and consistency vs single-pass.

## Lab 4.8 — Batch API for non-blocking workloads

Skeleton:

```python
from anthropic import Anthropic
client = Anthropic()
batch = client.messages.batches.create(requests=[
    {"custom_id": f"doc-{i:03d}",
     "params": {"model": "claude-sonnet-4-5",
                "max_tokens": 1024,
                "messages": [{"role":"user","content": f"Extract data from: {doc}"}]}}
    for i, doc in enumerate(documents)
])
# Later: poll batch.id, when complete download results, re-submit failures by custom_id only.
```

**Use when**: overnight tech-debt reports, weekly audits, bulk extraction. **Do NOT use** for pre-merge checks or iterative multi-turn tool calls.

## Lab 4.9 — Eval harness

Run [Phase10_Advanced_Capstone/05_eval_harness.py](Phase10_Advanced_Capstone/05_eval_harness.py). Add 50 golden cases; track per-prompt accuracy, token counts, latency, and `stop_reason` distribution. Alert on >2% accuracy drop or >20% token drift after any prompt or model-snapshot change.

## Domain 4 self-check

- [ ] I can write explicit criteria for "what to flag / what to ignore" for any review.
- [ ] I rank: tool-use-as-formatter > prefill `{"label":"` > free-text JSON request.
- [ ] I know when retry-with-feedback won't help.
- [ ] I know why a bigger context window does NOT fix multi-file review.
- [ ] I know which workloads belong on the Batch API.

---

# DOMAIN 5 — Context Management & Reliability (15%)

## 5.A Theory recap

- **Stateless API**: full history must be in `messages` every call (Practice Q64, Q67). No `session_id` exists.
- **Lost-in-the-middle**: place key info at top and bottom; use explicit section headings (Practice Q13).
- **Progressive summarization risks losing exact numbers, percentages, dates**. Counter with a **"case facts" block** outside the summary, included in every prompt (Practice Q54).
- **Trim tool outputs** to relevant fields via a PostToolUse hook (Practice Q14: prefer compact upstream output over a summarizer downstream).
- **Hybrid context strategy** (Practice Q65, Q66): structured facts + summary of older turns + verbatim recent turns.
- **Subagents** isolate verbose discovery; the coordinator keeps one line in context instead of 15 files (Practice Q45).
- **Scratchpad files** preserve key findings across context boundaries (Chapter 11.4).
- **Error categories**: transient (retry w/ backoff), validation (fix input), business (explain + alternative), permission (escalate).
- **Anti-patterns**: generic error status, silent suppression (empty = success), abort-on-first-failure, infinite local retries (Chapter 10.2).
- **Distinguish access failure (timeout) from valid empty result** (`"0 results"` from industry reports is informative; timeout from patent DB needs retry — Practice Q12).
- **Coverage annotations** in the final synthesis when some sources failed (Practice Q5).
- **Escalation triggers**: explicit "get me a manager" → immediate; policy gap (e.g., competitor price match silent in policy) → escalate (Practice Q50); multiple customer matches → ask for an extra identifier, do NOT guess (Practice Q55).
- **NOT reliable triggers**: sentiment, model self-rated confidence, complex classifiers.
- **Structured handoff** to humans: customer id, summary, root cause, actions taken, recommended action, escalation reason (Chapter 9.3).
- **Provenance**: every claim must carry `source_url`, `source_name`, `publication_date`, `confidence`. Preserve conflicting values with attribution (Practice Q1, Chapter 12).
- **Stratified random sampling**: aggregate "97% accuracy" can hide 40% errors on one doc type — analyze accuracy by doc type and field.
- **Field-level confidence calibration**: high confidence + stable accuracy → automate; low confidence → human review.

## 5.B Anchor files

| Concept | File |
|---|---|
| RAG chunking | [Domain5_ContextMgmt_Reliability_15pct/01_chunking.py](Domain5_ContextMgmt_Reliability_15pct/01_chunking.py) |
| Vector search | [Domain5_ContextMgmt_Reliability_15pct/02_embeddings_and_search.py](Domain5_ContextMgmt_Reliability_15pct/02_embeddings_and_search.py) |
| Hybrid BM25 | [Domain5_ContextMgmt_Reliability_15pct/03_hybrid_bm25.py](Domain5_ContextMgmt_Reliability_15pct/03_hybrid_bm25.py) |
| Reranking | [Domain5_ContextMgmt_Reliability_15pct/04_reranking.py](Domain5_ContextMgmt_Reliability_15pct/04_reranking.py) |
| Contextual retrieval | [Domain5_ContextMgmt_Reliability_15pct/05_contextual_retrieval.py](Domain5_ContextMgmt_Reliability_15pct/05_contextual_retrieval.py) |
| KB QA mini-project | [Domain5_ContextMgmt_Reliability_15pct/mini_project_kb_qa.py](Domain5_ContextMgmt_Reliability_15pct/mini_project_kb_qa.py) |
| Escalation + interceptor | [Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py](Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py) |
| Multi-tier support | [Phase10_Advanced_Capstone/03_support_agent_multi_tier.py](Phase10_Advanced_Capstone/03_support_agent_multi_tier.py) |
| SOC triage pipeline (graceful degradation) | [Phase10_Advanced_Capstone/01_soc_triage_pipeline.py](Phase10_Advanced_Capstone/01_soc_triage_pipeline.py) |

## Lab 5.1 — Extract a persistent "case facts" block

Modify [Phase10_Advanced_Capstone/03_support_agent_multi_tier.py](Phase10_Advanced_Capstone/03_support_agent_multi_tier.py):

1. After each tool call, parse out transactional facts (customer id, order id, amount, request).
2. Maintain a `CASE_FACTS` dict in code (not in conversation history).
3. Inject it into the system prompt on every turn:

```
=== CASE FACTS ===
Customer ID: {cid}
Order ID:    {oid}
Amount:      ${amt}
Request:     {req}
Status:      {status}
===
```

Run a long simulated dialogue. Observe the model now answers "the 15% discount I mentioned" correctly even at turn 40 (Practice Q54).

## Lab 5.2 — Trim verbose tool outputs (PostToolUse hook)

```python
def trim_order(result):
    return {k: result[k] for k in ("order_id","status","total","items","return_eligible")}
```

Wire it into the dispatcher of [Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py](Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py) so any `lookup_order` result is pruned before being placed in the message history. Compare `input_tokens` before/after.

## Lab 5.3 — Position-aware input layout

When you aggregate results from multiple agents into a single synthesis call, structure the input as:

```
[KEY FINDINGS — top]
- 3 critical vulnerabilities in auth.ts
- 1 SQL injection in user-search

[DETAILED RESULTS — middle, with explicit headings]
=== File auth.ts ===
...
=== File search.ts ===
...

[ACTION ITEMS — bottom]
Priority: fix auth.ts before merge.
```

Headings + primacy/recency placement mitigate lost-in-the-middle (Practice Q13).

## Lab 5.4 — Scratchpad file pattern

In a long investigation, have the agent write key findings to `investigation-scratchpad.md` as it goes. On a fresh session, prime context with the scratchpad instead of re-running discovery (Chapter 11.4).

## Lab 5.5 — Delegate to subagents to protect context

Refactor [Domain1_AgentArchitecture_27pct/mini_project_research_agent.py](Domain1_AgentArchitecture_27pct/mini_project_research_agent.py) so the coordinator delegates "read these 15 files and tell me about dependencies" to an Explore subagent that returns only a 3-line summary. The coordinator's context now grows by 3 lines, not 15 files (Practice Q45, Chapter 11.5).

## Lab 5.6 — Structured error propagation in multi-agent system

Inside the research mini-project, simulate a web-search subagent timeout. The subagent must return:

```json
{
  "status": "partial_failure",
  "failure_type": "timeout",
  "attempted_query": "AI music industry 2024",
  "partial_results": [{"title":"...","url":"...","relevance":0.8}],
  "alternative_approaches": [
    "Try narrower query 'AI music composition tools'",
    "Switch to an alternative data source"
  ],
  "coverage_impact": "Not covered: AI impact on music production"
}
```

The coordinator then decides: retry with narrower query, accept partial results, or annotate the gap. Verify the final synthesis carries a **coverage annotation** rather than silently dropping the section (Practice Q5, Q9).

## Lab 5.7 — Distinguish access failures from valid empty results

Subagent returns three categories of outcomes; the coordinator must treat them differently:

| Subagent outcome | Coordinator action |
|---|---|
| `15 results` | use |
| `0 results` (valid empty) | accept as informative |
| `timeout` (access failure) | retry decision |

(Practice Q12.)

## Lab 5.8 — Escalation calibration

In [Phase10_Advanced_Capstone/03_support_agent_multi_tier.py](Phase10_Advanced_Capstone/03_support_agent_multi_tier.py), encode these explicit triggers in the system prompt with one few-shot per trigger:

- "get me a manager" → immediate escalation (Practice Q49).
- Policy silent on request (e.g., competitor price match) → escalate for human judgment (Practice Q50).
- Multiple customer matches → ask user for additional identifier; do NOT guess (Practice Q55).
- Refund above auto-approve threshold → blocked by **hook**, never prompt (Practice Q51 — programmatic precondition).

## Lab 5.9 — Structured handoff payload

When the agent escalates, emit this JSON to the human queue:

```json
{
  "customer_id": "CUST-12345",
  "customer_name": "Priya Subramanian",
  "issue_summary": "Damaged item refund request",
  "order_id": "ORD-9001",
  "root_cause": "Item arrived damaged; photos attached",
  "actions_taken": [
    "Verified via get_customer",
    "Confirmed order via lookup_order",
    "Offered replacement — customer insists on refund"
  ],
  "refund_amount": "$89.99",
  "recommended_action": "Approve full refund",
  "escalation_reason": "Customer requested a manager"
}
```

The human reviewer only sees this — it must be self-contained (Chapter 9.3).

## Lab 5.10 — Provenance + conflict preservation

When two sources disagree, preserve both:

```json
{
  "claim": "AI-generated share of streaming music",
  "values": [
    {"value":"12%","source":"Spotify Annual Report 2024","date":"2024-03","methodology":"automated"},
    {"value":"8%","source":"Music Industry Association Survey","date":"2024-07","methodology":"survey n=500"}
  ],
  "conflict_detected": true,
  "possible_explanation": "Methodology and time-period differences"
}
```

Do NOT arbitrarily pick one (Practice Q1, Chapter 12.2).

## Lab 5.11 — Stratified sampling for extraction QA

In [Phase10_Advanced_Capstone/05_eval_harness.py](Phase10_Advanced_Capstone/05_eval_harness.py), break the eval by **document type** and **field**, not just aggregate accuracy. Demonstrate a case where overall accuracy is 97% but one doc type sits at 60% — that's the bucket to fix.

## Domain 5 self-check

- [ ] I can give 3 reasons to extract "case facts" outside the conversation.
- [ ] I know why "summarize everything" loses critical info.
- [ ] I can write a structured subagent error that lets the coordinator recover.
- [ ] I know the 5 reliable escalation triggers and 3 unreliable ones.
- [ ] I never pick a value when sources conflict — I preserve both with provenance.

---

# 6. Capstone scenarios (cross-domain)

Replicate each end-to-end exam scenario by composing the labs above:

| Scenario | Build by combining |
|---|---|
| **Customer Support Agent** | Labs 2.1 (tool descriptions), 1.4 (hook for refund cap), 5.8 (escalation triggers), 5.9 (handoff payload), 5.1 (case facts) |
| **Code Generation with Claude Code** | Labs 3.1–3.5 |
| **Multi-Agent Research System** | Labs 1.5, 1.6, 5.6, 5.7, 5.10 |
| **Developer Productivity Tools** | Labs 2.5–2.7, 3.7, 3.8 |
| **Claude Code for CI/CD** | Labs 3.5, 3.6, 4.6, 4.8 |
| **Structured Data Extraction** | Labs 4.3, 4.4, 4.5, 5.11 |
| **Conversational AI Architecture Patterns** | Labs 5.1, 5.3 + the drift fixes in Practice Q69/Q70 |
| **Agentic AI Tools (open in the guide)** | Labs 1.3, 1.4, 2.2, 5.6 |

---

# 7. Pre-exam checklist

Already in this repo: [Phase9_ExamPrep/final_checklist.md](Phase9_ExamPrep/final_checklist.md), [Phase9_ExamPrep/glossary.md](Phase9_ExamPrep/glossary.md), [Phase9_ExamPrep/practice_questions.md](Phase9_ExamPrep/practice_questions.md), [Phase9_ExamPrep/practice_questions_setC.md](Phase9_ExamPrep/practice_questions_setC.md).

Add these last-mile drills:

- [ ] Recite the agent loop in 4 lines.
- [ ] Name a deterministic guarantee a hook gives that a prompt cannot.
- [ ] State two CLAUDE.md misconfigurations that block teammates from inheriting instructions.
- [ ] Decide planning vs direct execution for 10 random tasks in <60 s.
- [ ] Distinguish CLI flags for non-interactive run vs structured output.
- [ ] Walk through 5 ways to compress context without losing exact values.
- [ ] List the 3 unreliable escalation triggers and explain why each fails.

---

# 8. Out-of-scope (do NOT study)

Per the official guide:

- Fine-tuning / training custom models
- API auth, billing, account management
- Specific language framework implementation details beyond schemas
- MCP server hosting / infra / container orchestration
- Claude internals, RLHF, Constitutional AI
- Vector DB implementation details
- Computer use / vision / streaming
- Rate limits, quotas, cost calculations
- OAuth, key rotation
- Cloud-provider specifics
- Benchmarks / model comparisons
- Prompt-caching internals (know it exists)
- Tokenization algorithm details

---

**End of Lab Guide.** Work top-down; tick the self-check boxes in each domain; finish with the capstone scenarios in Section 6.
