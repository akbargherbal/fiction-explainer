# Plan — "The Transformer Architecture" in the style of Family Guy

Status: **approved** · Author: orchestrator · Date: 2026-10-10
Approved by the human on 2026-10-10; decisions locked in §9 and §12.
Run slug (proposed): `2026-10-10-transformer-architecture-family-guy`

This is the plan the human approves *before* any run directory is created. It adapts the
existing `fiction-explainer` pipeline (see `PIPELINE.md`, `AGENTS.md`) to two things it was not
originally pointed at: a **dialogue-only, joke-driven TV style** and an **external corpus with a
search engine** (`FG_Subtitles`). Nothing here changes the pipeline's hard rules; it adds a
bridge and a few run-specific defaults.

---

## 1. Goal and non-goals

**Goal.** An original, readable piece of fiction that *teaches the transformer architecture* by
dramatising it, in a voice a Family Guy viewer recognises — without reproducing a line of the
show and without bending a single fact about transformers.

**Non-goals (unless the human asks).**

- Reproducing Family Guy dialogue, scenes or characters verbatim. Style is imitated through
  patterns only (AGENTS.md rule 4).
- A script that a studio could shoot. This is a teaching piece in a manner.
- Fine-tuning or training anything. All search is read-only over the existing corpus.
- Explaining the *entire* field. A ~2,500-word piece carries 4–6 MUST concepts, no more.

---

## 2. Why this pairing works — and the one hard part

Family Guy's signature device is the **cutaway**: someone says a thing, we hard-cut to an
unrelated scene, one sharp beat lands the joke, cut back. That is a near-perfect instrument for
explaining a system made of parts that do not resemble each other: a cutaway can *be* the
tokenizer, *be* the attention head, *be* the softmax, without a narrator ever saying "in other
words".

The hard part is the opposite of the usual one. Most style targets are prose; this one is
**100% dialogue with no narration, no descriptions and no attributions** — the subtitles are
speech only. So:

- The style profile must describe *voices and gags*, not sentences and paragraphs.
- The measured proxy in `tools/style_profile.py` will misread the corpus (see §7). We account
  for that rather than pretend it is clean.
- The piece needs a spine of scene-able events, or it becomes a string of disconnected jokes
  that teaches nothing. **The outline, not the voice, is where this run can fail.**

---

## 3. Assets we already have

### 3.1 `fiction-explainer` (this repo)

- Roles: researcher, style-critic, planner, premise-judge, writer, fact-checker, cold-reader
  (`.claude/agents/*.md`), orchestrated per `PIPELINE.md`.
- Tools: `new_run.py`, `run_status.py`, `number_paragraphs.py`, `slop_lint.py`,
  `style_profile.py`, `lock_check.py`, `archive_notes.py`, `notes_digest.py`.
- Contract: files are shared state; one prose owner; reviewers cite `[P#]`; KEEP locks are
  sacred; ≥3 revision rounds is the soft cap.

### 3.2 `FG_Subtitles` (external dependency, ~60 MB clone)

Verified locally against a fresh clone:

| Capability | Interface | Needs download? | Status here |
|---|---|---|---|
| Episode metadata, raw SRT | `family_guy.py` (`meta`, `seasons`, `episodes`, `get`, `json`) | no | works |
| Exact / phrase | `search.py --exact "…"` (FTS5, unstemmed) | no | works (fts.db cached) |
| Regex | `search.py --regex "…" -i` | no | works |
| Semantic | `search.py --semantic "…"` | ~31 MB index + ~1.23 GB model | index not cached; `torch` + `sentence-transformers` installed; CPU-only |
| Hybrid (RRF) | `search.py --hybrid "…"` | as semantic | — |
| Scene-aware chunks | `chunk.py` (`gap`/`w8`/`w20`); `w8` is the indexed one | no | parquet committed |
| Character evidence | `family_guy_personas.md` (3,491 speaker-labelled HI lines) | no | committed |
| Quality numbers | `dev/RESULTS.md` (recall@10 0.55, MRR 0.42 for gemma@512) | — | — |

Facts that shape the plan: the DB is **344 episodes, ~162k cues, 18 seasons**; subtitles are
dialogue only; semantic search is *scene* search, not word search; the prebuilt index is public
on Hugging Face (`akbargherbal/fg-subtitles-index`).

---

## 4. Gaps to close (the bridge)

