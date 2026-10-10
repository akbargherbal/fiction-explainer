#!/usr/bin/env python3
"""Assemble a Family Guy style corpus from the read-only subtitle database.

The excerpts feed `tools/style_profile.py --dialogue`. They are other people's
copyrighted dialogue: this tool writes only under ``--out`` (expected to be a
git-ignored ``styles/<slug>/`` folder) and never inside a run directory.

Usage:
    python tools/fg_corpus.py --out styles/family-guy \\
        [--seasons 1,5,10,15,21] [--episodes-per-season 6] \\
        [--blocks 3] [--block-cues 60] [--target-words 12000] \\
        [--labelled] [--fg-dir PATH]

Writes:
    <out>/excerpt-SxxEyy.txt   cleaned dialogue, one cue per line
    <out>/citations.jsonl      one row per cue: file, line, season, episode,
                               start, end, speaker, text

``--labelled`` prefers the hearing-impaired (HI) subtitle of each episode, whose
lines carry ``SPEAKER:`` tags; when none exists it falls back to the default
subtitle and records ``speaker: null``.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdutil  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

TS = r"(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})"
SPEAKER_RE = re.compile(r"^\s*[-–]?\s*\[?([A-Z][A-Za-z0-9 .'\-]{0,24}?)\]?\s*:\s*(.+)$")


@dataclass
class Cue:
    start: float
    end: float
    text: str
    speaker: str | None = None


def default_fg_dir() -> Path:
    env = os.environ.get("FG_SUBTITLES_DIR")
    return Path(env) if env else ROOT.parent / "FG_Subtitles"


# --------------------------------------------------------------------------- #
# SRT parsing (mirrors FG_Subtitles/chunk.py so the corpus cleans the same way)
# --------------------------------------------------------------------------- #
def ts_to_seconds(t: str) -> float:
    m = re.match(r"\s*" + TS, t)
    if not m:
        raise ValueError(f"bad timestamp: {t!r}")
    h, mm, s, ms = (int(x) for x in m.groups())
    return h * 3600 + mm * 60 + s + ms / 1000.0


def clean_text(lines: list) -> str:
    """Strip tags, drop music lines, normalise quotes, join to one utterance."""
    out = []
    for line in lines:
        if "\u266a" in line or "\u266b" in line:      # song lyric line
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = (line.replace("\u00a0", " ")
                    .replace("\u2019", "'").replace("\u2018", "'")
                    .replace("\u201c", '"').replace("\u201d", '"'))
        line = line.strip()
        if line:
            out.append(line)
    return re.sub(r"\s+", " ", " ".join(out)).strip()


def parse_srt(content: str, labelled: bool = False) -> list:
    """Parse raw SRT into cleaned cues; empty cues are dropped."""
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cues: list = []
    i, n = 0, len(lines)
    while i < n:
        if "-->" not in lines[i]:
            i += 1
            continue
        start_s, end_s = lines[i].split("-->", 1)
        start, end = ts_to_seconds(start_s), ts_to_seconds(end_s)
        i += 1
        body: list = []
        while i < n:
            cur = lines[i]
            stripped = cur.strip()
            if stripped == "":
                i += 1
                break
            if "-->" in cur:
                break
            if stripped.isdigit() and i + 1 < n and "-->" in lines[i + 1]:
                break
            body.append(cur)
            i += 1
        text = clean_text(body)
        if text:
            speaker = None
            if labelled:
                speaker, text = split_speaker(text)
            cues.append(Cue(start, end, text, speaker))
    return cues


def split_speaker(text: str):
    """'PETER: shut up, meg' -> ('PETER', 'shut up, meg'); else (None, text)."""
    m = SPEAKER_RE.match(text)
    if not m:
        return None, text
    label = m.group(1).strip()
    rest = m.group(2).strip()
    if not rest or len(label.split()) > 3:
        return None, text
    return label, rest


# --------------------------------------------------------------------------- #
# sampling
# --------------------------------------------------------------------------- #
def evenly_pick(items: list, k: int) -> list:
    if k <= 0 or len(items) <= k:
        return list(items)
    if k == 1:
        return [items[len(items) // 2]]
    idx = sorted({round(i * (len(items) - 1) / (k - 1)) for i in range(k)})
    return [items[i] for i in idx]


def pick_blocks(n: int, blocks: int, block_cues: int) -> list:
    """Up to ``blocks`` contiguous [lo, hi) ranges spread across n cues."""
    if n <= 0:
        return []
    if n <= block_cues or blocks <= 1:
        return [(0, n)]
    span = n - block_cues
    ranges = []
    for i in range(blocks):
        lo = round(i * span / (blocks - 1))
        ranges.append((lo, min(n, lo + block_cues)))
    merged: list = []
    for lo, hi in ranges:
        if merged and lo <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
        else:
            merged.append((lo, hi))
    return merged


# --------------------------------------------------------------------------- #
# database access (read-only)
# --------------------------------------------------------------------------- #
def connect(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def seasons_in_db(con: sqlite3.Connection) -> list:
    return [r["season"] for r in con.execute("SELECT DISTINCT season FROM episodes ORDER BY season")]


def episodes_in_season(con: sqlite3.Connection, season: int) -> list:
    return [r["episode"] for r in con.execute(
        "SELECT episode FROM episodes WHERE season = ? ORDER BY episode", (season,))]


def episode_content(con: sqlite3.Connection, season: int, episode: int, labelled: bool):
    ep_id = season * 1000 + episode
    if labelled:
        row = con.execute(
            "SELECT content FROM subtitles WHERE episode_id = ? AND variant = 'HI' "
            "ORDER BY cues DESC LIMIT 1", (ep_id,)).fetchone()
        if row:
            return row["content"], True
    row = con.execute(
        "SELECT content FROM subtitles WHERE episode_id = ? AND is_default = 1 LIMIT 1",
        (ep_id,)).fetchone()
    return (row["content"] if row else None), False


# --------------------------------------------------------------------------- #
# building
# --------------------------------------------------------------------------- #
def fmt_ts(seconds: float) -> str:
    s = int(round(seconds))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def build(fg_dir: Path, out_dir: Path, seasons: list, episodes_per_season: int,
          blocks: int, block_cues: int, target_words: int, labelled: bool) -> dict:
    db = Path(fg_dir) / "data" / "family_guy_subtitles.db"
    if not db.is_file():
        raise FileNotFoundError(f"no subtitle database at {db} (pass --fg-dir)")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    con = connect(db)
    available = seasons_in_db(con)
    unknown = [s for s in seasons if s not in available]
    if unknown:
        con.close()
        raise ValueError(f"season(s) not in the database: {unknown}; available: {available}")

    files, citations, total_words = 0, [], 0
    # Spread the word target across the requested seasons so every era is
    # represented, instead of filling it from the earliest ones.
    per_season = max(1, target_words // max(1, len(seasons)))
    try:
        for season in seasons:
            season_words = 0
            for episode in evenly_pick(episodes_in_season(con, season), episodes_per_season):
                if season_words >= per_season:
                    break
                content, is_hi = episode_content(con, season, episode, labelled)
                if not content:
                    continue
                cues = parse_srt(content, labelled=labelled)
                chosen = [(lo, hi) for lo, hi in pick_blocks(len(cues), blocks, block_cues)]
                picked = [c for lo, hi in chosen for c in cues[lo:hi]]
                if not picked:
                    continue
                name = f"excerpt-S{season:02d}E{episode:02d}.txt"
                lines = []
                for c in picked:
                    lines.append(f"{c.speaker}: {c.text}" if c.speaker else c.text)
                (out_dir / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
                files += 1
                words = sum(len(c.text.split()) for c in picked)
                season_words += words
                total_words += words
                for ln, c in enumerate(picked, start=1):
                    citations.append({
                        "file": name, "line": ln, "season": season, "episode": episode,
                        "start": fmt_ts(c.start), "end": fmt_ts(c.end),
                        "speaker": c.speaker, "text": c.text,
                    })
    finally:
        con.close()

    (out_dir / "citations.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in citations), encoding="utf-8")
    return {
        "out_dir": str(out_dir), "files": files, "cues": len(citations),
        "words": total_words, "seasons": seasons, "labelled": labelled,
        "target_words": target_words, "reached_target": total_words >= target_words,
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", required=True, help="output folder, e.g. styles/family-guy")
    p.add_argument("--fg-dir", default=str(default_fg_dir()), help="clone of FG_Subtitles (read-only)")
    p.add_argument("--seasons", default="1,5,10,15,21", help="comma-separated season numbers")
    p.add_argument("--episodes-per-season", type=int, default=6)
    p.add_argument("--blocks", type=int, default=3, help="contiguous blocks sampled per episode")
    p.add_argument("--block-cues", type=int, default=60)
    p.add_argument("--target-words", type=int, default=12000)
    p.add_argument("--labelled", action="store_true", help="prefer HI subtitles for SPEAKER: tags")
    return p


def main(argv=None) -> int:
    mdutil.setup_stdout()
    args = build_parser().parse_args(argv)
    seasons = [int(s) for s in re.split(r"[,\s]+", args.seasons) if s.strip()]
    try:
        info = build(Path(args.fg_dir), Path(args.out), seasons, args.episodes_per_season,
                     args.blocks, args.block_cues, args.target_words, args.labelled)
    except (FileNotFoundError, ValueError, sqlite3.Error) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(json.dumps(info, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
