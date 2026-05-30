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

# Each chapter == one Domain*/ folder, mirroring the repo exactly.
# Schema: (chapter_no, parent_dir, chapter_title, named_subs)
#   named_subs -> ordered list of sub-folder names rendered as inline sections.
# Everything else (loose .md, exercises.md, .py + .lab.md pairs, capstones/)
# is auto-discovered by render_folder().
CHAPTERS: list[tuple[str, str, str, list[str]]] = [
    ("1", "Domain1_AgentArchitecture_27pct",
        "Domain 1 \u2014 Agent Architecture & Orchestration (27%)",
        []),
    ("2", "Domain2_ToolDesign_MCP_18pct",
        "Domain 2 \u2014 Tool Design & MCP Integration (18%)",
        ["tool_use", "mcp"]),
    ("3", "Domain3_ClaudeCode_Workflows_20pct",
        "Domain 3 \u2014 Claude Code Configuration & Workflows (20%)",
        []),
    ("4", "Domain4_PromptEngineering_StructuredOutput_20pct",
        "Domain 4 \u2014 Prompt Engineering & Structured Output (20%)",
        ["api_basics", "prompt_engineering"]),
    ("5", "Domain5_ContextMgmt_Reliability_15pct",
        "Domain 5 \u2014 Context Management & Retrieval / RAG (15%)",
        []),
]