| # | Gap | Bridge to build |
|---|---|---|
| G1 | `style_profile.py` reads `styles/<slug>/*.txt\|md`; the corpus is a SQLite DB / SRT | `tools/fg_corpus.py` → writes `styles/family-guy/excerpt-NN.txt` + `styles/family-guy/citations.jsonl` (season/episode/start/end per excerpt) |
| G2 | Search lives in another repo and has four modes | `tools/fg_search.py` → one wrapper: `literal`, `regex`, `semantic`, `hybrid`; writes hits to `runs/<run>/scratch/fg_hits/*.json` |
| G3 | The list of *who is speaking* is only in HI subtitles | `tools/fg_corpus.py --labelled` → dialogue with `SPEAKER:` tags where available; reuse the personas file |
| G4 | `style_profile.py` assumes quoted prose dialogue | a `--dialogue` mode (each line = an utterance) **or** documented acceptance of the mismeasure (§7) |
| G5 | The seven roles are Claude Code agents; this session is OpenCode | dispatch them as `subagent` prompts that read `.claude/agents/<role>.md`, **or** port to `.opencode` agent files |
| G6 | Family Guy is a script, not a short story | define `--form "prose with cutaway beats"` and tell the writer exactly what each cutaway must do (§6) |

All bridge code lives in this repo under `tools/` (or `plans/` for docs) and is standard-library
+ optional `numpy`/`pandas`. The FG repo is used **read-only** and never vendored; the plan pins
its clone directory via one env var (`FG_SUBTITLES_DIR`).

---

## 5. What we are explaining (scope the researcher will confirm)

Working scope for ~2,500 words. Priorities are the researcher's to finalise in `01_spec.md`.

**MUST concepts (the piece fails without them).**

- C1 **Tokens → embeddings.** Text is chopped into tokens; each maps to a vector of numbers.
- C2 **Self-attention.** Every token builds a *query*, *key* and *value*; query·key scores are
  scaled, softmaxed into weights, and used to blend values. The weights come from the input,
  not from any memory.
- C3 **The block and the stack.** Attention + a feed-forward network, each wrapped in a residual
  connection and normalisation; repeat N times.
- C4 **Next-token prediction.** The final vector is turned into a probability for every token in
  the vocabulary; generation is sampling one token, appending it, repeating.

**SHOULD concepts (include if the story holds).**

