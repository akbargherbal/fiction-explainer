#!/usr/bin/env python3
"""Archive the consumed notes.md of a run and reset it from the template.

Usage:
    python tools/archive_notes.py runs/<slug> --responding-to N

N is the draft number the notes responded to. They are moved to notes_history/round_N.md and a
fresh notes.md for draft v{N+1} is created. Nothing happens if the notes contain no bullets.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdutil  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def archive(run: Path, responding_to: int, template: Path = None) -> Path:
    template = template or ROOT / "templates" / "notes.md"
    notes = run / "notes.md"
    if not notes.is_file():
        return None
    if not any(mdutil.parse_notes(mdutil.read_text(notes)).values()):
        return None
    hist = run / "notes_history"
    hist.mkdir(exist_ok=True)
    dest = hist / f"round_{responding_to}.md"
    k = 2
    while dest.exists():
        dest = hist / f"round_{responding_to}-{k}.md"
        k += 1
    shutil.move(str(notes), str(dest))
    fresh = template.read_text(encoding="utf-8").replace("{round}", str(responding_to + 1))
    notes.write_text(fresh, encoding="utf-8")
    return dest


def main(argv=None) -> int:
    mdutil.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--responding-to", type=int, required=True)
    a = ap.parse_args(argv)
    run = Path(a.run)
    if not run.is_dir():
        print(f"error: no such run directory: {run}", file=sys.stderr)
        return 2
    dest = archive(run, a.responding_to)
    if dest is None:
        print("nothing to archive (no notes bullets)")
    else:
        print(f"archived to {dest}; notes.md reset for draft v{a.responding_to + 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
