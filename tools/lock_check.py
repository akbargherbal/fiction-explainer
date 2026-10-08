#!/usr/bin/env python3
"""Manage KEEP locks on drafts.

Locked text lives between <!-- KEEP --> and <!-- /KEEP --> and must survive every revision verbatim.

Usage:
    python tools/lock_check.py list   DRAFT
    python tools/lock_check.py apply  --draft DRAFT --notes NOTES --out OUT
    python tools/lock_check.py adopt  --original DRAFT --edited EDITED --out OUT
    python tools/lock_check.py check  --old OLD --new NEW
    python tools/lock_check.py diff   --old OLD --new NEW

apply  wraps passages quoted under '## Keep' in notes.md. A quote may use '...' (or the ellipsis
       character) to span a long passage: "start of it ... end of it". Exit 1 if any quote could not
       be locked; the rest are still written.
adopt  wraps every paragraph that is new or changed in EDITED relative to the original draft.
check  exit 1 if a KEEP block in OLD is missing from NEW, or present but no longer marked.
diff   which paragraphs of NEW are new or changed relative to OLD.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdutil  # noqa: E402

_QUOTE_RE = re.compile(r'"([^"]+)"|“([^”]+)”')


def _norm(s: str) -> str:
    return mdutil.norm_ws(s)


def check(old_text: str, new_text: str) -> tuple:
    old_blocks = [_norm(b) for b in mdutil.keep_blocks(old_text)]
    new_blocks = [_norm(b) for b in mdutil.keep_blocks(new_text)]
    new_plain = _norm(mdutil.clean(new_text))
    missing, unmarked = [], []
    for b in old_blocks:
        if not b:
            continue
        if b not in new_plain:
            missing.append(b)
        elif not any(b in nb for nb in new_blocks):
            unmarked.append(b)
    return missing, unmarked


def quote_regex(quote: str):
    parts = re.split(r"\s*(?:\.\.\.|…)\s*", quote.strip())
    pieces = []
    for part in parts:
        ws = part.split()
        if ws:
            pieces.append(r"\s+".join(re.escape(w) for w in ws))
    if not pieces:
        return None
    return re.compile(".*?".join(pieces), re.S | re.I)


def apply_keeps(draft: str, notes: str) -> tuple:
    """Return (new_text, results). results: list of (status, quote)."""
    bullets = mdutil.parse_notes(notes)["keep"]
    existing = [(m.start(), m.end()) for m in mdutil.KEEP_BLOCK_RE.finditer(draft)]
    results, spans = [], []
    for bullet in bullets:
        quotes = [a or b for a, b in _QUOTE_RE.findall(bullet)]
        if not quotes:
            results.append(("NO_QUOTE", bullet))
            continue
        for q in quotes:
            rx = quote_regex(q)
            if rx is None:
                results.append(("NO_QUOTE", q))
                continue
            matches = list(rx.finditer(draft))
            if not matches:
                results.append(("NOT_FOUND", q))
                continue
            inside = [m for m in matches if any(s <= m.start() and m.end() <= e for s, e in existing)]
            fresh = [m for m in matches if m not in inside]
            if inside and not fresh:
                results.append(("ALREADY_LOCKED", q))
                continue
            if len(fresh) > 1:
                results.append(("AMBIGUOUS", q))
                continue
            m = fresh[0]
            if any(m.start() < e and s < m.end() for s, e in existing):
                results.append(("CONFLICT", q))
                continue
            if any(m.start() < e and s < m.end() for s, e in spans):
                results.append(("CONFLICT", q))
                continue
            spans.append((m.start(), m.end()))
            results.append(("LOCKED", q))
    out = draft
    for s, e in sorted(spans, reverse=True):
        out = out[:s] + mdutil.KEEP_OPEN + out[s:e] + mdutil.KEEP_CLOSE + out[e:]
    return out, results


def adopt(original: str, edited: str) -> tuple:
    known = {_norm(p["text"]) for p in mdutil.numbered_paragraphs(original)}
    out, wrapped = [], 0
    for chunk in re.split(r"(\n\s*\n)", edited):
        s = chunk.strip()
        if not s or re.fullmatch(r"\n\s*\n", chunk):
            out.append(chunk)
            continue
        if mdutil.RULE_RE.match(s) or "KEEP" in s and mdutil._KEEP_MARK.search(s):
            out.append(chunk)
            continue
        head = ""
        body = s
        if mdutil.HEADING_RE.match(s):
            first, _, rest = s.partition("\n")
            head, body = first + "\n", rest.strip()
            if not body:
                out.append(chunk)
                continue
        if _norm(mdutil.clean(body)) in known:
            out.append(chunk)
            continue
        lead = chunk[: len(chunk) - len(chunk.lstrip())]
        trail = chunk[len(chunk.rstrip()):]
        out.append(lead + head + mdutil.KEEP_OPEN + body + mdutil.KEEP_CLOSE + trail)
        wrapped += 1
    return "".join(out), wrapped


def diff(old: str, new: str) -> dict:
    o = [(p["id"], _norm(p["text"])) for p in mdutil.numbered_paragraphs(old)]
    n = [(p["id"], _norm(p["text"])) for p in mdutil.numbered_paragraphs(new)]
    oset, nset = {t for _, t in o}, {t for _, t in n}
    new_ids = [i for i, t in n if t not in oset]
    gone_ids = [i for i, t in o if t not in nset]
    return {
        "old_paragraphs": len(o),
        "new_paragraphs": len(n),
        "unchanged": len(n) - len(new_ids),
        "new_or_changed_ids": new_ids,
        "removed_or_changed_old_ids": gone_ids,
    }


def _read(path: str) -> str:
    return mdutil.read_text(path)


def main(argv=None) -> int:
    mdutil.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list")
    s.add_argument("draft")
    s = sub.add_parser("apply")
    s.add_argument("--draft", required=True)
    s.add_argument("--notes", required=True)
    s.add_argument("--out", required=True)
    s = sub.add_parser("adopt")
    s.add_argument("--original", required=True)
    s.add_argument("--edited", required=True)
    s.add_argument("--out", required=True)
    s = sub.add_parser("check")
    s.add_argument("--old", required=True)
    s.add_argument("--new", required=True)
    s = sub.add_parser("diff")
    s.add_argument("--old", required=True)
    s.add_argument("--new", required=True)
    args = ap.parse_args(argv)

    for attr in ("draft", "notes", "original", "edited", "old", "new"):
        v = getattr(args, attr, None)
        if v and not Path(v).is_file():
            print(f"error: no such file: {v}", file=sys.stderr)
            return 2

    if args.cmd == "list":
        blocks = mdutil.keep_blocks(_read(args.draft))
        for i, b in enumerate(blocks, 1):
            print(f"{i}. {_norm(b)[:100]}")
        print(f"{len(blocks)} locked block(s)")
        return 0

    if args.cmd == "apply":
        text, results = apply_keeps(_read(args.draft), _read(args.notes))
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        problems = 0
        for status, q in results:
            short = _norm(q)[:80]
            print(f"{status}: {short}")
            if status in ("NOT_FOUND", "AMBIGUOUS", "CONFLICT", "NO_QUOTE"):
                problems += 1
        locked = sum(1 for st, _ in results if st == "LOCKED")
        print(f"wrote {args.out} · {locked} newly locked · {problems} problem(s)")
        return 1 if problems else 0

    if args.cmd == "adopt":
        text, wrapped = adopt(_read(args.original), _read(args.edited))
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out} · {wrapped} human-edited paragraph(s) locked")
        return 0

    if args.cmd == "check":
        missing, unmarked = check(_read(args.old), _read(args.new))
        for b in missing:
            print(f"MISSING: {b[:100]}")
        for b in unmarked:
            print(f"UNMARKED (present but KEEP markers dropped): {b[:100]}")
        print("OK: all locked passages preserved" if not (missing or unmarked) else f"FAIL: {len(missing)} missing, {len(unmarked)} unmarked")
        return 1 if (missing or unmarked) else 0

    d = diff(_read(args.old), _read(args.new))
    print(json.dumps(d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
