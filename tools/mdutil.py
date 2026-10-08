"""Shared text helpers for the fiction-explainer tools. Standard library only."""
from __future__ import annotations

import re
import sys
from pathlib import Path

KEEP_OPEN = "<!-- KEEP -->"
KEEP_CLOSE = "<!-- /KEEP -->"

KEEP_BLOCK_RE = re.compile(r"<!--\s*KEEP\s*-->(.*?)<!--\s*/KEEP\s*-->", re.S)
_KEEP_MARK = re.compile(r"<!--\s*/?KEEP\s*-->")
_COMMENT_NOT_KEEP = re.compile(r"<!--(?!\s*/?KEEP\s*-->).*?-->", re.S)
_ANY_COMMENT = re.compile(r"<!--.*?-->", re.S)
RULE_RE = re.compile(r"^\s*(?:[-*_]\s*){3,}$")
HEADING_RE = re.compile(r"^#{1,6}\s+\S")
WORD_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")
DIALOGUE_RE = re.compile(r"“[^”]*”|\"[^\"\n]*\"")
TEXT_SUFFIXES = {".txt", ".md", ".markdown"}
NOTE_SECTIONS = ("keep", "change", "pivot", "reject", "overrule")

_ABBR = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|St|Prof|Sr|Jr)\.")
_SENT_RE = re.compile(r'''[^.!?]+(?:[.!?]+["'”’)\]]*)|[^.!?]+$''')


def setup_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass


def read_text(path) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def strip_comments(text: str) -> str:
    """Remove HTML comments except KEEP markers."""
    return _COMMENT_NOT_KEEP.sub("", text)


def strip_keep_markers(text: str) -> str:
    return _KEEP_MARK.sub("", text)


def clean(text: str) -> str:
    """Text with all comments and KEEP markers removed."""
    return strip_keep_markers(strip_comments(text))


def keep_blocks(text: str) -> list:
    return [m.group(1) for m in KEEP_BLOCK_RE.finditer(text)]


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def numbered_paragraphs(text: str) -> list:
    """Stable paragraph numbering shared by every tool and reviewer.

    Headings and scene rules are not numbered. Each item: id, scene, heading,
    heading_line, text.
    """
    out = []
    heading = ""
    heading_line = ""
    scene = 1
    n = 0
    for block in re.split(r"\n\s*\n", clean(text)):
        b = block.strip()
        if not b:
            continue
        if RULE_RE.match(b):
            scene += 1
            continue
        if HEADING_RE.match(b):
            first, _, rest = b.partition("\n")
            heading_line = first.strip()
            heading = heading_line.lstrip("#").strip()
            b = rest.strip()
            if not b:
                continue
        n += 1
        out.append(
            {"id": n, "scene": scene, "heading": heading, "heading_line": heading_line, "text": b}
        )
    return out


def prose_text(text: str) -> str:
    return "\n\n".join(p["text"] for p in numbered_paragraphs(text))


def words(text: str) -> list:
    return WORD_RE.findall(text)


def sentences(text: str) -> list:
    flat = re.sub(r"\s+", " ", text).strip()
    flat = _ABBR.sub(lambda m: m.group(0)[:-1] + "\x00", flat)
    flat = re.sub(r"(?<=\d)\.(?=\d)", "\x00", flat)
    flat = flat.replace("e.g.", "e\x00g\x00").replace("i.e.", "i\x00e\x00")
    return [p.strip().replace("\x00", ".") for p in _SENT_RE.findall(flat) if p.strip()]


def parse_notes(text: str) -> dict:
    """Parse notes.md into {section: [bullet, ...]} for the five known sections."""
    text = _ANY_COMMENT.sub("", text)
    result = {k: [] for k in NOTE_SECTIONS}
    current = None
    for line in text.splitlines():
        h = re.match(r"^\s*#{1,6}\s*(.+?)\s*$", line)
        if h:
            name = h.group(1).strip().lower()
            current = name if name in result else None
            continue
        if current is None:
            continue
        b = re.match(r"^\s*(?:[-*+]|\d+[.)])\s+(.*\S)\s*$", line)
        if b:
            result[current].append(b.group(1))
        elif line.strip() and result[current] and line[:1] in (" ", "\t"):
            result[current][-1] += " " + line.strip()
    return result


def corpus_files(path) -> list:
    p = Path(path)
    if p.is_file():
        return [p]
    if p.is_dir():
        return sorted(
            f
            for f in p.rglob("*")
            if f.is_file()
            and f.suffix.lower() in TEXT_SUFFIXES
            and not f.name.startswith(".")
            and not f.name.lower().startswith("readme")
        )
    return []
