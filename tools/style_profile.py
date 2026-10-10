#!/usr/bin/env python3
"""Measure style from text, and compare a draft against a reference corpus.

Usage:
    python tools/style_profile.py profile styles/<slug> [--dialogue] [--json] [--out stats.json]
    python tools/style_profile.py compare --reference styles/<slug> --draft drafts/draft_v1.md
                                          [--dialogue] [--tolerance 0.35] [--json]

PATH may be a file or a folder of .txt/.md files. Metrics are cheap proxies for voice (rhythm,
punctuation habits, dialogue share, person, tense hint, lexical variety). They catch drift, not voice.
Dialogue detection assumes double quotes ("..." or curly quotes).

``--dialogue`` is for corpora that are dialogue only (subtitles, screenplays) and carry no quote
marks: each non-empty line counts as one utterance, the utterance length replaces sentence length,
and dialogue share is 1.0. Pass it for the reference corpus; leave it off for a prose draft.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdutil  # noqa: E402

STOP = set(
    "a about above after again all also am an and any are as at be because been before being below "
    "between both but by can could did do does doing down during each few for from further had has "
    "have having he her here hers herself him himself his how i if in into is it its itself just me "
    "more most my myself no nor not now of off on once only or other our ours ourselves out over own "
    "same she should so some such than that the their theirs them themselves then there these they "
    "this those through to too under until up very was we were what when where which while who whom "
    "why will with would you your yours yourself yourselves said one like".split()
)
FIRST = {"i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves"}
SECOND = {"you", "your", "yours", "yourself", "yourselves"}
PAST = {"was", "were", "had", "did", "said", "went", "came", "saw", "knew", "thought", "made", "took"}
PRES = {"is", "are", "has", "does", "says", "goes", "comes", "sees", "knows", "thinks", "makes", "takes"}
CONJ_START = {"and", "but", "so", "yet", "or", "nor"}
PRONOUN_START = {"he", "she", "they", "i", "we", "it", "you"}
FLOORS = {"per1k": 1.0, "share": 0.02, "len": 1.0}
MIN_WORDS = 300


def kind(key: str) -> str:
    if key.endswith("_per_1k"):
        return "per1k"
    if key.endswith(("_share", "_hint")) or key.startswith("mattr"):
        return "share"
    return "len"


def _pct(vals: list, p: float) -> float:
    if not vals:
        return 0.0
    k = (len(vals) - 1) * p / 100.0
    f = int(k)
    c = min(f + 1, len(vals) - 1)
    return vals[f] + (vals[c] - vals[f]) * (k - f)


def mattr(tokens: list, window: int = 250) -> float:
    n = len(tokens)
    if n == 0:
        return 0.0
    if n <= window:
        return len(set(tokens)) / n
    counts: Counter = Counter(tokens[:window])
    total = len(counts) / window
    num = 1
    for i in range(window, n):
        out = tokens[i - window]
        counts[out] -= 1
        if counts[out] == 0:
            del counts[out]
        counts[tokens[i]] += 1
        total += len(counts) / window
        num += 1
    return total / num


def compute(text: str, as_dialogue: bool = False) -> dict:
    """Measure a text. With ``as_dialogue`` (subtitles, screenplays) each
    non-empty line is one utterance and the whole text counts as dialogue."""
    prose = mdutil.prose_text(text)
    toks = mdutil.words(prose)
    n = len(toks)
    if n == 0:
        raise ValueError("no prose found")
    low = [t.lower().replace("’", "'") for t in toks]
    base = [t.split("'")[0] for t in low]
    k = 1000.0 / n

    if as_dialogue:
        pairs = [(ln, mdutil.words(ln)) for ln in prose.splitlines() if ln.strip()]
        paras = [len(w) for _, w in pairs]
    else:
        pairs = [(s, mdutil.words(s)) for s in mdutil.sentences(prose)]
        paras = [len(mdutil.words(p)) for p in re.split(r"\n\s*\n", prose) if p.strip()]
    pairs = [(s, w) for s, w in pairs if w]
    lens = sorted(len(w) for _, w in pairs)
    paras = [x for x in paras if x]

    if as_dialogue:
        dlg_words = n
    else:
        dialogue = mdutil.DIALOGUE_RE.findall(prose)
        dlg_words = sum(len(mdutil.words(d)) for d in dialogue)
    narration = mdutil.DIALOGUE_RE.sub(" ", prose)
    nbase = [w.lower().replace("’", "'").split("'")[0] for w in mdutil.words(narration)]
    past = sum(1 for w in nbase if w in PAST)
    pres = sum(1 for w in nbase if w in PRES)

    starts = []
    for s, _ in pairs:
        m = re.match(r"[\"“‘'(\[\s]*([A-Za-z]+)", s)
        if m:
            starts.append(m.group(1).lower())
    ns = max(len(starts), 1)

    def count(ch: str) -> int:
        return prose.count(ch)

    metrics = {
        "sent_mean": sum(lens) / len(lens),
        "sent_median": statistics.median(lens),
        "sent_stdev": statistics.pstdev(lens) if len(lens) > 1 else 0.0,
        "sent_p90": _pct(lens, 90),
        "short_sent_share": sum(1 for x in lens if x <= 6) / len(lens),
        "long_sent_share": sum(1 for x in lens if x >= 30) / len(lens),
        "para_mean": sum(paras) / len(paras) if paras else 0.0,
        "para_median": statistics.median(paras) if paras else 0.0,
        "dialogue_share": dlg_words / n,
        "commas_per_1k": count(",") * k,
        "semicolons_per_1k": count(";") * k,
        "colons_per_1k": count(":") * k,
        "em_dashes_per_1k": (count("—") + prose.count(" -- ")) * k,
        "questions_per_1k": count("?") * k,
        "exclamations_per_1k": count("!") * k,
        "ellipses_per_1k": (count("…") + prose.count("...")) * k,
        "parens_per_1k": count("(") * k,
        "first_person_per_1k": sum(1 for w in base if w in FIRST) * k,
        "second_person_per_1k": sum(1 for w in base if w in SECOND) * k,
        "ly_adverbs_per_1k": sum(1 for w in low if len(w) > 5 and w.endswith("ly")) * k,
        "past_tense_hint": (past / (past + pres)) if (past + pres) else None,
        "conj_start_share": sum(1 for w in starts if w in CONJ_START) / ns,
        "pronoun_start_share": sum(1 for w in starts if w in PRONOUN_START) / ns,
        "the_start_share": sum(1 for w in starts if w == "the") / ns,
        "mattr_250": mattr(low),
    }
    top = Counter(w for w in low if "'" not in w and len(w) > 3 and w not in STOP)
    return {
        "words": n,
        "sentences": len(pairs),
        "paragraphs": len(paras),
        "dialogue": as_dialogue,
        "metrics": {key: (round(v, 4) if v is not None else None) for key, v in metrics.items()},
        "top_words": top.most_common(25),
    }


def load_corpus(path) -> tuple:
    files = mdutil.corpus_files(path)
    if not files:
        raise FileNotFoundError(f"no .txt/.md excerpts found at {path}")
    return "\n\n".join(mdutil.read_text(f) for f in files), len(files)


def compare(ref: dict, draft: dict, tol: float = 0.35) -> list:
    rows = []
    for key, r in ref["metrics"].items():
        d = draft["metrics"].get(key)
        if r is None or d is None:
            continue
        floor = FLOORS[kind(key)]
        delta = d - r
        rel = delta / max(abs(r), floor)
        flag = "OK"
        if abs(delta) > tol * max(abs(r), floor):
            flag = "HIGH" if delta > 0 else "LOW"
        rows.append({"metric": key, "reference": r, "draft": d, "delta_pct": round(rel * 100, 1), "flag": flag})
    return rows


def render_profile(stats: dict, label: str, nfiles: int) -> str:
    out = [f"# Style profile (measured) — {label}", ""]
    if stats.get("dialogue"):
        out.append("_Dialogue mode: each non-empty line is one utterance; dialogue share is 1.0._")
        out.append("")
    out.append(f"Words {stats['words']} · sentences {stats['sentences']} · paragraphs {stats['paragraphs']} · files {nfiles}")
    out += ["", "| Metric | Value |", "|---|---|"]
    for key, v in stats["metrics"].items():
        out.append(f"| {key} | {'n/a' if v is None else f'{v:.3f}'} |")
    out += ["", "Top content words: " + ", ".join(f"{w} ({c})" for w, c in stats["top_words"]), ""]
    if stats["words"] < 2000:
        out.append("_Small corpus (<2,000 words): treat the numbers as rough._")
    return "\n".join(out)


def render_compare(rows: list, ref_words: int, draft_words: int, tol: float, dialogue: bool = False) -> str:
    out = ["# Style compare (draft vs reference)", ""]
    out.append(f"Reference {ref_words} words · draft {draft_words} words · tolerance ±{tol:.0%}"
               + (" · reference read in dialogue mode" if dialogue else ""))
    if draft_words < MIN_WORDS:
        out.append(f"_Draft under {MIN_WORDS} words: comparison is unreliable._")
    if dialogue:
        out.append("_Reference is dialogue-only: sentence metrics describe utterances, not prose sentences._")
    out += ["", "| Metric | Reference | Draft | Δ% | Flag |", "|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['metric']} | {r['reference']:.3f} | {r['draft']:.3f} | {r['delta_pct']:+.0f}% | {r['flag']} |")
    flagged = [r for r in rows if r["flag"] != "OK"]
    out += ["", "Outside tolerance: " + (", ".join(f"{r['metric']} {r['flag']}" for r in flagged) or "none"), ""]
    return "\n".join(out)


def main(argv=None) -> int:
    mdutil.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("profile")
    p.add_argument("path")
    p.add_argument("--dialogue", action="store_true", help="each non-empty line is one utterance")
    p.add_argument("--json", action="store_true")
    p.add_argument("--out")
    c = sub.add_parser("compare")
    c.add_argument("--reference", required=True)
    c.add_argument("--draft", required=True)
    c.add_argument("--dialogue", action="store_true", help="read the reference as dialogue-only")
    c.add_argument("--tolerance", type=float, default=0.35)
    c.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    try:
        if args.cmd == "profile":
            text, nfiles = load_corpus(args.path)
            stats = compute(text, as_dialogue=args.dialogue)
            if args.out:
                Path(args.out).parent.mkdir(parents=True, exist_ok=True)
                Path(args.out).write_text(json.dumps(stats, indent=2), encoding="utf-8")
                print(f"wrote {args.out}")
            elif args.json:
                print(json.dumps(stats, indent=2))
            if not args.json or args.out:
                print(render_profile(stats, args.path, nfiles))
            return 0
        ref_text, _ = load_corpus(args.reference)
        draft_path = Path(args.draft)
        if not draft_path.is_file():
            print(f"error: no such file: {draft_path}", file=sys.stderr)
            return 2
        ref, dr = compute(ref_text, as_dialogue=args.dialogue), compute(mdutil.read_text(draft_path))
        rows = compare(ref, dr, args.tolerance)
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            print(render_compare(rows, ref["words"], dr["words"], args.tolerance, args.dialogue))
        return 0
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
