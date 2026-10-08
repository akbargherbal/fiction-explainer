# PIPELINE.md — orchestration procedure

Tool-neutral. "Dispatch `<role>`" means: run that role (see [AGENTS.md](AGENTS.md)) as a **separate agent with a fresh context** — in Claude Code, the subagent of the same name in `.claude/agents/`.

## Ground rules for the orchestrator

- You coordinate. You never write story prose, spec content or reviews.
- Every dispatch prompt contains exactly: the **role mode** (if the role has modes), the **run directory**, and the **output file(s)** expected. Pass paths, not contents.
- After each dispatch, check the output exists (`python tools/run_status.py status <run>`). If missing, retry once, quoting what went wrong. A second failure: stop and report.
- Dispatch independent work in parallel (one message, several dispatches).
- The run is resumable at any point: `python tools/run_status.py status <run>` returns the current `stage` and a `todo` list of what can run next.

---

## Procedure A — Initial run (`/explain`)

**A0. Parse the arguments.**

- Concept and style are separated by `|`, ` in the style of `, ` as written by ` or ` style: `. Examples:
  - `Kubernetes controllers | Jorge Luis Borges`
  - `React hooks in the style of Terry Pratchett --length 3000 --form "dialogue"`
- Flags: `--review-plan`, `--resume [run]`, `--length N`, `--form "…"`, `--audience "…"`.
- If concept or style is missing, ask the human **one** short question. Otherwise do not ask anything.
- `--resume`: skip to A2 using the given run (or `python tools/run_status.py latest`).

**A1. Create the run.**

```
python tools/new_run.py --concept "<X>" --style "<Y>" [--length N] [--form "…"] [--audience "…"]
```

It prints JSON: `run_dir`, `style_slug`, `style_dir`, `excerpt_files`. Then, in `brief.md`:

- Under **Assumptions**, list every default you filled in (form, length, audience, anything inferred from the one-liner).
- If `excerpt_files` is `0`, add to Assumptions: `Style target is UNGROUNDED: no excerpts in styles/<slug>/. Style fidelity will rest on model memory.`
- Do not ask the human to approve the brief. Straight through is the default.

**A2. Loop on `run_status.py status <run>` until the draft exists.** Dispatch by `todo`:

| `todo` item | Dispatch | Output |
|---|---|---|
| `research` and `style_profile` | **in parallel:** `researcher`, and `style-critic` in **profile** mode | `01_spec.md`, `01_questions.md`; `05_style_profile.md`, `05_style_stats.json` |
| `premises` | `planner` in **premises** mode | `02_premises.md` |
| `premise_choice` | `premise-judge` | `03_premise_choice.md` |
| `outline` | `planner` in **outline** mode | `04_outline.md` |
| `draft` | `writer` in **draft** mode | `drafts/draft_v1.md` |

**Premise regeneration (at most once).** If the first line of `03_premise_choice.md` is `DECISION: REGENERATE`:

1. `python tools/run_status.py archive-plan <run> --label regen_1`
2. Dispatch `planner` (premises mode) again, telling it to read `plans_archive/regen_1/03_premise_choice.md` and fix what the judge rejected.
3. Dispatch `premise-judge`, telling it this is the second attempt and it **must** choose A, B or C.

If `plans_archive/regen_1` already exists, never regenerate again.

**`--review-plan`.** After `04_outline.md` exists, stop. Tell the human: the chosen premise (one line), the paths of `03_premise_choice.md` and `04_outline.md`, and that they may edit either (edits are authoritative) and then run `/explain --resume <run>`. Do not draft.

**A3. Review wave** (Procedure R) on `drafts/draft_v1.md`.

**A4. Report to the human.** One short message: where the draft is, where the digest is, the headline numbers from the digest, and the next step ("write `notes.md`, then `/revise`"). Do not paste the story.

---

## Procedure R — Review wave for the latest draft vN

Let `N` be `round` from `run_status.py status`.

1. `python tools/number_paragraphs.py drafts/draft_vN.md --out reviews/vN/numbered.md`
2. **In parallel:**
   - `cold-reader` → `reviews/vN/cold_read.md` (give it only the run directory and N)
   - `style-critic` in **review** mode → `reviews/vN/style.md`
   - `fact-checker` in **audit** mode → `reviews/vN/accuracy.md`
   - `python tools/slop_lint.py drafts/draft_vN.md --out reviews/vN/lint.md`
3. When `cold_read.md` exists: `fact-checker` in **grade** mode → `reviews/vN/comprehension.md`.
4. Write `reviews/vN/digest.md` yourself, **consolidating** the review files (do not add your own literary judgement). Format below.

