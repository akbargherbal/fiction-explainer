# Brief

- **Concept / framework:** the transformer architecture
- **Style target:** Family Guy
- **Style slug:** family-guy  (excerpts expected in `styles/family-guy/`)
- **Form:** prose with cutaway beats
- **Target length:** 2500 words
- **Audience:** a curious non-specialist who has used ChatGPT but has no ML background
- **Created:** 2026-10-10

## Hard constraints

- No real people as characters (AGENTS.md rule 10); Family Guy parodies celebrities constantly — this is out of scope.
- No narrator and no lecture: no "in other words", "essentially", "think of it like". Family Guy has no narrator.
- Every cutaway enacts exactly one MUST/SHOULD concept (see `plans/family-guy-transformer.md` §6).
- Style is imitated through patterns only. Never copy more than 15 contiguous words from any excerpt or subtitle.
- Generation is a *sampling* from a distribution, not a lookup: no scene may imply the model looks a fact up or "knows" it (invariant I1/I2).

## Assumptions made by the pipeline

- Form defaults to **prose with cutaway beats**: dialogue-forward prose, cutaways separated by `* * *` (per the approved plan, keeps the repo's prose tools valid).
- Length 2,500 words ±15%.
- Audience as given: non-specialist who has used ChatGPT, no ML background.
- Style target is **GROUNDED**: 11 excerpt files in `styles/family-guy/` (12,755 words, 1,980 cues, seasons 1/5/10/15/21), built by `tools/fg_corpus.py --labelled` from the read-only `FG_Subtitles` clone at `../FG_Subtitles` (commit `3d4988f`).
- The measured style stats must be read in **dialogue mode** (`style_profile.py --dialogue`): subtitles carry no quote marks, so without the flag the profile would misreport dialogue share as 0.
- Semantic + hybrid subtitle search is enabled; the ~1.26 GB index + model download was approved (plan §12).
- `--review-plan` is on: pause after `04_outline.md` for the human to approve the premise + concept-to-cutaway mapping.
- Concepts in scope (MUST): tokens→embeddings, self-attention (Q/K/V · softmax), the block and stack, next-token prediction. Optional: multi-head, position, context window.

## Pivot log

(pivot instructions from notes.md are appended here)
