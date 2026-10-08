#!/usr/bin/env python3
"""Create a run directory from the templates and print what the orchestrator needs as JSON.

Usage:
    python tools/new_run.py --concept "Python asyncio event loop" --style "Terry Pratchett"
        [--length 2000] [--form "short story"] [--audience "..."] [--slug my-run]
        [--runs-dir runs] [--styles-dir styles]
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdutil  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_AUDIENCE = "a technically literate reader who has heard of the concept but never used it"


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "x"


def rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def create_run(concept, style, runs_dir, styles_dir, length="2000", form="short story", audience=DEFAULT_AUDIENCE, slug=None, today=None) -> dict:
    runs_dir, styles_dir = Path(runs_dir), Path(styles_dir)
    today = today or datetime.date.today().isoformat()
    style_slug = slugify(style)
    base = slug or f"{today}-{slugify(concept)[:30].strip('-')}-{style_slug[:20].strip('-')}"
    run = runs_dir / base
    n = 2
    while run.exists():
        run = runs_dir / f"{base}-{n}"
        n += 1
    for sub in ("drafts", "reviews", "notes_history", "scratch"):
        (run / sub).mkdir(parents=True)

    brief = (ROOT / "templates" / "brief.md").read_text(encoding="utf-8")
    for key, val in {
        "{concept}": concept, "{style}": style, "{style_slug}": style_slug,
        "{form}": form, "{length}": str(length), "{audience}": audience, "{date}": today,
    }.items():
        brief = brief.replace(key, val)
    (run / "brief.md").write_text(brief, encoding="utf-8")

    notes = (ROOT / "templates" / "notes.md").read_text(encoding="utf-8").replace("{round}", "1")
    (run / "notes.md").write_text(notes, encoding="utf-8")

    style_dir = styles_dir / style_slug
    return {
        "run_dir": rel(run),
        "style_slug": style_slug,
        "style_dir": rel(style_dir),
        "excerpt_files": len(mdutil.corpus_files(style_dir)),
    }


def main(argv=None) -> int:
    mdutil.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--concept", required=True)
    ap.add_argument("--style", required=True)
    ap.add_argument("--length", default="2000")
    ap.add_argument("--form", default="short story")
    ap.add_argument("--audience", default=DEFAULT_AUDIENCE)
    ap.add_argument("--slug")
    ap.add_argument("--runs-dir", default=str(ROOT / "runs"))
    ap.add_argument("--styles-dir", default=str(ROOT / "styles"))
    a = ap.parse_args(argv)
    info = create_run(a.concept, a.style, a.runs_dir, a.styles_dir, a.length, a.form, a.audience, a.slug)
    print(json.dumps(info, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
