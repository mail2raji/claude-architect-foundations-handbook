# Domain 3 — Claude Code Configuration & Workflows

*Was Phase 8.* **Cert weight: 20%.**

**Maps to:** Skilljar "Claude Code & Computer Use" (8 lessons). **Exam weight: ~3%.**
**Goal:** Awareness-level understanding of two Anthropic-built agentic surfaces.

This phase is shorter — the exam tests **concepts**, not coding from scratch.

---

## 8.1 Claude Code

**What it is:** An Anthropic-built terminal CLI that runs Claude as an autonomous coding agent on your local machine.

**Mental model:** A ReAct agent (Phase 7) whose tools are `bash`, `text_editor`, `glob`, `grep`, plus optional MCP servers, plus subagents and skills.

**Key features to recognize on the exam:**

| Feature | What it does |
|---|---|
| **Skills** | Reusable markdown instructions (`SKILL.md`) automatically applied when relevant. Phase 8 reference: `introduction-to-agent-skills` course on Skilljar. |
| **Subagents** | Spawn a separate Claude session to handle a side-task (e.g., "Explore", "AzureCostOptimize") without polluting the main context. |
| **MCP integration** | Add any MCP server from Phase 6 — appears as tools instantly. |
| **Custom commands / `AGENTS.md`** | Repo-level instructions Claude Code reads on startup. |
| **Memory** | `/memories/` scopes: user, session, repo. (You already have one in this workspace.) |
| **Plan / Edit / Apply modes** | Determinism vs autonomy knobs. |

**When to use Claude Code vs the API directly:**

- **Claude Code** — you're an engineer at your terminal, want a pair-programmer that can touch files, run tests, and iterate.
- **API directly** — you're building a *product* that contains Claude.

**Real-world scenario:** *Refactor a 12-file PowerShell module to use a shared logging helper.* Claude Code can plan it, edit all files, run a linter, and report back. With the API alone you'd hand-roll the whole agent.

> Reference course: https://anthropic.skilljar.com/claude-code-in-action

---

## 8.2 Computer Use

**What it is:** A *tool* (`computer_use`) that lets Claude control a virtual machine's **mouse, keyboard, and screen**. Claude sees screenshots, decides clicks, types, and submits.

**Architecture (memorize):**

```
┌──────────┐  click(x,y) / type(...)   ┌──────────────┐
│  CLAUDE  │ ────────────────────────► │  SANDBOX VM  │
│          │ ◄──── screenshot ──────── │ (your code   │
└──────────┘                           │  takes shots │
                                       │  & executes) │
                                       └──────────────┘
```

You provide the VM and a thin executor. Anthropic provides the model and the tool schema.

**Use cases:**
- Browser automation where there is no API.
- Legacy desktop app automation.
- QA testing of UI flows.

**Critical safety knobs:**
- Run in a **sandbox** — never on production hosts.
- **Allow-list** of URLs / apps.
- **Confirm-before-act** for risky actions (sending email, money transfers).
- Strict **prompt-injection** defense: hostile websites can try to manipulate the model.

**Real-world scenario:** *Fill 200 supplier-onboarding forms on a vendor portal that has no API.* Spin up a Linux VM with a browser, give Claude the `computer_use` tool, and let it loop with a per-form approval gate.

---

## 8.3 Hands-on (light)

No runnable code in this phase — those tools require a VM (Computer Use) or a CLI install (Claude Code). Instead:

- Install **Claude Code** locally and run `claude` in your workspace. Ask it to "explain the architecture of `Send-EscalationEmail.ps1`". Read the result. That tells you 80% of what the exam cares about.
- Open the **Claude Code in Action** Skilljar course (free) for the polished walkthrough.

---

## 8.4 Exam tips

- Claude Code = local terminal agent.
- Computer Use = mouse/keyboard tool — **sandbox** required.
- Both are **agents under the hood** — every Phase 7 safety knob applies.
- Computer Use is **vision-based** — it relies on screenshots.

Next → [Domain 4a: Foundations, Setup & the Claude API](../Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/README.md)
