# Practice Questions Set C (HARD, scenario-based) — Domain 1 — Agent Architecture & Orchestration (27%)

Sourced from the consolidated Set C (30 questions total). Each is a real-production scenario; many have plausible distractors.

Only the **9 questions tagged for this domain** appear here.

> Treat these as exam practice: read twice, eliminate clearly wrong answers, only then pick.

---

### 1. A team builds a Claude chatbot that occasionally calls `delete_account()`. The agent has `max_steps=20`, runs Sonnet, and logs every call. What is the MOST important missing safeguard?
- A) Switch to Opus
- B) Lower `max_steps` to 10
- C) Require human confirmation before irreversible tools
- D) Add streaming

### 2. A SOC analyst wants Claude to look up an IP, then post a Slack message, then close the alert. Errors mid-way must not orphan the alert. Best pattern?
- A) Single autonomous agent
- B) Chain workflow with explicit error gates
- C) Voting
- D) Orchestrator-workers

### 9. Your eval set shows Haiku scoring 88% and Sonnet 91% on classification. You want to ship Haiku to save 5×. What's the right move?
- A) Ship Haiku — 3% gap is acceptable
- B) Ship Sonnet — quality wins
- C) Router: Haiku first, escalate low-confidence cases to Sonnet
- D) Voting on Haiku × 5

### 10. A research workflow needs to plan, do 6 parallel sub-searches, then synthesize. Steps aren't known precisely. Best pattern?
- A) Chain
- B) Router
- C) Orchestrator-workers
- D) Evaluator-optimizer

### 12. A production agent must respect a $0.10 budget per session. Which mechanism enforces this?
- A) Anthropic enforces it server-side
- B) Track cumulative input+output tokens; halt the loop when projected cost exceeds budget
- C) `max_tokens` does it automatically
- D) Use `stop_sequence`

### 19. You want a workflow that drafts an email, critiques it against a rubric, and revises until the critique passes or 3 rounds elapse. Best pattern?
- A) Chain
- B) Router
- C) Evaluator-optimizer
- D) Voting

### 27. Which of these is a poor reason to choose an autonomous agent over a workflow?
- A) Subtasks are not known at design time
- B) The path varies with input
- C) The team wants the design to feel modern
- D) Tool composition depends on intermediate results

### 28. You're upgrading from Sonnet snapshot `2026-02-10` to `2026-05-20`. What's the safest deployment?
- A) Hot-cutover in production
- B) Run new snapshot in shadow against the eval harness, then canary 5% → 50% → 100% with rollback on regression
- C) A/B test in Claude.ai
- D) Roll out to Haiku users only

### 30. A KPI dashboard says your agent's success rate dropped from 96% to 88% after a quiet snapshot bump. First diagnostic step?
- A) Replay the eval harness against both snapshots and inspect failures by class
- B) Switch to Opus
- C) Lower `max_steps`
- D) Disable caching


---

## Answer key with explanations

| # | Ans | Source phase | Why |
|---|---|---|---|
| 1 | **C** | Phase 7 | The only safeguard that prevents irreversible damage is human-in-the-loop confirmation. `max_steps` and Opus do nothing for destructive tools. |
| 2 | **B** | Phase 7 | Steps are deterministic and ordered; a chain with explicit gates lets you stop and recover on partial failure. An agent for this is over-engineered and harder to debug. |
| 9 | **C** | Phase 7 | Router with confidence-based escalation gives the cost of Haiku and the quality of Sonnet. Pure-Haiku gives away 3% accuracy; pure-Sonnet wastes money. |
| 10 | **C** | Phase 7 | Sub-search shape is dynamic → orchestrator-workers. Chain requires known sequence; evaluator-optimizer is for quality loops. |
| 12 | **B** | Phase 7 | You enforce budgets in YOUR code by tracking usage and halting. The API has no per-session budget. |
| 19 | **C** | Phase 7 | Generator + critic loop with a stop condition = evaluator-optimizer by definition. |
| 27 | **C** | Phase 7 | "Modern feel" is not an engineering reason. Anthropic recommends the simplest pattern that works; agents have higher cost, latency, and safety surface. |
| 28 | **B** | Phase 9 | Shadow + canary with rollback is the only safe deployment for model bumps. A/B in Claude.ai doesn't reflect API behavior. |
| 30 | **A** | Phase 9 | The eval harness is exactly the tool for this. Inspect failures by class to localize regression (verbosity? format? reasoning?). Then decide rollback vs prompt update. |
