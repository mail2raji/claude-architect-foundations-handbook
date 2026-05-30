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

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "mdbook" / "src"

# (chapter_no, source_dir, chapter_title, extras_in_order)
# Chapter order now follows the Claude Certified Architect — Foundations exam domains.
# Each subfolder under a Domain*/ root is rendered as its own chapter so the
# builder can keep its one-folder-per-chapter contract.
CHAPTERS: list[tuple[str, str, str, list[str]]] = [
    ("1", "Domain4_PromptEngineering_StructuredOutput_20pct/api_basics",          "Domain 4a \u2014 Foundations, setup & the Claude API",  ["00_foundations.md", "00_setup_notes.md", "exercises.md"]),
    ("2", "Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering",  "Domain 4b \u2014 Prompt engineering and evaluation",    ["exercises.md"]),
    ("3", "Domain2_ToolDesign_MCP_18pct/tool_use",                                "Domain 2a \u2014 Tool use (function calling)",          ["exercises.md"]),
    ("4", "Domain5_ContextMgmt_Reliability_15pct",                                "Domain 5 \u2014 Context management & retrieval (RAG)",  ["exercises.md"]),
    ("5", "Domain2_ToolDesign_MCP_18pct/mcp",                                     "Domain 2b \u2014 Model Context Protocol (MCP)",         ["01_mcp_concepts.md", "exercises.md"]),
    ("6", "Domain1_AgentArchitecture_27pct",                                      "Domain 1 \u2014 Agent architecture & orchestration",    ["01_workflows_vs_agents.md", "exercises.md"]),
    ("7", "Domain3_ClaudeCode_Workflows_20pct",                                   "Domain 3 \u2014 Claude Code configuration & workflows", []),
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
        # Resolve relative to original chapter folder
        if target.startswith("../"):
            # link points outside the chapter folder
            resolved = target.lstrip("./")
        else:
            resolved = f"{chapter_subdir}/{target}" if target else chapter_subdir
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
    text = (
        "# Claude Certified Architect Foundations\n\n"
        "## The Hands-On Handbook\n\n"
        "*From zero to production-grade agents.*\n\n"
        "Welcome. This site is the rendered, searchable edition of the book.\n"
        "Use the sidebar to jump between chapters, or the magnifying-glass icon\n"
        "in the top-left to search the whole book.\n\n"
        "- Source repository: <https://github.com/mail2raji/claude-architect-foundations-handbook>\n"
        "- Single-file edition: see `BOOK.md` in the repo\n"
        "- License: MIT\n"
    )
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
