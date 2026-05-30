# Domain 4 — Prompt Engineering & Structured Output

**Cert weight:** 20% of the Claude Certified Architect — Foundations exam.
**Goal:** Drive Claude reliably with well-structured prompts and produce machine-parseable output you can validate, route on, and rerun deterministically.

> This domain merges the original Phase 2 (Claude API basics) and Phase 3 (Prompt engineering & evaluation) modules. The folder layout is:
>
> - [`api_basics/`](api_basics/README.md) — the **mechanics** of the Messages API: messages, roles, system prompts, streaming, structured output, vision, `stop_reason` handling.
> - [`prompt_engineering/`](prompt_engineering/README.md) — the **technique catalogue**: XML tags, few-shot, chain-of-thought, prefilling, evaluation frameworks, and LLM-as-judge.

Both subfolders are runnable end-to-end and are referenced by [LAB_GUIDE.md](../LAB_GUIDE.md) Domain 4 labs (4.1 – 4.9).

---

## What the exam expects you to be able to do

| Exam objective | Anchor file |
|---|---|
| Build a multi-turn conversation with correct `assistant`/`user` roles | [`api_basics/02_multi_turn.py`](api_basics/02_multi_turn.py) |
| Use system prompts to set persona, rules, and constraints | [`api_basics/03_system_prompt.py`](api_basics/03_system_prompt.py) |
| Stream tokens & rebuild deltas client-side | [`api_basics/04_streaming.py`](api_basics/04_streaming.py) |
| Coerce a strict JSON schema out of Claude | [`api_basics/05_structured_output.py`](api_basics/05_structured_output.py) |
| Send images alongside text (vision) | [`api_basics/06_vision.py`](api_basics/06_vision.py) |
| Interpret every `stop_reason` value and handle errors | [`api_basics/07_stop_reasons_and_errors.py`](api_basics/07_stop_reasons_and_errors.py) |
| Use XML tags to separate instruction, data, and examples | [`prompt_engineering/01_xml_tags.py`](prompt_engineering/01_xml_tags.py) |
| Apply few-shot exemplars to lift accuracy | [`prompt_engineering/02_few_shot.py`](prompt_engineering/02_few_shot.py) |
| Trigger chain-of-thought via `<thinking>` tags | [`prompt_engineering/03_chain_of_thought.py`](prompt_engineering/03_chain_of_thought.py) |
| Prefill the assistant turn to lock format | [`prompt_engineering/04_prefilling.py`](prompt_engineering/04_prefilling.py) |
| Build an eval harness with a ground-truth dataset | [`prompt_engineering/05_eval_framework.py`](prompt_engineering/05_eval_framework.py) |
| Use LLM-as-judge for open-ended outputs | [`prompt_engineering/06_llm_judge.py`](prompt_engineering/06_llm_judge.py) |

---

## The "structured output" pipeline

```
┌──────────────┐    well-named     ┌──────────────┐   prefill   ┌──────────────┐
│ XML-tagged   │ ──── examples ──► │ Few-shot     │ ── "{"  ──► │  Claude      │
│ prompt       │                   │ exemplars    │             │              │
└──────────────┘                   └──────────────┘             └──────┬───────┘
                                                                       │ JSON
                                                                       ▼
                                                              ┌──────────────┐
                                                              │  Pydantic    │
                                                              │  / JSON-     │
                                                              │  Schema val. │
                                                              └──────┬───────┘
                                                            valid ◄──┴──► retry-with-feedback
```

`api_basics/05_structured_output.py` teaches the validation half.
`prompt_engineering/04_prefilling.py` teaches the lock-the-format half.
The retry-with-feedback loop is built in [LAB_GUIDE.md](../LAB_GUIDE.md) Lab 4.4.

---

## Recommended order

1. Read this README.
2. Work through [`api_basics/README.md`](api_basics/README.md) and run files 01 → 07.
3. Do the [`api_basics/exercises.md`](api_basics/exercises.md).
4. Move to [`prompt_engineering/README.md`](prompt_engineering/README.md), run files 01 → 06.
5. Do the [`prompt_engineering/exercises.md`](prompt_engineering/exercises.md).
6. Return to [LAB_GUIDE.md](../LAB_GUIDE.md) Domain 4 labs for synthesis exercises (retry-with-feedback, multi-instance reviewer, judge-evaluator).

---

Next → [Domain 2 — Tool Design & MCP Integration](../Domain2_ToolDesign_MCP_18pct/README.md)
