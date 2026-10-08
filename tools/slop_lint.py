#!/usr/bin/env python3
"""Heuristic lint for common LLM-fiction 'slop'. Reports; never edits.

Usage:
    python tools/slop_lint.py drafts/draft_v1.md [--out reviews/v1/lint.md] [--json] [--strict]
                              [--ignore CATEGORY ...] [--max CATEGORY=N ...]

Findings are heuristics. The style-critic triages them: a voice may legitimately use em dashes
or "not X but Y" on purpose. `--max em-dash=8` raises a limit; `--ignore em-dash` skips a category.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdutil  # noqa: E402

I = re.I

# (category, regex, allowed count, narration_only, description)
PATTERNS = [
    (
        "slop-word",
        re.compile(
            r"\b(?:tapestr(?:y|ies)|testaments? to|delv(?:e|es|ed|ing)\b|kaleidoscop\w*|"
            r"symphon(?:y|ies) of|myriad|palpable|ethereal|unwavering|labyrinth\w*|nestled|"
            r"bustling|intricate\b|whispers? of|echo(?:es|ed|ing)? of)",
            I,
        ),
        0,
        False,
        "Overused 'AI-flavoured' vocabulary",
    ),
    (
        "cliche-body",
        re.compile(
            r"\b(?:shivers? (?:ran |went )?down|breath (?:she|he|they|I|we) (?:hadn't|didn't|had not|did not) "
            r"(?:realize|realise|know)|heart (?:skipped|hammered|pounded|raced)|"
            r"eyes (?:sparkled|twinkled|glinted)|couldn'?t help but)",
            I,
        ),
        0,
        False,
        "Stock physical-reaction clichés",
    ),
    (
        "stock-transition",
        re.compile(
            r"\b(?:little did (?:she|he|they|I|we)|in that moment|something (?:shifted|stirred|changed) "
            r"(?:in|within|between)|for the first time in (?:years|a long time|her life|his life|forever)|"
            r"a sense of)\b",
            I,
        ),
        0,
        False,
        "Stock transitions and mood-announcers",
    ),
    (
        "explainer-tell",
        re.compile(
            r"\b(?:in other words|put simply|to put it simply|simply put|essentially|in essence|"
            r"this is (?:exactly )?how|which is (?:exactly )?how|that is (?:exactly )?how|"
            r"what this means is)\b",
            I,
        ),
        2,
        True,
        "Narrator explaining instead of dramatizing",
    ),
    (
        "said-adverb",
        re.compile(
            r"\b(?:said|asked|replied|whispered|murmured|muttered|answered|exclaimed|says|asks|replies)"
            r"\s+\w+ly\b",
            I,
        ),
        2,
        False,
        "Dialogue tags propped up by adverbs",
    ),
    (
        "not-just-but",
        re.compile(
            r"\bnot (?:just|merely|only|simply)\b[^.!?]{1,70}?,?\s*\bbut\b|"
            r"\bnot so much\b[^.!?]{1,60}?\bas\b",
            I,
        ),
        0,
        False,
        "'not just X, but Y' construction",
    ),
    (
        "negation-reversal",
        re.compile(
            r"\b(?:wasn't|isn't|weren't|aren't|was not|is not|were not|are not)\b[^.!?]{1,50}[.—–;,]\s*"
            r"(?:It|This|That|He|She|They)\s+(?:was|is|were|are)\b",
            I,
        ),
        1,
        False,
        "'It wasn't X. It was Y.' reversal",
    ),
]

MORAL_RE = re.compile(
    r"\b(?:realized|realised|understood|learned|knew)\s+(?:then\s+)?that\b|"
    r"\bthe (?:real|true|only) (?:lesson|point|secret|truth|magic|power)\b|"
    r"\bthat(?:'s| was) (?:the (?:real |true )?(?:lesson|point|secret|truth)|"
    r"what (?:it|everything) (?:was )?(?:all )?(?:about|meant))\b",
    I,
)
TRIPLET_RE = re.compile(r"\b[\w'’-]+, [\w'’-]+,? (?:and|or) [\w'’-]+\b")
LY_EXCEPT = {
    "family", "supply", "assembly", "anomaly", "butterfly", "friendly", "lonely", "lovely",
    "deadly", "lively", "elderly", "likely", "unlikely", "monopoly", "multiply", "apply",
    "comply", "imply", "rally", "ally", "italy", "july",
}
DENSITY_LIMITS = {
    "em-dash": 5.0,
    "triplet": 4.0,
    "narration-question": 3.0,
    "narration-exclaim": 2.0,
    "ly-adverb": 18.0,
}
MIN_WORDS_FOR_DENSITY = 200
CATEGORY_ALLOWED = {c: a for c, _, a, _, _ in PATTERNS}
CATEGORY_ALLOWED.update({"opener-run": 0, "moral-closer": 0})
DESCRIPTIONS = {c: d for c, _, _, _, d in PATTERNS}
DESCRIPTIONS["opener-run"] = "Three or more consecutive sentences opening with the same word"
DESCRIPTIONS["moral-closer"] = "Closing paragraph states the lesson"


def _snippet(src: str, m, pad: int = 35) -> str:
    s = max(0, m.start() - pad)
    e = min(len(src), m.end() + pad)
    return ("…" if s else "") + re.sub(r"\s+", " ", src[s:e]).strip() + ("…" if e < len(src) else "")


def analyze(text: str, ignore=(), overrides=None) -> dict:
    overrides = overrides or {}
    ignore = set(ignore)
    paras = mdutil.numbered_paragraphs(text)
    prose = "\n\n".join(p["text"] for p in paras)
    nwords = len(mdutil.words(prose))
    narration_all = mdutil.DIALOGUE_RE.sub(" ", prose)
    findings: list = []
    counts: Counter = Counter()

    for p in paras:
        narr = mdutil.DIALOGUE_RE.sub(" ", p["text"])
        for cat, rx, _allowed, narr_only, _desc in PATTERNS:
            if cat in ignore:
                continue
            src = narr if narr_only else p["text"]
            for m in rx.finditer(src):
                counts[cat] += 1
                findings.append({"category": cat, "paragraph": p["id"], "snippet": _snippet(src, m)})
        if "opener-run" not in ignore:
            firsts = []
            for s in mdutil.sentences(p["text"]):
                mm = re.match(r"[\"“‘'(\[\s]*([A-Za-z']+)", s)
                firsts.append(mm.group(1).lower() if mm else "")
            i = 0
            while i < len(firsts):
                j = i
                while j + 1 < len(firsts) and firsts[i] and firsts[j + 1] == firsts[i]:
                    j += 1
                if j - i + 1 >= 3:
                    counts["opener-run"] += 1
                    findings.append(
                        {
                            "category": "opener-run",
                            "paragraph": p["id"],
                            "snippet": f"{j - i + 1} consecutive sentences start with '{firsts[i]}'",
                        }
                    )
                i = j + 1

    if paras and "moral-closer" not in ignore:
        last = paras[-1]
        m = MORAL_RE.search(last["text"])
        if m:
            counts["moral-closer"] += 1
            findings.append({"category": "moral-closer", "paragraph": last["id"], "snippet": _snippet(last["text"], m)})

    k = 1000.0 / max(nwords, 1)
    ly = [w for w in re.findall(r"\b[A-Za-z]{4,}ly\b", prose) if w.lower() not in LY_EXCEPT]
    density = {
        "em-dash": (prose.count("—") + prose.count(" -- ")) * k,
        "triplet": len(TRIPLET_RE.findall(prose)) * k,
        "narration-question": narration_all.count("?") * k,
        "narration-exclaim": narration_all.count("!") * k,
        "ly-adverb": len(ly) * k,
    }

    flags = []
    for cat, n in counts.items():
        lim = overrides.get(cat, CATEGORY_ALLOWED.get(cat, 0))
        if n > lim:
            flags.append(f"{cat}: {n} found (allowed {lim:g})")
    if nwords >= MIN_WORDS_FOR_DENSITY:
        for name, v in density.items():
            if name in ignore:
                continue
            lim = overrides.get(name, DENSITY_LIMITS[name])
            if v > lim:
                flags.append(f"{name}: {v:.1f} per 1k words (limit {lim:g})")

    return {
        "words": nwords,
        "paragraphs": len(paras),
        "counts": dict(counts),
        "density": {k2: round(v, 2) for k2, v in density.items()},
        "density_checked": nwords >= MIN_WORDS_FOR_DENSITY,
        "flags": flags,
        "findings": findings,
    }


def render_md(report: dict, name: str = "") -> str:
    out = [f"# Slop lint{(' — ' + name) if name else ''}", ""]
    out.append(f"Words: {report['words']} · Paragraphs: {report['paragraphs']}")
    out += ["", "## Flags", ""]
    out += [f"- {f}" for f in report["flags"]] or ["- none"]
    out += ["", "## Density (per 1,000 words)", ""]
    if not report["density_checked"]:
        out.append(f"_Text under {MIN_WORDS_FOR_DENSITY} words: density limits not applied._")
        out.append("")
    out += ["| Metric | Value | Limit |", "|---|---|---|"]
    for name_, v in report["density"].items():
        out.append(f"| {name_} | {v:.1f} | {DENSITY_LIMITS[name_]:g} |")
    by_cat: dict = {}
    for f in report["findings"]:
        by_cat.setdefault(f["category"], []).append(f)
    out += ["", "## Findings", ""]
    if not by_cat:
        out.append("None.")
    for cat, items in by_cat.items():
        out.append(f"### {cat} ({len(items)}) — {DESCRIPTIONS.get(cat, '')}")
        out += [f"- [P{f['paragraph']}] {f['snippet']}" for f in items]
        out.append("")
    out += ["_Heuristics only. Triage against the style target before acting._", ""]
    return "\n".join(out)


def main(argv=None) -> int:
    mdutil.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("--out", help="write the Markdown report here")
    ap.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any flag is raised")
    ap.add_argument("--ignore", nargs="*", default=[], metavar="CATEGORY")
    ap.add_argument("--max", nargs="*", default=[], metavar="CATEGORY=N")
    args = ap.parse_args(argv)

    path = Path(args.draft)
    if not path.is_file():
        print(f"error: no such file: {path}", file=sys.stderr)
        return 2
    overrides = {}
    for item in args.max:
        key, _, val = item.partition("=")
        try:
            overrides[key] = float(val)
        except ValueError:
            print(f"error: bad --max value: {item}", file=sys.stderr)
            return 2

    report = analyze(mdutil.read_text(path), ignore=args.ignore, overrides=overrides)
    md = render_md(report, path.name)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"wrote {out} · {len(report['flags'])} flag(s)")
    elif args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(md)
    return 1 if (args.strict and report["flags"]) else 0


if __name__ == "__main__":
    sys.exit(main())