- C5 **Multi-head attention.** Several attention heads look at different relations at once.
- C6 **Position.** Attention is order-blind on its own; position is injected.
- C7 **Training vs inference; the context window** (and, optionally, the KV cache as "why the
  second word is faster than the first").

**Misconceptions to defeat (the cold-reader probes these).**

- M1 The model "looks things up" or "knows" facts.
- M2 Attention means the model "understands" or "focuses like a person".
- M3 The model "stores whole sentences" and retrieves them.
- M4 "Temperature" is a creativity dial with no cost.
- M5 The model "plans the whole sentence" before writing.

**Invariants (falsifiable, checkable per paragraph).**

- I1 Attention weights are computed from the current input; nothing is fetched from a stored
  fact table.
- I2 The model outputs a probability distribution over the vocabulary; the token is *sampled*,
  not chosen with intent.
- I3 Nothing in the architecture is order-aware until position is added.
- I4 Multi-head attention is parallel; heads are not a sequence of steps.

---

## 6. Creative thesis: cutaways are the teaching engine

The premise the planner is asked to build around:

> A main A-plot in the Griffin house, told almost entirely in dialogue, where a phrase Peter
> says gets **cut away** to a miniature scene that *is* a piece of the transformer. Cutting back,
> the family's reaction (usually doubt from Brian or Lois) corrects the oversimplification the
> cutaway just made. The running gag is that every cutaway costs Peter something.

Rules for the writer (added to the run's Hard constraints, not to `AGENTS.md`):

1. **Every cutaway enacts one concept.** If a cutaway explains two things or zero things, cut it.
2. **The correction is in-character and wrong-then-right.** A family member's bad analogy is
   allowed *only if events fix it* — this is how misconceptions M1–M5 get dramatised instead of
   contradicted.
3. **No narrator.** No "essentially", "in other words", "think of it like". The style target does
   not have one; a narrator is a defect.
4. **Cutaways are marked by the existing `* * *` scene separator.** Form differs from the show's
   screenplay layout so the pipeline's prose tools stay valid (see §7).
5. **One callback.** At least one cutaway returns and lands differently, so the piece has shape.

`--review-plan` is **recommended** for this run: the premise and the cutaway mapping are the
whole ballgame, and approving them before prose is cheap.

---

## 7. Style fidelity for a dialogue-only corpus

### 7.1 Building the corpus (G1)

Sampling plan: spread across the show's eras, not one season — e.g. S01, S05, S10, S15, S21;
both `non-HI` (natural dialogue) and one `HI` file per sampled episode (speaker tags). Target
**8k–15k words of excerpts** (well above the 5k floor) so the measured stats are meaningful.
`styles/family-guy/` stays git-ignored (copyright), and `citations.jsonl` lets reviewers point
back to `S05E12 00:07:14` without pasting subtitle text into a run file.

### 7.2 The measurement caveat (G4) — do not skip this

`style_profile.py` computes `dialogue_share` by finding double-quoted spans. The subtitles have
**no quotes**, so it will report ≈0 dialogue share for a corpus that is 100% dialogue, and its
sentence/paragraph rhythm metrics will be measuring a wall of short cue lines. Two acceptable
fixes; pick one before the profile is built:

- **(a) Recommended:** add `--dialogue` to `style_profile.py`: treat each non-empty line as an
  utterance, set `dialogue_share = 1.0`, and report utterance-length stats (mean/median/p90,
  share ≤6 words, share ≥30). Small, tested change.
- **(b) Cheap:** `fg_corpus.py` wraps each cue so the existing detector fires. Distorts
  punctuation metrics; only if (a) is out of scope.

Either way the profile's **qualitative sections carry the weight** — the measured numbers are a
floor for rhythm, not a description of voice.

### 7.3 The style-critic's new evidence artifact

Add an optional `05_style_evidence.md`: a citation-backed inventory of the show's mechanics —
recurring gags, catchphrases, cutaway set-ups, character speech habits — each row citing
`S##E## @ mm:ss`. This is what makes pastiche measurable instead of vibes. It is written by the
style-critic, never handed verbatim to the writer (the profile summarises it; hard rule 4 still
bans copying).

### 7.4 What "Family Guy voice" actually consists of (profile checklist)

- **Cutaway grammar:** set-up line → hard cut → escalation → hard cut back.
- **Non-sequitur escalation** and a beat of silence before the punch.
- **Character tics:** Peter's confident wrongness and summoning of Lois; Stewie's ornate
  diction curdling into a tantrum; Brian's sceptical question; Quagmire's tic word; Lois as the
  voice of doubt; Meg as the ignored one.
- **Pop-culture and meta reference**, and self-aware "this is the joke" framing.
- **Repetition as structure:** a phrase said 3–4 times, deadpan, then inverted.
- **Register whiplash:** crude next to formal.

### 7.5 Anti-pastiche guardrails

Named in the profile's "lazy-pastiche traps": catchphrase karaoke with no scene around it;
random cutaways with no teaching function; swearing as a substitute for a joke; references that
date the piece. Also: no real people as characters (AGENTS.md rule 10) — Family Guy does this
constantly, and it is out of scope here.

---

## 8. Search in the loop — the contract

Search is not a stage; it is a **research instrument** used at four moments. Every call is
recorded so claims are traceable.

| When | Who | Mode | Example query | Output |
|---|---|---|---|---|
| Style research | style-critic (profile) | `literal` + `regex` | `giggity` · `shut up, meg` · `road to` · `remember when` · `like the time` · `meanwhile` | `scratch/fg_hits/*.json` → folded into `05_style_evidence.md` |
| Style research | style-critic (profile) | `semantic` / `hybrid` | "a cutaway to an unrelated scene that lands the joke" · "Stewie insults someone with elaborate vocabulary" · "the family reacts to a nonsense plan" | same |
| Premise check | planner (premises) | `semantic` | "a father confidently explains something he completely misunderstands" | shapes premise B/C, not quoted |
| Accuracy support | fact-checker (audit) | `literal` | only for *style* claims the draft makes (e.g. "does this tic recur?"); **never** for transformer facts | `reviews/vN/accuracy.md` |

Explicit rule: **search is for the show, never for the concept.** The transformer spec is
researched from primary sources (the original paper, a current technical reference) and verified
by running code, exactly as the researcher normally does. Subtitle hits may inform how the story
*sounds*; they may not inform what it *claims*.

Recommended seed queries (record actual output, not expectations):

- Literal: `giggity`, `shut up, meg`, `what the deuce`, `grinds my gears`, `victory is mine`,
  `oh my god`, `you've got to be kidding`, `remember when`, `this is like that time`,
  `we now return to`, `meanwhile`.
- Regex: `^[A-Z]{6,}` (shouted lines) · `\(weakly\)|\(laughs\)|\(sighs\)` (delivery tags) ·
  `\b(road to)\b` (episode-title device).
- Semantic: see table. Hybrid as a cross-check when semantic and literal disagree.

Cost note: literal/regex are offline and instant; semantic/hybrid pull ~1.26 GB on first use.
Budget the download once, cache it under `~/.cache/fg_subtitles/`, and prefer literal for
frequency claims (it is exact) while semantic finds *scenes*.

---

## 9. Brief (locked 2026-10-10)

| Field | Proposed value | Why |
|---|---|---|
| Concept | The transformer architecture | as given |
| Style | Family Guy | as given |
| Form | Prose with cutaway beats (`* * *` separators); dialogue-forward, minimal narration | keeps prose tooling valid, keeps the show's engine |
| Length | 2,500 words (±15%) | room for ~5 cutaways plus a spine; 2,000 is tight |
| Audience | A curious non-specialist who has used ChatGPT but has no ML background | the show's register is broad; jargon must be earned |
| Hard constraint | No real people; no copying show lines; no narrator | AGENTS.md + §6 |
| Hard constraint | Every cutaway enacts exactly one MUST/SHOULD concept | §6 |
| Flag | `--review-plan` (pause after outline) | approve premise + mapping before prose |

---

## 10. Runbook (pipeline mapped to this run)

Standard `PIPELINE.md` Procedure A → R, with the deltas noted.

| Stage | Dispatch | Output | Delta from default |
|---|---|---|---|
| A1 | `new_run.py` | `brief.md` | form/length/audience from §9; assumptions list FG_Subtitles path + clone commit |
| A2a | `researcher` ∥ `style-critic` (profile) | `01_spec.md`, `01_questions.md`; `05_style_profile.md`, `05_style_stats.json` (+`05_style_evidence.md`) | style-critic runs `fg_corpus.py` + `fg_search.py` first; uses `--dialogue` |
| A2b | `planner` (premises) | `02_premises.md` | premises must differ in **cutaway strategy**, not just setting |
| A2c | `premise-judge` | `03_premise_choice.md` | judge scores each premise on: concepts dramatised, cutaway fit, self-correction potential |
| A2d | `planner` (outline) | `04_outline.md` | coverage matrix maps each concept → the cutaway that enacts it |
| A2e | **pause** (`--review-plan`) | — | human approves premise + mapping |
| A2f | `writer` (draft) | `drafts/draft_v1.md` | obeys §6 rules; dialogue-forward |
| A3/R | `number_paragraphs.py`; `cold-reader` ∥ `style-critic` (review) ∥ `fact-checker` (audit) ∥ `slop_lint.py`; then `fact-checker` (grade) | `reviews/v1/*` | style-critic review uses new rubric emphasis: cutaway function, tic discipline, register whiplash |
| A3 | orchestrator | `reviews/v1/digest.md` | same format |
| A4 | human | read draft + digest → `notes.md` → `/revise` | default |

Revision loop unchanged (max 3 rounds, KEEP locks verified by `lock_check.py`).

---

## 11. Milestones with acceptance checks

Each milestone is "done" only when its check passes.

- **M0 — Decisions (this doc).** Human answers §12. Check: brief fields fixed, semantic download
  approved or declined, form chosen.
- **M1 — Bridge tools.** ✅ *Done 2026-10-10.* `tools/fg_corpus.py`, `tools/fg_search.py`,
  `style_profile.py --dialogue`; tests in `tests/test_fg_corpus.py` and `tests/test_fg_search.py`
  (+ `--dialogue` cases in `tests/test_tools.py`). Check passed: `python -m unittest discover -s
  tests` → 54 tests OK. Evidence: corpus built (11 files, 12,755 words, 1,980 cues, 5 seasons,
  `labelled=True`); dialogue profile reports `dialogue_share 1.0`, `sent_mean 6.49`;
  literal/regex search return cited hits; hits written under `scratch/fg_hits/`.
- **M2 — Grounded style profile.** `styles/family-guy/` holds ≥8k words across ≥5 seasons;
  `05_style_profile.md` + `05_style_stats.json` + `05_style_evidence.md` exist with citations.
  Check: profile is `GROUNDED (n files)`; evidence file has ≥15 cited rows.
- **M3 — Concept spec.** `01_spec.md` (≥4 MUST concepts, every invariant falsifiable) +
  `01_questions.md` (4 mechanism, 3 transfer, 2 misconception, 1 boundary). Check: fact-checker
  can audit it; transformer claims traced to primary sources and to `scratch/` code.
- **M4 — Premises → judge → outline.** 3 genuinely different cutaway strategies; one chosen; a
  coverage matrix with every MUST concept assigned to a cutaway. Check: judge's `DECISION:` line
  is A/B/C; no MUST concept unmapped.
- **M5 — Outline approval** (`--review-plan`). Check: human signs off or edits.
- **M6 — Draft v1.** Check: word count within ±15%; slop lint run; no line copies >15 contiguous
  words from any excerpt (`lock_check.py`/manual spot check); stated length and format correct.
- **M7 — Review wave + digest.** Check: `accuracy.md`, `comprehension.md`, `style.md`, `lint.md`,
  digest all exist; cold-reader answers tagged `FROM THE TEXT` vs `PRIOR KNOWLEDGE`.
- **M8 — Human notes + one revision round.** Check: KEEP blocks survive `lock_check.py check`;
  blockers fixed or Overruled.

Stop rule: after M8, if the digest's teaching gaps are structural, prefer a **Pivot** over a
third polish round (the pipeline's own warning).

---

## 12. Decisions (locked 2026-10-10)

1. **Form:** prose with cutaway beats (`* * *` separators). Keeps the prose tooling valid.
2. **Length:** ~2,500 words (±15%) — room for a spine plus ~5 cutaways.
3. **Audience:** a curious non-specialist who has used ChatGPT but has no ML background.
4. **Search:** semantic **and** hybrid enabled; the ~1.26 GB index + model may be downloaded
   once and cached under `~/.cache/fg_subtitles/`. Literal/regex remain the source for exact
   frequency claims.
5. **`--review-plan`:** **yes** — pause after the outline for premise + concept-to-cutaway
   approval before any prose.
6. **Real people:** excluded (AGENTS.md rule 10); Family Guy's celebrity parody is out of scope.
7. **Scope:** the 4 MUST concepts in §5 stand; the researcher may promote at most one SHOULD
   concept if the outline has room, and must not add concepts without a matching cutaway.

Still open (non-blocking, settle during M1/M2): the exact season sample for `styles/family-guy/`
and the target excerpt word count.

---

## 13. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Dialogue-only corpus breaks `style_profile.py` metrics | `--dialogue` mode; treat numbers as a floor (§7.2) |
| Style fidelity drifts to catchphrase karaoke | `05_style_evidence.md` + review rubric on cutaway function and tic discipline |
| Explanations become lectures | Hard rule: no narrator; the correction must be in-character and event-driven |
| Accuracy slips because jokes simplify | Invariants I1–I4 are checkable per paragraph; fact-checker audits against the spec |
| Copyright | `styles/*/` git-ignored; ≤15 contiguous words; hits stored only in `scratch/`; FG repo read-only, pinned |
| Semantic index/model unavailable or too large | literal/regex carry frequency claims; semantic is optional enrichment |
| Premise looks funny but teaches nothing | Coverage matrix at M4; `--review-plan` pause at M5 |

---

## 14. Appendix — proposed commands and layout

```bash
# 0. one-time: clone the (read-only) corpus repo next to this one
git clone https://github.com/akbargherbal/FG_Subtitles.git ../FG_Subtitles
export FG_SUBTITLES_DIR="$PWD/../FG_Subtitles"

# 1. assemble style excerpts + citation index  (G1/G3, proposed tool)
python tools/fg_corpus.py --fg-dir "$FG_SUBTITLES_DIR" --out styles/family-guy \
    --seasons 1,5,10,15,21 --labelled --target-words 12000

# 2. search  (G2, proposed wrapper)  — every hit written under the run's scratch/
python tools/fg_search.py literal  "giggity"        --limit 20 --out runs/<run>
python tools/fg_search.py regex    "\\(weakly\\)"    --limit 20 --out runs/<run>
python tools/fg_search.py semantic "a cutaway that lands the joke" --limit 10 --out runs/<run>

# 3. style profile  (G4, small tool change)
python tools/style_profile.py profile styles/family-guy --dialogue \
    --out runs/<run>/05_style_stats.json

# 4. start the run, pause after the outline
python tools/new_run.py --concept "the transformer architecture" --style "Family Guy" \
    --form "prose with cutaway beats" --length 2500 \
    --audience "a curious non-specialist who has used ChatGPT but has no ML background"
```

Proposed additions to this repo:

```
plans/family-guy-transformer.md      # this document (orchestrator artifact)
tools/fg_corpus.py                   # DB/SRT -> styles/<slug>/ excerpts + citations.jsonl
tools/fg_search.py                   # literal/regex/semantic/hybrid wrapper (read-only)
tests/test_fg_corpus.py              # fixture SRT -> expected excerpt + citation
tests/test_fg_search.py              # literal hit returns a known episode
# style_profile.py                   # --dialogue mode (edit, not new file)
styles/family-guy/                   # git-ignored corpus (never pushed)
```

Recorded in `brief.md` assumptions when the run starts: the bridge tools' versions, the
`FG_Subtitles` clone commit, and whether semantic search was enabled.
