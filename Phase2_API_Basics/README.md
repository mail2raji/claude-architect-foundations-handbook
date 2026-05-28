# Phase 2 — Working with the Claude API

**Maps to:** Skilljar "Getting started with Claude" (16 lessons). **Exam weight: ~15%.**
**Goal:** Confidently call the Messages API for chat, streaming, vision, and structured output.

---

## 2.1 The Messages API in one diagram

```
┌──────────────────────────────────────────────────────────────────┐
│  client.messages.create(                                         │
│     model       = "claude-sonnet-4-5",   ← which Claude          │
│     max_tokens  = 1024,                  ← cap on output         │
│     system      = "You are a SOC analyst.",  ← persona/rules     │
│     temperature = 0.0,                   ← 0=deterministic, 1=creative │
│     messages    = [                                              │
│        {"role": "user",      "content": "..."},                  │
│        {"role": "assistant", "content": "..."},                  │
│        {"role": "user",      "content": "..."}   ← always ends user │
│     ],                                                           │
│     stream      = False,                                         │
│     tools       = [...],   # Phase 4                             │
│  )                                                               │
└──────────────────────────────────────────────────────────────────┘
```

Three roles only: **`system`** (one, top-level), **`user`**, **`assistant`** — and `messages` must **alternate user/assistant** and **end with user**.

`content` can be a **string** *or* a **list of content blocks** (text, image, tool_use, tool_result, document). Content blocks are the more flexible form — Phases 4 and 5 lean on them.

---

## 2.2 Hands-on examples (work through in order)

| # | File | What you'll learn |
|---|---|---|
| 1 | [`01_first_message.py`](01_first_message.py) | Single-turn request, reading the response object |
| 2 | [`02_multi_turn.py`](02_multi_turn.py) | Maintain conversation history; CLI chatbot |
| 3 | [`03_system_prompt.py`](03_system_prompt.py) | Persona/rules via `system`; temperature |
| 4 | [`04_streaming.py`](04_streaming.py) | Token-by-token UX (`with client.messages.stream(...)`) |
| 5 | [`05_structured_output.py`](05_structured_output.py) | Two reliable JSON tactics: prefilling + Pydantic |
| 6 | [`06_vision.py`](06_vision.py) | Image content blocks (network-diagram analysis) |
| 7 | [`07_stop_reasons_and_errors.py`](07_stop_reasons_and_errors.py) | `stop_reason`, retries, rate limits |

Run them one at a time. Read the source first, predict the output, then run.

---

## 2.3 Key concepts called out

### Roles & turn alternation
`messages` must alternate user/assistant. You can't have two `user` messages in a row. You CAN merge them into one string if needed.

### `system` vs `user`
- `system` = the **persona, rules, constraints** that apply to the whole conversation.
- `user` = what the user said in this turn.

> **Anti-pattern:** putting rules in the user message. Hostile users can override "rules" they see in the user role. System role is the architectural place for guardrails.

### `max_tokens`
Caps OUTPUT only. If output hits the cap, `stop_reason == "max_tokens"` and you must continue manually. Always set this — protects your bill from runaway loops.

### `temperature`
- `0.0` → near-deterministic. Use for classification, extraction, evaluation, tool routing.
- `0.7–1.0` → creative. Use for brainstorming, marketing copy.
- Default `1.0`. Most production code sets `0` explicitly.

### `stop_reason`
| Value | Meaning | Architect action |
|---|---|---|
| `end_turn` | Model finished naturally | All good |
| `max_tokens` | Hit your cap | Increase cap or chain another call |
| `stop_sequence` | Hit a custom stop string you passed | Expected |
| `tool_use` | Model wants to call a tool | See Phase 4 |
| `pause_turn` | Reserved for long-running flows | Resume by re-sending the convo |

### Streaming
Two modes:
- **Non-streaming** (`stream=False`) — get full response at once. Simplest.
- **Streaming** (`with client.messages.stream(...) as s:`) — get deltas in real time. Necessary for chat UX.

### Structured output (extremely common exam topic)
Two reliable techniques:

1. **Prefilling**: end the assistant turn with `{` so Claude *must* continue JSON.
2. **Tool use as JSON formatter**: define a tool whose `input_schema` is your desired JSON shape; force `tool_choice={"type":"tool","name":"..."}`. This is the **most reliable** technique.

---

## 2.4 Real-world scenario

> **Build a "log triage" microservice.** Ops sends raw firewall + auth logs over HTTPS. Your service must return JSON `{severity, category, suggested_action}`.
>
> - Single-turn ✔ (no chat needed)
> - System prompt with policy ✔
> - `temperature=0` ✔ (deterministic)
> - Tool-use-as-formatter for guaranteed JSON ✔ (Phase 4)
> - Stream? No (machine-to-machine).
>
> You'll implement the toy version of this in `05_structured_output.py` and the full version with tools in Phase 4.

---

## 2.5 Exercises

See [`exercises.md`](exercises.md).

## 2.6 Mini quiz (answer mentally before peeking)

1. What are the three valid roles in `messages`?
2. Why must `messages` end with a `user` turn?
3. Which parameter caps output length?
4. Which `stop_reason` means Claude wants to call a tool?
5. Name the two reliable techniques to get strict JSON out of Claude.

Answers at the bottom of [`exercises.md`](exercises.md).

Next → [Phase 3: Prompt Engineering & Evaluation](../Phase3_Prompt_Engineering/README.md)