If notes from the previous round exist in `notes_history/round_{N-1}.md`, tell `fact-checker` and `style-critic` to read its **Overrule** section: overruled findings are downgraded to NOTE with the reason recorded, not re-raised.

### Digest format (max ~60 lines)

```
# Draft vN — digest
Run: <slug> · Words: <n> · Style grounding: GROUNDED (<k> files) | UNGROUNDED

| Check | Result |
|---|---|
| Accuracy | <B> blockers · <W> warnings · <N> notes |
| Coverage (MUST concepts dramatized) | x / y |
| Cold read (answers supported by the text) | a / b · misconception probes c / d |
| Style fidelity (mean of 1–5 rubric) | x.x |
| Slop lint | <n> flags: <categories> |

## Blockers (fixed automatically next round unless you Overrule)
- F1 [P12] one line

## Teaching gaps
- C3 <what failed to land> (from comprehension.md)

## Style
- Closest to the voice: [P..] · Furthest: [P..]
- Top pastiche tells (max 3)

## What's working (Keep candidates)
- [P7] "first eight words of the passage…"  (max 5)

## Suggested notes (copy what you agree with into notes.md)
- Change: …
- Pivot: only if the critics point at a structural problem

## Last round's notes → outcome   (only from round 2 on; from drafts/draft_vN.changes.md)
- Keep: honored / Change: done / …

## Read
drafts/draft_vN.md · reviews/vN/{accuracy,comprehension,style,lint}.md · reviews/vN/numbered.md
```

---

## Procedure V — Revision (`/revise [run]`)

Default run: `python tools/run_status.py latest`. Let `N` be the latest draft number.

**V1. Check state.** `python tools/run_status.py status <run>`. Reviews for draft vN must be complete (finish Procedure R first if not).
Read `notes.md` with `python tools/run_status.py status` (`notes_pending`). If there are no note bullets:

- blockers exist in `reviews/vN/accuracy.md` → proceed with a **blockers-only** revision and say so;
- otherwise tell the human there is nothing to do and stop.

**V2. Locks.**

- If `drafts/draft_vN.edited.md` exists:
  `python tools/lock_check.py adopt --original drafts/draft_vN.md --edited drafts/draft_vN.edited.md --out drafts/draft_vN.locked.md`
  then apply Keep quotes on top:
  `python tools/lock_check.py apply --draft drafts/draft_vN.locked.md --notes notes.md --out drafts/draft_vN.locked.md`
- Otherwise:
  `python tools/lock_check.py apply --draft drafts/draft_vN.md --notes notes.md --out drafts/draft_vN.locked.md`

Exit code 1 means some Keep quotes could not be matched. The tool still writes what it could. Remember the messages; report them to the human at the end.

**V3. Pivot.** If `notes.md` has Pivot bullets **and** `plans_archive/round_N` does not exist:

1. Append the pivot text to the **Pivot log** in `brief.md`.
2. `python tools/run_status.py archive-plan <run> --label round_N`
3. Re-run `planner` (premises) → `premise-judge` → `planner` (outline), each told to read the Pivot log and the archived plan. (Same regeneration rule as A2.)

If `plans_archive/round_N` already exists, the pivot was applied earlier; do not repeat it.

**V4. Revise.** Dispatch `writer` in **revise** mode. It reads `drafts/draft_vN.locked.md` (or `draft_vN.md` if no locks), `reviews/vN/digest.md`, `reviews/vN/accuracy.md`, `notes.md` and, if a pivot happened, the new outline. It writes `drafts/draft_v{N+1}.md` and `drafts/draft_v{N+1}.changes.md`.
Accuracy BLOCKERS are always fixed unless the notes **Overrule** them.

**V5. Verify locks.**
`python tools/lock_check.py check --old drafts/draft_vN.locked.md --new drafts/draft_v{N+1}.md`
Exit 1 → re-dispatch `writer` once, quoting the output. Still failing → stop and tell the human which locked passages were lost.

**V6. Archive notes.** `python tools/archive_notes.py <run> --responding-to N`

**V7. Review wave** (Procedure R) on draft v{N+1}, then report as in A4.

---

## Limits

- Soft cap: **3 revision rounds**. At round 3 and beyond, say so and recommend either a Pivot or stopping. Past that, revision tends to sand off whatever is distinctive.
- Retries: one per failed dispatch.
- Cost: a full run is roughly 8–10 agent dispatches for the first draft and about 6 per revision round. `--review-plan` adds no cost; it only adds a pause.
