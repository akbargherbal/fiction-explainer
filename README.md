# fiction-explainer

Give a coding agent **"concept X, in style Y"** and let a small team of agents research it, plan it, write it, fact-check it, cold-read it and critique the voice. You read one draft plus a short digest, write notes, and iterate.

The bet: one-shot "explain X like author Y" produces gappy pastiche, but an agentic loop with *external checks* (a spec to verify against, code that gets run, a reader who only sees the story, measurable style stats) fixes most of the structural problems. It does **not** replace taste. That stays with you.

Built for **Claude Code** first. The contract is tool-neutral (`AGENTS.md`, `PIPELINE.md`), so porting is mostly copying role prompts.

## Quick start

```bash
git clone <your repo> && cd fiction-explainer
python --version            # 3.9+ ; tools use only the standard library
python -m unittest discover -s tests -v

# Optional but strongly recommended for style fidelity:
mkdir styles/terry-pratchett
# drop 3-10 excerpts (.txt/.md, ~5k+ words total) you have the right to analyse there

claude                      # start Claude Code in this folder
> /explain Python's asyncio event loop | Terry Pratchett
```

If Claude Code was already open when you added the agents, restart it (or run `/agents`) so they are picked up.

The style slug is the lower-cased, hyphenated style name (`Terry Pratchett` → `styles/terry-pratchett/`). `new_run.py` prints the slug and how many excerpt files it found.

## What happens

```
/explain "X | Y"
  ├─ researcher ─────────┐  (parallel)  concept spec, invariants, misconceptions, quiz + key
  ├─ style-critic ───────┘              style profile from excerpts + measured stats
  ├─ planner → 3 premises
  ├─ premise-judge → picks one (fresh context)
  ├─ planner → outline + coverage matrix
  ├─ writer → drafts/draft_v1.md
  └─ review wave (parallel)
       ├─ cold-reader   sees only the story; answers the quiz; flags confusion
       ├─ fact-checker  audits story vs spec, runs code; later grades the cold read
       ├─ style-critic  rubric vs profile + measured stats
       └─ slop_lint.py  mechanical tells
     → reviews/v1/digest.md
```

You then read `drafts/draft_v1.md` and `reviews/v1/digest.md`.

## Your input: `notes.md`

`runs/<slug>/notes.md` is created for you. Fill only what you need:

| Section | Meaning | Effect |
|---|---|---|
| **Keep** | Quote passages you like: `- "exact text"` or `- "start of it ... end of it"` | Wrapped in `<!-- KEEP -->`; the writer must preserve them verbatim, and `lock_check.py` verifies it |
| **Change** | Targeted revisions, cite `[P12]` from `reviews/vN/numbered.md` | Only flagged passages are touched |
| **Pivot** | Structural moves ("swap the central metaphor for…") | Archives the plan and re-plans from the premise |
| **Reject** | Things never to do again in this run | Binding for later rounds |
| **Overrule** | Critic findings that are wrong or intentional: `- F3: narrator is unreliable on purpose` | Downgraded to a note, not re-raised |

Then run `/revise`. You can also edit the draft directly: save your copy as `drafts/draft_vN.edited.md` and every paragraph you changed or added is locked automatically.

Accuracy **blockers** are always fixed, even if you write nothing, unless you Overrule them.

Useful flags: `/explain ... --review-plan` pauses after the outline so you can approve the premise before any prose; `/explain --resume <run>` continues an interrupted run; `--length 3000`, `--form "dialogue"`, `--audience "..."`.

## `taste.md`?

Deliberately not created. Each run keeps its own notes in `notes_history/`. After a few runs:

```bash
python tools/notes_digest.py
```

shows which words and requests recur across your notes. Promote the ones that genuinely repeat into a persistent file then.

## Tuning

- **Models.** Add `model: opus` (or another) to an agent's frontmatter in `.claude/agents/`. Worth doing for `writer`. If your tool supports multiple model families, put a *different* family on `fact-checker` and `cold-reader`: five hats on one model agree with each other too easily.
- **Cost.** A first draft is about 8-10 agent dispatches; a revision round about 6. Trim the review wave first (drop `style-critic` review mode, keep the lint script) if you need it leaner.
- **Permissions.** `.claude/settings.json` pre-approves the pipeline's own tools and writes under `runs/`. Trim it if you prefer prompts.
- **`python` vs `python3`.** Commands use `python`. If you only have `python3`, search-and-replace.

## Known limits (read these before trusting the digest)

- **Cold-reader contamination.** The cold reader is an LLM that already knows most frameworks. It must tag every answer `FROM THE TEXT` or `PRIOR KNOWLEDGE`, and only the former counts, but it can still be wrong about its own sources. Treat the score as a signal, not a measurement.
- **Same-model blind spots.** Critics share the writer's tastes if they share its model.
- **Style fidelity needs excerpts.** Without them the profile is flagged `UNGROUNDED` and rests on model memory.
- **Measured style is a proxy.** Sentence-length and punctuation stats catch obvious drift, not voice.
- **Diminishing returns.** Past ~3 revision rounds the draft tends to get blander. The pipeline warns you.
- **Copyright.** `styles/*/` is git-ignored on purpose: excerpts are other people's text. Outputs are original fiction in a manner, not reproductions. Agents are instructed never to copy more than 15 contiguous words from an excerpt.

## Layout

See [AGENTS.md](AGENTS.md) for roles, run-directory layout and hard rules, and [PIPELINE.md](PIPELINE.md) for the exact orchestration procedure.
