#!/usr/bin/env python3
"""Aggregate your notes across runs so recurring preferences become visible.

Usage:
    python tools/notes_digest.py [--runs-dir runs] [--top 12]

Counts, per section (Keep/Change/Pivot/Reject/Overrule), the words that recur across all notes
files (current and archived). It is crude on purpose: you read the output and decide what, if
anything, deserves a persistent taste.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdutil  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
STOP = set(
    "the a an and or but of to in on for with is are was were be it its this that these those as at by "
    "from into more less too very not no too than then so just also make made scene paragraph para "
    "should would could can will have has had they them their there here what when where which who "
    "some any all one two".split()
)


def collect(runs_dir: Path) -> dict:
    sections = {k: [] for k in mdutil.NOTE_SECTIONS}
    runs = 0
    for run in sorted(p for p in runs_dir.iterdir() if p.is_dir()) if runs_dir.is_dir() else []:
        files = list((run / "notes_history").glob("*.md")) if (run / "notes_history").is_dir() else []
        if (run / "notes.md").is_file():
            files.append(run / "notes.md")
        used = False
        for f in files:
            parsed = mdutil.parse_notes(mdutil.read_text(f))
            for k, items in parsed.items():
                sections[k].extend((run.name, i) for i in items)
                used = used or bool(items)
        runs += 1 if used else 0
    return {"sections": sections, "runs": runs}


def top_terms(items: list, n: int) -> list:
    c: Counter = Counter()
    for _, text in items:
        text = re.sub(r"\[P\d+\]|\"[^\"]*\"|“[^”]*”", " ", text)
        seen = {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'-]{3,}", text)} - STOP
        c.update(seen)
    return [(w, k) for w, k in c.most_common(n) if k >= 2]


def render(data: dict, top: int) -> str:
    out = ["# Notes digest", "", f"Runs with notes: {data['runs']}", ""]
    for k, items in data["sections"].items():
        out.append(f"## {k.capitalize()} ({len(items)} items)")
        terms = top_terms(items, top)
        out.append("Recurring terms: " + (", ".join(f"{w} ×{n}" for w, n in terms) if terms else "none yet (needs repeats across notes)"))
        out.append("")
    out.append("_Promote something to a persistent taste file only when it recurs across several runs._")
    return "\n".join(out)


def main(argv=None) -> int:
    mdutil.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs-dir", default=str(ROOT / "runs"))
    ap.add_argument("--top", type=int, default=12)
    a = ap.parse_args(argv)
    print(render(collect(Path(a.runs_dir)), a.top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
