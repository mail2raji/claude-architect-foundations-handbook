# Phase 3 — Prompt Engineering & Evaluation

**Maps to:** Skilljar "Prompt engineering & evaluation" (16 lessons). **Exam weight: ~22% combined.**
**Goal:** Write reliable prompts AND prove they work with automated evals.

---

## 3.1 The 10 prompting techniques you must know

Anthropic teaches these as "the prompt engineering stack". Memorize the list — exam favorite.

| # | Technique | One-line rule |
|---|---|---|
| 1 | **Be clear & direct** | Say exactly what you want, like to a smart new hire. |
| 2 | **Use XML tags** | Delimit sections (`<task>`, `<context>`, `<example>`, `<rules>`). Claude was trained to respect them. |
| 3 | **System prompt for persona/rules** | Persona goes in `system`, the actual question in `user`. |
| 4 | **Multi-shot examples (few-shot)** | Show 2–5 input/output examples in `<examples>`. Improves consistency more than any other technique. |
| 5 | **Chain-of-thought (CoT)** | Ask Claude to "think step by step in `<thinking>` tags before answering". Big lift on math/reasoning. |
| 6 | **Prefilling** | Start the assistant turn (`{`, `<answer>`, `Step 1.`) to force a format. |
| 7 | **Role / persona prompting** | "You are a senior X" — improves quality. |
| 8 | **Chain prompts** | Decompose a hard task into N small Claude calls instead of one mega-prompt. |
| 9 | **Long context tricks** | Put **documents at the top**, the **question at the bottom**. Ask Claude to quote relevant snippets first. |
| 10 | **Be specific about output format** | "Reply in JSON with these keys…" and pair with prefilling or tool use. |

### XML-tag template (use this as your default)

```text
<task>
Summarize the document below into 5 bullet points for a CFO.
</task>

<rules>
- Each bullet ≤ 20 words.
- Use only facts from the <document>.
- If the document is empty, reply EMPTY.
</rules>

<document>
{{insert document here}}
</document>

<examples>
<example>
<document>… short test doc …</document>
<answer>
- bullet 1
- bullet 2
</answer>
</example>
</examples>

Now produce the answer in <answer> tags.
```

> **Exam trap:** XML tags do NOT need to be valid XML. Claude doesn't parse them — it just learned that `<tag>...</tag>` marks a section.

---

## 3.2 Chain-of-thought (CoT) — the single biggest reasoning lever

Ask Claude to think before answering:

```text
First, in <thinking> tags, work through the problem step by step.
Then in <answer> tags, give the final answer only.
```

Then parse out `<answer>...</answer>`. This typically improves accuracy on multi-step questions by **10–30 %**.

> Modern Claude models also support **extended thinking** (sometimes called *reasoning models*) where the API itself returns a separate `thinking` block. You enable it with `thinking={"type":"enabled","budget_tokens":...}`. Know the name for the exam.

---

## 3.3 Real-world scenario for prompting

> **Compliance ticket classifier.** You must classify each ticket into one of: `SOX`, `GDPR`, `HIPAA`, `Other`.
>
> A naive prompt gets ~80% accuracy. By adding (a) XML tags, (b) 5 few-shot examples, (c) `<thinking>` CoT, and (d) `temperature=0` you get 95%+. We measure all four versions in `03_eval_framework.py`.

---

## 3.4 Why evaluation matters

Prompts are software. Software needs tests. Without evals you have no idea if your "small tweak" to the prompt made the system better — or silently worse. **The Architect's responsibility is to set up evals before going to production.**

Anthropic teaches three eval flavors:

| Eval type | When to use | How |
|---|---|---|
| **Ground-truth (deterministic)** | When there is a single correct answer (classification, extraction) | Compare predicted vs. expected → accuracy/F1 |
| **LLM-as-judge** | Open-ended outputs (summaries, replies) — no single right answer | A second Claude call (often Opus) scores the output 1–5 against a rubric |
| **Code-grader / heuristic** | Format checks (valid JSON?), length, contains-PII?, etc. | A plain Python function |

A good production eval suite mixes all three.

### LLM-as-judge prompt template

```text
You are a strict grader.
<task>Score the answer 1-5 against the rubric.</task>
<rubric>
5 = perfect, addresses every required point, no hallucinations
4 = ...
1 = wrong or hallucinated
</rubric>
<question>{{q}}</question>
<answer>{{a}}</answer>
<expected_facts>{{facts}}</expected_facts>

First explain in <thinking>, then output a single integer 1-5 in <score>.
```

---

## 3.5 Hands-on examples

| # | File | Topic |
|---|---|---|
| 1 | [`01_xml_tags.py`](01_xml_tags.py) | Naive vs XML-structured prompt for ticket classification |
| 2 | [`02_few_shot.py`](02_few_shot.py) | Add 5 examples — watch accuracy jump |
| 3 | [`03_chain_of_thought.py`](03_chain_of_thought.py) | `<thinking>` tag + extract `<answer>` |
| 4 | [`04_prefilling.py`](04_prefilling.py) | Force a format (JSON, "Step 1.", etc.) |
| 5 | [`05_eval_framework.py`](05_eval_framework.py) | Ground-truth eval over a tiny dataset |
| 6 | [`06_llm_judge.py`](06_llm_judge.py) | LLM-as-judge for open-ended outputs |

Run them in order — they build on the same dataset.

---

## 3.6 Exercises

See [`exercises.md`](exercises.md).

## 3.7 Mini quiz

1. Which technique typically gives the biggest accuracy lift on a fixed prompt?
2. Where should documents go in a long prompt: top or bottom?
3. What does "prefilling" mean and how do you do it in the Messages API?
4. Name the three flavors of evals.
5. Why is `temperature=0` important for evals?

Answers at the bottom of [`exercises.md`](exercises.md).

Next → [Phase 4: Tool Use](../Phase4_Tool_Use/README.md)
