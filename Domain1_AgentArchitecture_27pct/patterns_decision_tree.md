# Architectural Decision Tree — "Which pattern do I use?"

Use this when an exam scenario asks "what's the best architecture?"

## Step 1 — Is the work deterministic or open-ended?

```
Is the WORKFLOW (sequence of steps) known at design time?
├── YES → Use a WORKFLOW (cheaper, more reliable, easier to test)
│        Go to Step 2.
└── NO  → Use an AGENT (ReAct loop with tools + max_steps cap)
         Go to Step 5.
```

> **Anthropic's rule of thumb**: Prefer the simplest pattern that works. Workflows beat agents whenever both fit.

## Step 2 — Workflow shape

```
What's the workflow shape?

Single input → single output, fixed order?
└── PROMPT CHAINING
    Example: transcript → bullet summary → action items → JSON

Single input → one of N specialists?
└── ROUTER
    Example: ticket → {billing, tech, refund}
    Tip: Use Haiku for the classifier to save cost

Single input → many INDEPENDENT subtasks → merge?
└── PARALLELIZATION (SECTIONING)
    Example: security review = (auth) ∥ (input val) ∥ (logging) ∥ (crypto)

Same input → same call N times → vote?
└── PARALLELIZATION (VOTING)
    Example: PII classification with 5 votes, majority wins

Subtasks NOT known upfront, need a planner?
└── ORCHESTRATOR-WORKERS
    Example: "refactor codebase to add logging"

Output must hit a measurable quality bar?
└── EVALUATOR-OPTIMIZER (Generator + Critic loop)
    Example: legal copy that must pass a rubric
```

## Step 3 — Pick the model tier per step

```
Classification / extraction / formatting       → Haiku
General-purpose reasoning, tool use, RAG       → Sonnet (default)
Planning, judging, hardest synthesis           → Opus
```

Mix tiers within the same workflow. Don't pay Opus prices for a router classifier.

## Step 4 — Add cost levers

- Long, repeated system prompts? → `cache_control: ephemeral` on the static prefix.
- Non-realtime bulk work? → **Batch API** (~50% off).
- RAG with big context? → Hybrid + rerank → only top 5–10 chunks reach Claude.
- High-volume classification? → Haiku, prefilled JSON, `max_tokens` tight.

## Step 5 — Agent? Add the safety belt

If you must use an agent:
1. `max_steps` cap (8–25 typical).
2. **Allow-list** of tools per step (or per phase).
3. **Sandbox** filesystem / shell access (chroot, container).
4. **Confirm** before irreversible actions (send_email, payment, delete).
5. **Budget cap** (tokens or $).
6. **Log every step** (tool name, args, result) for incident response.
7. Treat tool output / web content / RAG chunks as **data, not instructions**.

## Step 6 — Retrieval choice

```
< 50 docs, mostly fits in context        → no RAG, just stuff context (+ caching)
50–50K docs, semantic queries            → vector + rerank
Acronym / ID / code-heavy queries        → hybrid (vector + BM25, RRF)
Very long docs, scattered facts          → CONTEXTUAL RETRIEVAL (Claude pre-summarizes each chunk)
Cross-document synthesis                 → Mini-agent: retrieve → reason → maybe retrieve more
```

## Step 7 — Tool design

- 1 tool = 1 verb. Compose, don't bundle.
- Descriptions read like a coworker briefing — what it does, when to call, when NOT.
- Return JSON, never free-text. Include `is_error` on failure.
- Idempotent where possible. Side effects need a confirm step.

## Step 8 — Structured output

- Need free text + small JSON? → XML tags + post-parse.
- Need strict schema? → **Tool use as formatter** with `tool_choice={"type":"tool","name":"emit"}`.
- Need a specific opening? → **Prefill** the assistant.

## Common exam mappings (memorize these)

| Scenario | Pattern |
|---|---|
| "Classify each ticket then route to a specialist team" | Router |
| "Outline → draft → polish" | Chain |
| "Review code across 5 dimensions" | Sectioning |
| "Run the classifier 5× and take majority" | Voting |
| "Plan, do, synthesize across many files" | Orchestrator-workers |
| "Generate then critique until rubric passes" | Evaluator-optimizer |
| "Hands-off research, undefined steps" | Agent (ReAct) |
| "Codebase refactor where files aren't known upfront" | Orchestrator-workers OR Agent |
| "EU-only PII, must cite sources" | RAG with citations + system rule |
| "Cheap high-volume classification" | Haiku + prefilled JSON + caching |
| "Open-ended research brief from many sources" | Router → RAG workers → Evaluator |

When in doubt: **the simpler the pattern, the more likely it is the right answer**.
