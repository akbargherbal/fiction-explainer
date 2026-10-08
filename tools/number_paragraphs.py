#!/usr/bin/env python3
"""Print a draft with stable [P#] paragraph ids, so reviewers and the human can cite passages.

Usage:
    python tools/number_paragraphs.py drafts/draft_v1.md [--out reviews/v1/numbered.md]

KEEP markers and HTML comments are stripped from the view; scene breaks are shown as '* * *'.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdutil  # noqa: E402


def render(text: str) -> str:
    lines = []
    last_heading = None
    last_scene = 1
    for p in mdutil.numbered_paragraphs(text):
        if p["scene"] != last_scene:
            lines.append(f"* * *  (scene {p['scene']})\n")
            last_scene = p["scene"]
        if p["heading_line"] and p["heading_line"] != last_heading:
            lines.append(p["heading_line"] + "\n")
            last_heading = p["heading_line"]
        lines.append(f"[P{p['id']}] {p['text']}\n")
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None) -> int:
    mdutil.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    path = Path(args.draft)
    if not path.is_file():
        print(f"error: no such file: {path}", file=sys.stderr)
        return 2
    view = render(mdutil.read_text(path))
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(view, encoding="utf-8")
        print(f"wrote {out}")
    else:
        sys.stdout.write(view)
    return 0


if __name__ == "__main__":
    sys.exit(main())
