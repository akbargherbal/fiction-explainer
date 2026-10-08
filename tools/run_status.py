#!/usr/bin/env python3
"""Where is a run, and what should happen next? Derived purely from which files exist.

Usage:
    python tools/run_status.py status runs/<slug> [--json]
    python tools/run_status.py latest [--runs-dir runs]
    python tools/run_status.py archive-plan runs/<slug> --label round_2

`stage` is the first thing to do; `todo` lists everything that can run now (items may be parallel):
  research, style_profile, premises, premise_choice, outline, draft,
  numbered, cold_read, style_review, lint, accuracy, grade, digest,
  revise (notes are waiting), await_human (nothing to do until you write notes).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdutil  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DRAFT_RE = re.compile(r"^draft_v(\d+)\.md$")
PLAN_FILES = ("02_premises.md", "03_premise_choice.md", "04_outline.md")
WAVE1 = {"cold_read": "cold_read.md", "style_review": "style.md", "lint": "lint.md", "accuracy": "accuracy.md"}


def latest_draft(run: Path) -> int:
    best = 0
    d = run / "drafts"
    if d.is_dir():
        for f in d.iterdir():
            m = DRAFT_RE.match(f.name)
            if m:
                best = max(best, int(m.group(1)))
    return best


def notes_pending(run: Path) -> bool:
    f = run / "notes.md"
    return f.is_file() and any(mdutil.parse_notes(mdutil.read_text(f)).values())


def status(run) -> dict:
    run = Path(run)
    info = {"run": str(run), "round": 0, "latest_draft": None, "stage": "init", "todo": [], "notes_pending": False}
    if not (run / "brief.md").is_file():
        info["error"] = "brief.md missing (run tools/new_run.py first)"
        return info

    n = latest_draft(run)
    info["round"] = n
    info["notes_pending"] = notes_pending(run)
    if n:
        info["latest_draft"] = str(run / "drafts" / f"draft_v{n}.md")
    has = lambda name: (run / name).is_file()  # noqa: E731

    todo = []
    if not (has("01_spec.md") and has("01_questions.md")):
        todo.append("research")
    if not has("05_style_profile.md"):
        todo.append("style_profile")
    if not todo:
        if not has("02_premises.md"):
            todo = ["premises"]
        elif not has("03_premise_choice.md"):
            todo = ["premise_choice"]
        elif not has("04_outline.md"):
            todo = ["outline"]
        elif n == 0:
            todo = ["draft"]
        else:
            rd = run / "reviews" / f"v{n}"
            if not (rd / "numbered.md").is_file():
                todo = ["numbered"]
            else:
                todo = [k for k, f in WAVE1.items() if not (rd / f).is_file()]
                if (rd / "cold_read.md").is_file() and not (rd / "comprehension.md").is_file():
                    todo.append("grade")
                if not todo and not (rd / "digest.md").is_file():
                    todo = ["digest"]
    info["todo"] = todo
    if todo:
        info["stage"] = todo[0]
    else:
        info["stage"] = "revise" if info["notes_pending"] else "await_human"
    return info


def latest_run(runs_dir: Path):
    if not runs_dir.is_dir():
        return None
    runs = [d for d in runs_dir.iterdir() if d.is_dir() and not d.name.startswith(".") and (d / "brief.md").is_file()]
    if not runs:
        return None
    return max(runs, key=lambda d: ((d / "brief.md").stat().st_mtime, d.name))


def archive_plan(run: Path, label: str) -> list:
    dest = run / "plans_archive" / label
    if dest.exists():
        raise FileExistsError(f"{dest} already exists")
    dest.mkdir(parents=True)
    moved = []
    for name in PLAN_FILES:
        src = run / name
        if src.is_file():
            shutil.move(str(src), str(dest / name))
            moved.append(name)
    return moved


def main(argv=None) -> int:
    mdutil.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status")
    s.add_argument("run")
    s.add_argument("--json", action="store_true", help="(default) kept for clarity")
    s = sub.add_parser("latest")
    s.add_argument("--runs-dir", default=str(ROOT / "runs"))
    s = sub.add_parser("archive-plan")
    s.add_argument("run")
    s.add_argument("--label", required=True)
    args = ap.parse_args(argv)

    if args.cmd == "status":
        if not Path(args.run).is_dir():
            print(f"error: no such run directory: {args.run}", file=sys.stderr)
            return 2
        print(json.dumps(status(args.run), indent=2))
        return 0
    if args.cmd == "latest":
        r = latest_run(Path(args.runs_dir))
        if r is None:
            print("error: no runs found", file=sys.stderr)
            return 1
        try:
            print(r.relative_to(ROOT))
        except ValueError:
            print(r)
        return 0
    run = Path(args.run)
    if not run.is_dir():
        print(f"error: no such run directory: {run}", file=sys.stderr)
        return 2
    try:
        moved = archive_plan(run, args.label)
    except FileExistsError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"archived {', '.join(moved) or 'nothing'} to plans_archive/{args.label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
