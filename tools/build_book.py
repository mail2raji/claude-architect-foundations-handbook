"""
Build BOOK.md by concatenating book front matter + each phase's content
into a single navigable file with a generated table of contents.

Usage:
    python tools/build_book.py

The output BOOK.md sits at the repo root.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (chapter_no, source_dir, chapter_title, extra_md_in_order, list_code_files)
# Chapter order now follows the Claude Certified Architect — Foundations exam domains.
# Each subfolder under a Domain*/ root is rendered as its own chapter so the
# builder can keep its one-folder-per-chapter contract.
CHAPTERS: list[tuple[str, str, str, list[str], bool]] = [
    ("1", "Domain1_AgentArchitecture_27pct",                                      "Domain 1 \u2014 Agent Architecture & Orchestration (27%)",   ["01_workflows_vs_agents.md", "exercises.md"],     True),
    ("2", "Domain2_ToolDesign_MCP_18pct/tool_use",                                "Domain 2a \u2014 Tool Use / Function Calling",               ["exercises.md"],                                  True),
    ("3", "Domain2_ToolDesign_MCP_18pct/mcp",                                     "Domain 2b \u2014 Model Context Protocol (MCP) (18%)",        ["01_mcp_concepts.md", "exercises.md"],            True),
    ("4", "Domain3_ClaudeCode_Workflows_20pct",                                   "Domain 3 \u2014 Claude Code Configuration & Workflows (20%)", [],                                               False),
    ("5", "Domain4_PromptEngineering_StructuredOutput_20pct/api_basics",          "Domain 4a \u2014 Foundations, Setup & the Claude API",       ["00_foundations.md", "00_setup_notes.md", "exercises.md"], True),
    ("6", "Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering",  "Domain 4b \u2014 Prompt Engineering & Evaluation (20%)",     ["exercises.md"],                                  True),
    ("7", "Domain5_ContextMgmt_Reliability_15pct",                                "Domain 5 \u2014 Context Management & Retrieval / RAG (15%)", ["exercises.md"],                                  True),
]

# Each domain now carries its OWN exam_prep/ subfolder, so the old single
# 'Exam preparation' appendix is gone. We keep one appendix that aggregates
# the per-domain exam-prep material so a reader who wants a single 'study
# everything' file still has one.
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


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def shift_headings(text: str, levels: int) -> str:
    """Demote markdown headings by `levels` (cap at h6).
    Skip code fences."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```"):
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


def list_code_files(dir_path: Path) -> list[str]:
    return sorted(p.name for p in dir_path.glob("*.py"))


def build_chapter(no: str, src_dir: str, title: str, extras: list[str], with_code: bool) -> str:
    folder = ROOT / src_dir
    section_anchor = f"chapter-{no}-{slugify(title)}"
    parts: list[str] = [f"\n\n<a id='{section_anchor}'></a>\n\n# Chapter {no}. {title}\n"]
    parts.append(f"> Source folder: [`{src_dir}/`]({src_dir}/README.md)\n")

    readme = read(folder / "README.md")
    if readme:
        # demote so chapter h1 stays unique
        parts.append(shift_headings(readme, 1))

    for extra in extras:
        epath = folder / extra
        content = read(epath)
        if not content:
            continue
        parts.append(f"\n\n## {Path(extra).stem.replace('_', ' ').title()}\n")
        parts.append(shift_headings(content, 1))

    if with_code:
        code_files = list_code_files(folder)
        if code_files:
            parts.append("\n\n## Code samples in this chapter\n")
            for cf in code_files:
                parts.append(f"- [`{cf}`]({src_dir}/{cf})")

    return "\n".join(parts)


def build_appendix(letter: str, src_dir: str, title: str, files: list[str]) -> str:
    folder = ROOT / src_dir
    section_anchor = f"appendix-{letter.lower()}-{slugify(title)}"
    parts: list[str] = [f"\n\n<a id='{section_anchor}'></a>\n\n# Appendix {letter}. {title}\n"]
    parts.append(f"> Source folder: [`{src_dir}/`]({src_dir}/README.md)\n")
    readme = read(folder / "README.md")
    if readme:
        parts.append(shift_headings(readme, 1))
    for f in files:
        content = read(folder / f)
        if not content:
            continue
        parts.append(f"\n\n## {Path(f).stem.replace('_', ' ').title()}\n")
        parts.append(shift_headings(content, 1))
    # list code if any
    code_files = list_code_files(folder)
    if code_files:
        parts.append("\n\n## Code samples in this appendix\n")
        for cf in code_files:
            parts.append(f"- [`{cf}`]({src_dir}/{cf})")
    return "\n".join(parts)


def build_toc() -> str:
    lines = ["# Table of contents\n"]
    lines.append("## Front matter\n")
    lines.append("- [Title page](#title-page)")
    lines.append("- [Preface](#preface)")
    lines.append("- [How to use this handbook](#how-to-use-this-handbook)")
    lines.append("\n## Chapters\n")
    for no, src_dir, title, _, _ in CHAPTERS:
        anchor = f"chapter-{no}-{slugify(title)}"
        lines.append(f"- [Chapter {no}. {title}](#{anchor})")
    lines.append("\n## Appendices\n")
    for letter, _, title, _ in APPENDICES:
        anchor = f"appendix-{letter.lower()}-{slugify(title)}"
        lines.append(f"- [Appendix {letter}. {title}](#{anchor})")
    return "\n".join(lines)


def main() -> int:
    parts: list[str] = []

    parts.append("<a id='title-page'></a>\n")
    parts.append(read(ROOT / "book" / "00_title.md"))
    parts.append("\n\n<a id='preface'></a>\n")
    parts.append(read(ROOT / "book" / "01_preface.md"))
    parts.append("\n\n<a id='how-to-use-this-handbook'></a>\n")
    parts.append(read(ROOT / "book" / "02_how_to_use.md"))
    parts.append("\n\n---\n\n")
    parts.append(build_toc())
    parts.append("\n\n---\n")

    for no, src, title, extras, with_code in CHAPTERS:
        parts.append(build_chapter(no, src, title, extras, with_code))
        parts.append("\n\n---\n")

    for letter, src, title, files in APPENDICES:
        parts.append(build_appendix(letter, src, title, files))
        parts.append("\n\n---\n")

    parts.append("\n\n*Generated by `tools/build_book.py`. Re-run after editing any chapter.*\n")

    out_path = ROOT / "BOOK.md"
    out_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {out_path}  ({out_path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
