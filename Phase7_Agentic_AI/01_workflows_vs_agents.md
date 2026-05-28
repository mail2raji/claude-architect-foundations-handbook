# Workflows vs Agents — Cheat-Sheet

| Pattern | One-line description | Code-controlled? | Typical use |
|---|---|---|---|
| **Chain** | Step 1 → Step 2 → ... fixed order | Yes | Outline-draft-polish |
| **Routing** | A router LLM call picks a specialist | Yes | Triage, model-tier picking |
| **Parallel (sectioning)** | Split work, fan out, merge | Yes | Multi-section reports |
| **Parallel (voting)** | Same task N times, majority wins | Yes | Reliability boost on classification |
| **Orchestrator-workers** | A planning LLM dynamically spawns workers | Partially | Research deep-dives |
| **Evaluator-optimizer** | Generator + critic loop until rubric passes | Partially | Legal drafts, code w/ tests |
| **Autonomous agent (ReAct)** | LLM picks next tool, observes, repeats | No | Open-ended tasks |

## Anthropic's golden rule

> Use the simplest pattern that works. Most production wins come from **prompts + workflows**, not from cranking the autonomy dial.

## Safety knobs for every agent

- `max_steps` budget
- `max_cost_usd` budget (track token usage × price)
- Allow-list of tools per step / per phase
- Human approval on irreversible actions (send-email, delete, transfer-money)
- Sandboxing (no host shell access unless you mean it)
- Full **trace logging** — every input, output, tool call, time, tokens

## Choosing a model tier inside an agent

Common pattern: cheap classifier (Haiku) → main reasoner (Sonnet) → final judge (Opus). Spend where it pays.
