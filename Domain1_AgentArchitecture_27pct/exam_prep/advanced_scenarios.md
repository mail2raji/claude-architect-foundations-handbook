# Advanced Architectural Scenarios — Domain 1 — Agent Architecture & Orchestration (27%)

Sourced from the consolidated 25 cross-domain scenarios.
Only the **11 scenarios tagged for this domain** appear here.

Sketch an architecture answer first, then compare to the solution sketch at the bottom.

---

## Exercises

**E2.** A SOC ingests 8,000 alerts/hour. 95% are noise. Budget is $300/day for AI. Architect a triage system.

**E3.** A compliance team needs nightly reports comparing 600 contracts against a master template, listing deviations. Latency doesn't matter; cost does. Architect.

**E4.** Marketing wants A/B tests of three subject lines per email. They send 10M emails/day. Architect a generator + selector.

**E5.** Engineering wants Claude to read a JIRA ticket and propose a PR. The PR may touch any of 800 files. Architect (workflow vs agent? safety?).

**E7.** Legal Ops wants a "redline-the-NDA" service that rewrites an NDA to fit company policy, then explains each change. Architect.

**E11.** A SaaS company gets ~50K support tickets/month. They want auto-tagging by product area + sentiment. Cost is the constraint. Architect.

**E12.** A research team wants Claude to write a 5-page report drawing from 200 internal PDFs every quarter. Quality is the constraint. Architect.

**E14.** A bank wants Claude to power a wealth-management workflow: pull positions → assess risk → recommend rebalance → draft client memo. Architect.

**E15.** A safety review: your team's agent calls a delete_customer tool occasionally on prod. What went wrong and how to fix?

**E19.** A research agent loops forever on one query. What knobs did the team forget?

**E25.** Design observability for a multi-agent system. What do you log per call?


---
## Solution sketches

**A2.** Router (Haiku) → 95% auto-close (Haiku) + 4% Sonnet enrichment + 1% Opus escalation drafts. Tool-augmented Sonnet path looks up IOCs. Daily cost model: 8000 × 24 × 0.95 Haiku is cheap; only ~10K Sonnet calls/day + ~2K Opus = fits $300.

**A3.** Batch API. Workflow per contract: chain (extract clauses → compare to template → emit deviations JSON). Use Haiku for clause extraction, Sonnet for comparison. Run nightly. ~50% savings via Batch.

**A4.** Sectioning pattern. Haiku generates 3 candidates in parallel. Opus picks the best with a brief rubric. Cache the brand voice rules. Or skip the picker by deploying all 3 to A/B test buckets.

**A5.** Orchestrator-workers. Opus plans steps (read ticket → search codebase → read affected files → write diff). Sonnet workers execute each step with tools. Strict file-write sandbox; PR must be reviewed by human before merge. `max_steps=20`. Token budget cap.

**A7.** Chain: extract clauses → compare each to policy → propose redlines → assemble. Use tool-use-as-formatter to emit `[{clause, original, suggested, rationale}]`. Sonnet throughout; Opus for the final coherence pass if needed.

**A11.** Router (Haiku) for tagging; second Haiku call for sentiment; cache the static tag taxonomy in the system prompt. Prefill `{` and use tool-as-formatter for strict JSON. Cost ~ Haiku × 50K/month — small.

**A12.** Orchestrator-workers + evaluator-optimizer. Opus plans sections. Sonnet workers each do a mini-RAG over the 200 PDFs in parallel. Opus integrates. Then evaluator-optimizer loop to polish until a rubric (citations present, no claims unsupported) passes.

**A14.** Chain: pull positions (tool) → assess risk (Sonnet) → recommend (Sonnet) → draft memo (Opus). Each stage gated; human approval before sending. Audit log. Cache the risk policy rules.

**A15.** Missing **allow-list** / **confirmation** on `delete_customer`. Add: `tool_choice` restricted to non-destructive tools by default; destructive tools require an explicit human-in-the-loop step.

**A19.** No `max_steps`. No token budget. Possibly no "ask the user when stuck" instruction. Add all three. Also log step transitions.

**A25.** Per call: model id, route taken, parent agent id, step number, input tokens (cached/non-cached split), output tokens, latency, `stop_reason`, tools called (name, args hash, success, latency), retrieval ids + ranks, user session (non-PII), error class. Trace ID for correlating multi-step chains. Without this you cannot debug a regression.
