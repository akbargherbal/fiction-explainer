# fiction-explainer

Turn **"concept X, explained in style Y"** into an original piece of fiction that actually teaches X.

A team of role-specialised agents shares state through files. The human steers at one point: reading a draft plus a short digest, then writing `notes.md`.

> This file is the tool-neutral contract. Claude Code gets thin wrappers in `.claude/` (agents + slash commands). The orchestration procedure lives in [PIPELINE.md](PIPELINE.md). Porting to Codex / Gemini CLI / OpenCode means re-creating the roles below in that tool's agent format and pointing its orchestrator at PIPELINE.md.

## Roles

| Role | Job | Writes |
|---|---|---|
| `researcher` | Builds the concept spec: core concepts, invariants, misconceptions, verified examples, comprehension questions + answer key | `01_spec.md`, `01_questions.md` |
| `style-critic` | **profile mode:** builds the style profile from excerpts. **review mode:** audits a draft against it | `05_style_profile.md`, `05_style_stats.json`, `reviews/vN/style.md` |
| `planner` | **premises mode:** 3 genuinely different premises. **outline mode:** scene plan + coverage matrix | `02_premises.md`, `04_outline.md` |
| `premise-judge` | Picks one premise against the spec and style (fresh context, never the planner) | `03_premise_choice.md` |
| `writer` | The **only** role that writes story text. Drafts and revises | `drafts/draft_vN.md`, `drafts/draft_vN.changes.md` |
| `fact-checker` | **audit mode:** checks the story against the spec, runs code to verify claims. **grade mode:** grades the cold reader's answers | `reviews/vN/accuracy.md`, `reviews/vN/comprehension.md` |
| `cold-reader` | Reads only the finished story, answers comprehension questions, reports confusion | `reviews/vN/cold_read.md` |

The orchestrator (the main session) coordinates, runs the Python tools, and writes `reviews/vN/digest.md`. It never writes story prose, spec content or reviews.

## Run directory

```
runs/<slug>/
  brief.md                 # input: concept, style, form, length, constraints, assumptions
  01_spec.md  01_questions.md
  02_premises.md  03_premise_choice.md  04_outline.md
  05_style_profile.md  05_style_stats.json
  drafts/draft_vN.md       # agent-written, never edited in place by humans
  drafts/draft_vN.locked.md    # draft + KEEP markers (generated from your notes)
  drafts/draft_vN.changes.md   # writer's account of what changed and why
  reviews/vN/{numbered,cold_read,style,lint,accuracy,comprehension,digest}.md
  notes.md                 # YOUR input for the next round (see templates/notes.md)
  notes_history/round_N.md # consumed notes
  plans_archive/           # superseded plans (after a Pivot or premise regeneration)
  scratch/                 # code the fact-checker runs (git-ignored)
```

`python tools/run_status.py status runs/<slug>` tells you (and the orchestrator) exactly what is done and what is next. It is derived from which files exist, so any interrupted run can resume.

## Hard rules (every agent)

1. **Files are the shared state.** Read and write inside the run directory. Pass paths between agents, never pasted contents.
2. **One owner of prose.** Only the `writer` writes or edits story text. Everyone else writes notes about it.
3. **Critics give notes, not rewrites.** At most one short example phrase per note, and only to show direction.
4. **Original text only.** Style is imitated through patterns (rhythm, diction, structure), never by reproducing the author's sentences. Never copy more than 15 contiguous words from any excerpt into any output file. Excerpts in `styles/` are analysed, never copied into `runs/`.
5. **Dramatize, don't lecture.** The story teaches through events, choices, consequences and dialogue. A narrator that explains the concept ("in other words…", "essentially…") is a defect unless the style target does exactly that.
6. **Accuracy is non-negotiable.** Nothing the story states or implies about the concept may contradict the spec's invariants. Unverified claims are marked, never smoothed over.
7. **Reference paragraphs by ID.** Reviewers and the human cite `[P12]`, using the numbering from `reviews/vN/numbered.md` (`python tools/number_paragraphs.py`).
8. **Locked text is sacred.** Text inside `<!-- KEEP --> … <!-- /KEEP -->` must be preserved verbatim, markers included, in every later draft.
9. **No invented sources.** Cite what you actually read; mark confidence.
10. **No real people as characters** unless the brief explicitly asks.

## Draft format (writer output)

- One `# Title` line, then prose. No front matter, no author's note, no appendix explaining the concept (unless the brief asks).
- Scenes separated by a line containing only `* * *`.
- Plain Markdown; emphasis sparingly.

## Human entry points

1. **The brief** — `/explain "<concept> | <style>"` creates `brief.md` (or fill `templates/brief.md` yourself).
2. **Style excerpts** — drop text into `styles/<style-slug>/` *before* the run for real style fidelity.
3. **The review** — read `drafts/draft_vN.md` + `reviews/vN/digest.md`, then write `notes.md` (sections `Keep`, `Change`, `Pivot`, `Reject`, `Overrule`) and run `/revise`.
4. **Overrides** — edit a draft yourself as `drafts/draft_vN.edited.md`; `/revise` locks everything you changed.

Optional: `/explain … --review-plan` pauses after the outline so you can approve the premise before any prose is written.

## Tools (`tools/`, Python 3.9+, standard library only)

| Tool | Purpose |
|---|---|
| `new_run.py` | Create a run directory and brief |
| `run_status.py` | What's done / what's next; latest run; archive a plan |
| `number_paragraphs.py` | Stable `[P#]` view of a draft for reviewers |
| `slop_lint.py` | Heuristic lint for LLM-fiction tells |
| `style_profile.py` | Measure style from excerpts; compare a draft to the reference |
| `lock_check.py` | Apply Keep locks from notes, adopt human edits, verify locks survived, diff drafts |
| `archive_notes.py` | Archive consumed notes, reset `notes.md` |
| `notes_digest.py` | Aggregate notes across runs to spot recurring preferences |

Run the tests with `python -m unittest discover -s tests -v`.
