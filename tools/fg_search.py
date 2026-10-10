#!/usr/bin/env python3
"""Search the Family Guy subtitles from a fiction-explainer run.

One wrapper over the four modes of ``FG_Subtitles/search.py`` (literal FTS5,
regex, semantic, hybrid). It never copies show text into deliverables: results
are printed as a short summary and, with ``--out``, written to
``<run>/scratch/fg_hits/*.json`` (git-ignored working state).

Usage:
    python tools/fg_search.py literal  "giggity" --limit 20 --out runs/<slug>
    python tools/fg_search.py regex    "\\(weakly\\)" -i --out runs/<slug>
    python tools/fg_search.py semantic "a cutaway that lands the joke" --yes
    python tools/fg_search.py hybrid   "the family reacts to a nonsense plan" --yes

Semantic / hybrid need an index (~31 MB) and a query model (~1.23 GB) on first
use; pass ``--yes`` to approve that download. Literal / regex are fully offline.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdutil  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MODE_ARG = {"literal": "--exact", "regex": "--regex", "semantic": "--semantic", "hybrid": "--hybrid"}
NEEDS_DOWNLOAD = {"semantic", "hybrid"}


def default_fg_dir() -> Path:
    env = os.environ.get("FG_SUBTITLES_DIR")
    return Path(env) if env else ROOT.parent / "FG_Subtitles"


def slugify(s: str, limit: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return slug[:limit].strip("-") or "query"


def build_fg_argv(fg_dir: Path, mode: str, query: str, limit: int, season, episode,
                  ignore_case: bool, yes: bool, no_dedupe: bool, raw: bool) -> list:
    argv = [sys.executable, str(Path(fg_dir) / "search.py"),
            MODE_ARG[mode], query, "--json", "--limit", str(limit)]
    if season is not None:
        argv += ["--season", str(season)]
    if episode is not None:
        argv += ["--episode", str(episode)]
    if mode == "regex" and ignore_case:
        argv.append("-i")
    if mode == "literal" and raw:
        argv.append("--raw")
    if mode in NEEDS_DOWNLOAD and yes:
        argv.append("--yes")
    if no_dedupe:
        argv.append("--no-dedupe")
    return argv


def run_search(fg_dir: Path, mode: str, query: str, limit: int = 20, season=None,
               episode=None, ignore_case: bool = False, yes: bool = False,
               no_dedupe: bool = False, raw: bool = False) -> tuple:
    script = Path(fg_dir) / "search.py"
    if not script.is_file():
        raise FileNotFoundError(f"no search.py in {fg_dir} (pass --fg-dir)")
    argv = build_fg_argv(fg_dir, mode, query, limit, season, episode,
                         ignore_case, yes, no_dedupe, raw)
    # No stdin: a semantic call without --yes must abort cleanly, not hang.
    proc = subprocess.run(argv, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    err = (proc.stderr or "").strip()
    low = err.lower()
    if proc.returncode != 0 and ("aborted" in low or "eof" in low):
        raise RuntimeError("the index/model download was declined or could not be confirmed; "
                           "re-run with --yes to fetch it")
    if proc.returncode != 0:
        raise RuntimeError(f"search.py failed ({proc.returncode}): {err[:300]}")
    try:
        results = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"could not parse search.py output as JSON: {e}") from e
    if not isinstance(results, list):
        raise RuntimeError("search.py returned JSON that is not a list")
    return results, (proc.stderr or "").strip()


def out_path(run_dir: Path, mode: str, query: str) -> Path:
    d = Path(run_dir) / "scratch" / "fg_hits"
    d.mkdir(parents=True, exist_ok=True)
    base = f"{mode}-{slugify(query)}"
    p = d / f"{base}.json"
    n = 2
    while p.exists():
        p = d / f"{base}-{n}.json"
        n += 1
    return p


def fmt_ts(seconds) -> str:
    s = int(round(float(seconds)))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def render_summary(results: list, mode: str, limit: int) -> str:
    if not results:
        return f"no results [{mode}]"
    lines = []
    for r in results[:limit]:
        text = re.sub(r"\s+", " ", str(r.get("text", "")))
        if len(text) > 110:
            text = text[:107] + "..."
        lines.append(f"S{int(r['season']):02d}E{int(r['episode']):02d}  "
                     f"{fmt_ts(r.get('start', 0))}  [{mode}]  {text}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fg_search.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--fg-dir", default=str(default_fg_dir()), help="clone of FG_Subtitles (read-only)")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--literal", metavar="PHRASE")
    mode.add_argument("--regex", metavar="PATTERN")
    mode.add_argument("--semantic", metavar="DESCRIPTION")
    mode.add_argument("--hybrid", metavar="DESCRIPTION")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--season", type=int)
    p.add_argument("--episode", type=int)
    p.add_argument("-i", "--ignore-case", action="store_true", help="with --regex")
    p.add_argument("--raw", action="store_true", help="with --literal: raw FTS5 syntax")
    p.add_argument("--yes", action="store_true", help="approve the semantic download")
    p.add_argument("--no-dedupe", action="store_true")
    p.add_argument("--out", default=None, help="run directory; hits go to <out>/scratch/fg_hits/")
    p.add_argument("--no-text", action="store_true", help="store metadata only, drop cue text")
    p.add_argument("--json", action="store_true", help="print raw JSON instead of a summary")
    return p


def main(argv=None) -> int:
    mdutil.setup_stdout()
    args = build_parser().parse_args(argv)
    mode = next(m for m in MODE_ARG if getattr(args, m) is not None)
    query = getattr(args, mode)
    try:
        results, note = run_search(Path(args.fg_dir), mode, query, args.limit, args.season,
                                   args.episode, args.ignore_case, args.yes,
                                   args.no_dedupe, args.raw)
    except (FileNotFoundError, RuntimeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2 if isinstance(e, FileNotFoundError) else 4

    stored = results
    if args.no_text:
        stored = [{k: v for k, v in r.items() if k != "text"} for r in results]
    payload = {"mode": mode, "query": query, "limit": args.limit, "season": args.season,
               "episode": args.episode, "count": len(results), "results": stored}
    written = None
    if args.out:
        written = out_path(Path(args.out), mode, query)
        written.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if note:
            print(note, file=sys.stderr)
        print(render_summary(results, mode, args.limit))
        if written:
            print(f"-> {written}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
