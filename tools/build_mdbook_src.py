"""
Build the mdBook source tree under `mdbook/src/` from the canonical chapter
folders.

The source folders are organised by Claude Certified Architect — Foundations
exam domain (Domain1_AgentArchitecture_27pct/, Domain2_ToolDesign_MCP_18pct/, ...).
Pre-domain foundations and post-domain exam-prep content have been absorbed
into the relevant domain folders so the source tree is one-to-one with the
five exam domains.

The source folders stay as-is so readers browsing GitHub see the layout they
expect. This script is the bridge: it copies the right chapter content into
mdBook's expected `src/` directory and writes `SUMMARY.md`.

Run locally:
    python tools/build_mdbook_src.py

GitHub Actions runs the same script before `mdbook build`.
"""

from __future__ import annotations

import posixpath
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "mdbook" / "src"

# (chapter_no, source_dir, chapter_title, extras_in_order)
# Chapter order mirrors the on-disk Domain1..Domain5 folder layout so the
# published site, the README's folder list, and the appendices all agree.
# Each subfolder under a Domain*/ root is rendered as its own chapter so the
# builder can keep its one-folder-per-chapter contract.
CHAPTERS: list[tuple[str, str, str, list[str]]] = [
    ("1", "Domain1_AgentArchitecture_27pct",                                      "Domain 1 \u2014 Agent architecture & orchestration",    ["01_workflows_vs_agents.md", "exercises.md"]),
    ("2", "Domain2_ToolDesign_MCP_18pct/tool_use",                                "Domain 2a \u2014 Tool use (function calling)",          ["exercises.md"]),
    ("3", "Domain2_ToolDesign_MCP_18pct/mcp",                                     "Domain 2b \u2014 Model Context Protocol (MCP)",         ["01_mcp_concepts.md", "exercises.md"]),
    ("4", "Domain3_ClaudeCode_Workflows_20pct",                                   "Domain 3 \u2014 Claude Code configuration & workflows", []),
    ("5", "Domain4_PromptEngineering_StructuredOutput_20pct/api_basics",          "Domain 4a \u2014 Foundations, setup & the Claude API",  ["00_foundations.md", "00_setup_notes.md", "exercises.md"]),
    ("6", "Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering",  "Domain 4b \u2014 Prompt engineering and evaluation",    ["exercises.md"]),
    ("7", "Domain5_ContextMgmt_Reliability_15pct",                                "Domain 5 \u2014 Context management & retrieval (RAG)",  ["exercises.md"]),
]