# One appendix per Domain. Each appendix can pull from multiple exam_prep/ paths.
APPENDICES: list[tuple[str, list[tuple[str, list[str]]], str]] = [
    ("A",
        [("Domain1_AgentArchitecture_27pct/exam_prep",
            ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md"])],
        "Exam prep \u2014 Domain 1"),
    ("B",
        [("Domain2_ToolDesign_MCP_18pct/tool_use/exam_prep",
            ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md"]),
         ("Domain2_ToolDesign_MCP_18pct/mcp/exam_prep",
            ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md"])],
        "Exam prep \u2014 Domain 2"),
    ("C",
        [("Domain3_ClaudeCode_Workflows_20pct/exam_prep",
            ["glossary.md", "final_checklist.md", "practice_questions.md", "exercises_harder.md", "advanced_scenarios.md"])],
        "Exam prep \u2014 Domain 3"),
    ("D",
        [("Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/exam_prep",
            ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md", "answers_foundations_exercise.md"]),
         ("Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/exam_prep",
            ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md"])],
        "Exam prep \u2014 Domain 4"),
    ("E",
        [("Domain5_ContextMgmt_Reliability_15pct/exam_prep",
            ["glossary.md", "final_checklist.md", "practice_questions.md", "practice_questions_setC.md", "exercises_harder.md", "advanced_scenarios.md"])],
        "Exam prep \u2014 Domain 5"),
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


SPECIAL_MD = {"README.md", "exercises.md"}


def list_loose_md(folder: Path) -> list[str]:
    return sorted(
        p.name for p in folder.iterdir()
        if p.is_file()
        and p.suffix == ".md"
        and p.name not in SPECIAL_MD
        and not p.name.endswith(".lab.md")
    )


def code_table(folder: Path, src_dir: str) -> list[str]:
    pys = sorted(p.name for p in folder.glob("*.py"))
    if not pys:
        return []
    out = [
        "| # | Script | What it does | Plain-English lab guide |",
        "|---|--------|--------------|--------------------------|",
    ]
    for i, py in enumerate(pys, 1):
        lab = py[:-3] + ".lab.md"
        lab_full = folder / lab
        lab_cell = f"[`{lab}`]({src_dir}/{lab})" if lab_full.exists() else "&mdash;"
        summary = lab_one_liner(lab_full) or "&mdash;"
        out.append(f"| {i} | [`{py}`]({src_dir}/{py}) | {summary} | {lab_cell} |")
    return out


def lab_one_liner(lab_path: Path) -> str:
    if not lab_path.exists():
        return ""
    text = lab_path.read_text(encoding="utf-8")
    m = re.search(r"^##\s+What this script does\s*\n+([^\n#][^\n]*)",
                  text, re.MULTILINE)
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip().replace("|", "\\|")


_README_TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def strip_duplicate_readme_h1(text: str, chapter_title: str) -> str:
    m = _README_TITLE_RE.match(text)
    if not m:
        return text
    readme_title = m.group(1).strip()
    chap_words = re.sub(r"[^\w\s]", " ", chapter_title).lower().split()
    readme_words = re.sub(r"[^\w\s]", " ", readme_title).lower().split()
    overlap = len(set(chap_words) & set(readme_words))
    if overlap >= max(2, len(readme_words) // 2):
        rest = text[m.end():]
        return rest.lstrip("\n")
    return text


def number_top_sections(text: str, chapter_no: str, min_level: int = 2) -> str:
    out: list[str] = []
    in_fence = False
    counter = 0
    target = "#" * min_level + " "
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line); continue
        if not in_fence and line.startswith(target) and not line.startswith(target + "#"):
            counter += 1
            heading_text = line[len(target):].lstrip()
            line = f"{target}{chapter_no}.{counter} {heading_text}"
        out.append(line)
    return "\n".join(out)


def render_folder(parts: list[str], src_dir: str, heading_shift: int,
                  named_subs: list[str] | None = None,
                  chapter_no: str | None = None,
                  chapter_title: str | None = None) -> None:
    folder = ROOT / src_dir
    if not folder.exists():
        return
    named_subs = named_subs or []

    readme = read(folder / "README.md")
    if readme:
        if chapter_title:
            readme = strip_duplicate_readme_h1(readme, chapter_title)
        shifted = shift_headings(readme, heading_shift)
        if chapter_no:
            shifted = number_top_sections(shifted, chapter_no,
                                          min_level=2 + heading_shift)
        parts.append(shifted)

    for fname in list_loose_md(folder):
        content = read(folder / fname)
        if not content:
            continue
        h1_match = _README_TITLE_RE.match(content)
        if h1_match:
            pretty = h1_match.group(1).strip()
            content = content[h1_match.end():].lstrip("\n")
        else:
            pretty = Path(fname).stem.replace("_", " ").title()
            pretty = re.sub(r"^\d+\s+", "", pretty)
        parts.append(f"\n\n{'#' * (heading_shift + 1)} {pretty}\n")
        parts.append(shift_headings(content, heading_shift + 1))

    ex = read(folder / "exercises.md")
    if ex:
        parts.append(f"\n\n{'#' * (heading_shift + 1)} Exercises\n")
        parts.append(shift_headings(ex, heading_shift + 1))

    table = code_table(folder, src_dir)
    if table:
        parts.append(f"\n\n{'#' * (heading_shift + 1)} Code samples & lab guides\n")
        parts.append(
            "Every runnable script ships with a sibling *plain-English lab guide* "
            "(`.lab.md`) that explains it as if you're seeing the file for the "
            "first time.\n"
        )
        parts.extend(table)

    for sub in named_subs:
        sub_path = folder / sub
        if not sub_path.exists() or not sub_path.is_dir():
            continue
        sub_src = f"{src_dir}/{sub}"
        parts.append(f"\n\n---\n\n{'#' * (heading_shift + 1)} Section &mdash; `{sub}/`\n")
        parts.append(f"> Source folder: [`{sub_src}/`]({sub_src}/README.md)\n")
        render_folder(parts, sub_src, heading_shift + 1, named_subs=[])

    capstones = folder / "capstones"
    if capstones.exists() and capstones.is_dir():
        cap_src = f"{src_dir}/capstones"
        parts.append(f"\n\n---\n\n{'#' * (heading_shift + 1)} Capstones\n")
        parts.append(
            f"Production-grade projects in [`{cap_src}/`]({cap_src}/). "
            "Each capstone is a runnable script with a sibling plain-English lab guide.\n"
        )
        ctable = code_table(capstones, cap_src)
        if ctable:
            parts.extend(ctable)


def build_chapter(no: str, parent_dir: str, title: str,
                  named_subs: list[str]) -> str:
    section_anchor = f"chapter-{no}-{slugify(title)}"
    parts: list[str] = [f"\n\n<a id='{section_anchor}'></a>\n\n# Chapter {no}. {title}\n"]
    parts.append(f"> Source folder: [`{parent_dir}/`]({parent_dir}/README.md)\n")
    render_folder(parts, parent_dir, heading_shift=1, named_subs=named_subs,
                  chapter_no=no, chapter_title=title)
    return "\n".join(parts)


def build_appendix(letter: str, sources: list[tuple[str, list[str]]], title: str) -> str:
    section_anchor = f"appendix-{letter.lower()}-{slugify(title)}"
    parts: list[str] = [f"\n\n<a id='{section_anchor}'></a>\n\n# Appendix {letter}. {title}\n"]
    for idx, (src_dir, files) in enumerate(sources):
        if idx > 0:
            parts.append("\n\n---\n")
        parts.append(f"> Source folder: [`{src_dir}/`]({src_dir}/README.md)\n")
        folder = ROOT / src_dir
        readme = read(folder / "README.md")
        if readme:
            parts.append(shift_headings(readme, 1))
        for f in files:
            content = read(folder / f)
            if not content:
                continue
            parts.append(f"\n\n## {Path(f).stem.replace('_', ' ').title()}\n")
            parts.append(shift_headings(content, 1))
        code_files = list_code_files(folder)
        if code_files:
            parts.append("\n\n## Code samples in this section\n")
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
    for no, _, title, _ in CHAPTERS:
        anchor = f"chapter-{no}-{slugify(title)}"
        lines.append(f"- [Chapter {no}. {title}](#{anchor})")
    lines.append("\n## Appendices\n")
    for letter, _, title in APPENDICES:
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

    for no, parent_dir, title, named_subs in CHAPTERS:
        parts.append(build_chapter(no, parent_dir, title, named_subs))
        parts.append("\n\n---\n")

    for letter, sources, title in APPENDICES:
        parts.append(build_appendix(letter, sources, title))
        parts.append("\n\n---\n")

    parts.append("\n\n*Generated by `tools/build_book.py`. Re-run after editing any chapter.*\n")

    out_path = ROOT / "BOOK.md"
    out_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {out_path}  ({out_path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