# Per-domain exam_prep/ folders are aggregated into one appendix per domain.
APPENDICES: list[tuple[str, str, str, list[str]]] = [
    ("A", "Domain1_AgentArchitecture_27pct/exam_prep", "Exam prep \u2014 Domain 1",
        ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md"]),
    ("B", "Domain2_ToolDesign_MCP_18pct/tool_use/exam_prep", "Exam prep \u2014 Domain 2a (tools)",
        ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md"]),
    ("C", "Domain2_ToolDesign_MCP_18pct/mcp/exam_prep", "Exam prep \u2014 Domain 2b (MCP)",
        ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md"]),
    ("D", "Domain3_ClaudeCode_Workflows_20pct/exam_prep", "Exam prep \u2014 Domain 3",
        ["glossary.md", "final_checklist.md", "practice_questions.md", "exercises_harder.md", "advanced_scenarios.md"]),
    ("E", "Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/exam_prep", "Exam prep \u2014 Domain 4a (API)",
        ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md", "answers_foundations_exercise.md"]),
    ("F", "Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/exam_prep", "Exam prep \u2014 Domain 4b (prompts)",
        ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md"]),
    ("G", "Domain5_ContextMgmt_Reliability_15pct/exam_prep", "Exam prep \u2014 Domain 5",
        ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md"]),
]


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def shift_headings(text: str, levels: int) -> str:
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence:
            m = re.match(r"^(#{1,6})(\s)", line)
            if m:
                hashes = m.group(1)
                new_level = min(len(hashes) + levels, 6)
                line = "#" * new_level + line[len(hashes):]
        out.append(line)
    return "\n".join(out)


def rewrite_links(text: str, chapter_subdir: str) -> str:
    """
    Inside a chapter README, links like `01_first_message.py` or
    `(../Domain1_AgentArchitecture_27pct/README.md)` won't resolve under mdbook/src.
    We turn them into absolute GitHub URLs so users can still click through.
    Relative paths (including ``../``) are resolved against ``chapter_subdir``
    using ``posixpath.normpath`` so they stay accurate after upward traversal.
    """
    base = "https://github.com/mail2raji/claude-architect-foundations-handbook/blob/main"

    def repl(match: re.Match) -> str:
        label, target = match.group(1), match.group(2)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            return match.group(0)
        # Strip anchors
        anchor = ""
        if "#" in target:
            target, anchor = target.split("#", 1)
            anchor = "#" + anchor
        # Resolve relative path against the chapter folder using POSIX rules so
        # `../foo` inside Domain4/api_basics becomes Domain4/foo (not foo).
        if target:
            resolved = posixpath.normpath(posixpath.join(chapter_subdir, target))
        else:
            resolved = chapter_subdir
        return f"[{label}]({base}/{resolved}{anchor})"

    # markdown link pattern: [label](target)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


def write_chapter(no: str, src_dir: str, title: str, extras: list[str]) -> str:
    """Returns the filename relative to mdbook/src for SUMMARY.md."""
    folder = ROOT / src_dir
    out_dir = SRC / f"ch{no.zfill(2)}"
    out_dir.mkdir(parents=True, exist_ok=True)

    parts: list[str] = [f"# Chapter {no}. {title}\n"]
    readme = read(folder / "README.md")
    if readme:
        parts.append(shift_headings(rewrite_links(readme, src_dir), 1))

    for extra in extras:
        content = read(folder / extra)
        if not content:
            continue
        parts.append(f"\n\n## {Path(extra).stem.replace('_', ' ').title()}\n")
        parts.append(shift_headings(rewrite_links(content, src_dir), 1))

    code = sorted(p.name for p in folder.glob("*.py"))
    if code:
        parts.append("\n\n## Code samples in this chapter\n")
        base = f"https://github.com/mail2raji/claude-architect-foundations-handbook/blob/main/{src_dir}"
        for cf in code:
            parts.append(f"- [`{cf}`]({base}/{cf})")

    out_path = out_dir / "index.md"
    out_path.write_text("\n".join(parts), encoding="utf-8")
    return f"ch{no.zfill(2)}/index.md"


def write_appendix(letter: str, src_dir: str, title: str, files: list[str]) -> str:
    folder = ROOT / src_dir
    out_dir = SRC / f"appendix-{letter.lower()}"
    out_dir.mkdir(parents=True, exist_ok=True)

    parts: list[str] = [f"# Appendix {letter}. {title}\n"]
    readme = read(folder / "README.md")
    if readme:
        parts.append(shift_headings(rewrite_links(readme, src_dir), 1))
    for f in files:
        content = read(folder / f)
        if not content:
            continue
        parts.append(f"\n\n## {Path(f).stem.replace('_', ' ').title()}\n")
        parts.append(shift_headings(rewrite_links(content, src_dir), 1))

    code = sorted(p.name for p in folder.glob("*.py"))
    if code:
        parts.append("\n\n## Code samples\n")
        base = f"https://github.com/mail2raji/claude-architect-foundations-handbook/blob/main/{src_dir}"
        for cf in code:
            parts.append(f"- [`{cf}`]({base}/{cf})")

    out_path = out_dir / "index.md"
    out_path.write_text("\n".join(parts), encoding="utf-8")
    return f"appendix-{letter.lower()}/index.md"


def write_front_matter() -> tuple[str, str, str]:
    """Copy the three front matter files into mdbook/src and return their paths."""
    mapping = {
        "title.md":      ROOT / "book" / "00_title.md",
        "preface.md":    ROOT / "book" / "01_preface.md",
        "how-to-use.md": ROOT / "book" / "02_how_to_use.md",
    }
    for dest_name, src_path in mapping.items():
        if src_path.exists():
            (SRC / dest_name).write_text(read(src_path), encoding="utf-8")
    return "title.md", "preface.md", "how-to-use.md"


def write_intro() -> str:
    text = """<div class="hero">
  <p class="hero-eyebrow">Claude Certified Architect &mdash; Foundations</p>
  <h1 class="hero-title">The Hands-On Handbook</h1>
  <p class="hero-tag">From zero to production-grade agents in five domains.</p>
  <p class="hero-badges">
    <a href="https://github.com/mail2raji/claude-architect-foundations-handbook/actions/workflows/pages.yml"><img alt="Build &amp; deploy" src="https://github.com/mail2raji/claude-architect-foundations-handbook/actions/workflows/pages.yml/badge.svg"></a>
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue">
    <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-3776ab?logo=python&logoColor=white">
    <img alt="Anthropic Claude" src="https://img.shields.io/badge/Anthropic-Claude-d4915d">
  </p>
</div>

---

## What you'll learn

A hands-on path through every domain of the **Claude Certified Architect &mdash; Foundations** exam &mdash; with **42&nbsp;runnable Python scripts**, **per-script kid-friendly `.lab.md` guides**, **practice questions**, and **production-grade capstones**.

<div class="roadmap">
  <div class="roadmap-card"><span class="roadmap-num">1</span><strong>Agent architecture</strong><span class="roadmap-weight">27%</span></div>
  <div class="roadmap-card"><span class="roadmap-num">2</span><strong>Tools &amp; MCP</strong><span class="roadmap-weight">18%</span></div>
  <div class="roadmap-card"><span class="roadmap-num">3</span><strong>Claude Code</strong><span class="roadmap-weight">20%</span></div>
  <div class="roadmap-card"><span class="roadmap-num">4</span><strong>Prompts &amp; API</strong><span class="roadmap-weight">20%</span></div>
  <div class="roadmap-card"><span class="roadmap-num">5</span><strong>Context &amp; RAG</strong><span class="roadmap-weight">15%</span></div>
  <div class="roadmap-card roadmap-card-end"><span class="roadmap-num">&#10003;</span><strong>Exam-ready</strong><span class="roadmap-weight">100%</span></div>
</div>

---

## Chapters at a glance

| # | Chapter | Exam weight | Highlights |
|---|---------|------------|------------|
| 1 | [Domain 1 &mdash; Agent architecture & orchestration](ch01/index.md) | **27%** | Chain / Router / Parallel / Orchestrator / Evaluator / ReAct + 3 capstones |
| 2 | [Domain 2a &mdash; Tool use (function calling)](ch02/index.md) | (part of 18%) | Single & parallel tools, multi-turn loops, IT-triage agent |
| 3 | [Domain 2b &mdash; Model Context Protocol (MCP)](ch03/index.md) | (part of 18%) | Build a FastMCP server, write a client, bridge MCP &harr; Claude |
| 4 | [Domain 3 &mdash; Claude Code configuration & workflows](ch04/index.md) | **20%** | CLAUDE.md, settings, hooks, sub-agents, code-review capstone |
| 5 | [Domain 4a &mdash; Foundations, setup & the Claude API](ch05/index.md) | (part of 20%) | First call &rarr; streaming &rarr; vision &rarr; structured output |
| 6 | [Domain 4b &mdash; Prompt engineering & evaluation](ch06/index.md) | (part of 20%) | XML tags, few-shot, CoT, prefilling, LLM-as-judge, eval-harness capstone |
| 7 | [Domain 5 &mdash; Context management & retrieval (RAG)](ch07/index.md) | **15%** | Chunking, embeddings, BM25 hybrid, reranking, contextual retrieval, compliance-RAG capstone |

Plus seven **[Appendices A&ndash;G](appendix-a/index.md)** &mdash; one per domain &mdash; with glossaries, final checklists, advanced scenarios, and **90+ practice questions**.

---

## Quick start

```bash
git clone https://github.com/mail2raji/claude-architect-foundations-handbook.git
cd claude-architect-foundations-handbook
python -m venv .venv && source .venv/bin/activate   # on Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env                                # then paste your ANTHROPIC_API_KEY
python Domain1_AgentArchitecture_27pct/02_chain_workflow.py
```

Each runnable script has a sibling **`<name>.lab.md`** that explains *what* it does and *why* in plain English &mdash; aimed at someone seeing the file for the first time.

---

## How to use this site

- **Sidebar** &mdash; jump between chapters and appendices.
- **Magnifying glass** (top-left) &mdash; full-text search across the whole book.
- **Pencil icon** (top-right) &mdash; edit any page on GitHub.
- **Sun / moon icon** &mdash; light / dark theme (the navy theme is built for evenings).
- Prefer offline? Every chapter is also available as a single **[BOOK.md](https://github.com/mail2raji/claude-architect-foundations-handbook/blob/main/BOOK.md)** file in the repo.

---

## About

- **Author:** [@mail2raji](https://github.com/mail2raji)
- **Source:** <https://github.com/mail2raji/claude-architect-foundations-handbook>
- **License:** [MIT](https://github.com/mail2raji/claude-architect-foundations-handbook/blob/main/LICENSE)
- **Contributions** of typo fixes, extra exercises, or fresh capstones are warmly welcomed &mdash; see [CONTRIBUTING.md](https://github.com/mail2raji/claude-architect-foundations-handbook/blob/main/CONTRIBUTING.md).

> *Built with [mdBook](https://rust-lang.github.io/mdBook/) &middot; deployed by GitHub Actions on every push to `main`.*
"""
    (SRC / "introduction.md").write_text(text, encoding="utf-8")
    return "introduction.md"


def write_summary(intro: str, fm: tuple[str, str, str],
                  chapter_paths: list[tuple[str, str, str]],
                  appendix_paths: list[tuple[str, str, str]]) -> None:
    title_md, preface_md, howto_md = fm
    lines: list[str] = ["# Summary\n", f"[Introduction]({intro})\n"]
    lines.append("# Front matter\n")
    lines.append(f"- [Title page]({title_md})")
    lines.append(f"- [Preface]({preface_md})")
    lines.append(f"- [How to use this handbook]({howto_md})")
    lines.append("\n# Chapters\n")
    for no, title, path in chapter_paths:
        lines.append(f"- [Chapter {no}. {title}]({path})")
    lines.append("\n# Appendices\n")
    for letter, title, path in appendix_paths:
        lines.append(f"- [Appendix {letter}. {title}]({path})")
    (SRC / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if SRC.exists():
        shutil.rmtree(SRC)
    SRC.mkdir(parents=True, exist_ok=True)

    intro = write_intro()
    fm = write_front_matter()

    chapter_paths: list[tuple[str, str, str]] = []
    for no, src_dir, title, extras in CHAPTERS:
        p = write_chapter(no, src_dir, title, extras)
        chapter_paths.append((no, title, p))

    appendix_paths: list[tuple[str, str, str]] = []
    for letter, src_dir, title, files in APPENDICES:
        p = write_appendix(letter, src_dir, title, files)
        appendix_paths.append((letter, title, p))

    write_summary(intro, fm, chapter_paths, appendix_paths)

    files = sum(1 for _ in SRC.rglob("*.md"))
    print(f"Built mdBook source: {SRC}  ({files} markdown files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
