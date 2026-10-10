# Draft v1 — digest
Run: 2026-10-10-the-transformer-architecture-family-guy · Words: 2,640 · Style grounding: GROUNDED (12 files, seasons 1/5/10/15/21, dialogue mode)

| Check | Result |
|---|---|
| Accuracy | 1 blocker · 2 warnings · 4 notes |
| Coverage (MUST concepts dramatized) | 4 / 4 |
| Cold read (answers supported by the text) | 6 / 10 · misconception probes 2 / 2 |
| Style fidelity (mean of 1–5 rubric) | 2.7 |
| Slop lint | 1 flag: opener-run (5 hits, all deliberate repetition) |

## Blockers (fixed automatically next round unless you Overrule)
- F1 [P103]–[P109] the C2 worked numbers are false: `softmax([2,1,5]/√64) = [30,26,44]%`, not `[60,25,15]%`; no divisor yields the shown split, and in reading order the top score gets the smallest share (softmax is monotonic). Verified in `scratch/f1_scene4_numbers.py`. C2 is the only MUST concept with a worked number set, so this is load-bearing.

## Teaching gaps
- Q2 [P97]–[P109] (C2/self-attention, S4) the ÷√d_k scaling never lands — the scene stages it but shows no scaled scores, and the shown percentages (F1) don't follow from the scores, so "divide by root sixty four" reads as flavour. Also the blend is described as merging the *keys* rather than the values.
- Q7 [P215]–[P237] (C4/I8, S8) only the high-temperature direction is dramatised; the low-dial half ("a low dial gives the same answer, and is not truer") is never shown, so the reader had to invert it.
- Q6 context window was the spec's optional concept the outline cut — no scene was meant to carry it (scope, not a failed scene).
- Q10 product boundary (decoding/tuning/tools) is prior knowledge by design; only statelessness is text-borne.

## Style
- Closest to the voice: [P225] "It's more random. Pickled egg…" · [P243] "It's not smarter. It's stranger…" · Furthest: [P135] "Nobody's deciding. It added up percentages…" (mechanism narration in a character's mouth — the profile's named worst failure mode).
- Top pastiche tells: (1) five of six cutaways are the same bored "sir"-addressed functionary; (2) five triple-repeats share one `X. X. X.` template; (3) every cut launches on a bare assertion — no attested opener ("Remember when…", "We now return to…").
- Measured drift: no metric outside ±35%, but questions −34%, first/second person ≈−33%, lexical variety −25%; "well"/"yeah" (the corpus's #2/#4 content words) appear zero times. Zero semicolons, zero em dashes — matches the reference.

## What's working (Keep candidates)
- [P225] "It's more random. Pickled egg…"
- [P243] "It's not smarter. It's stranger…"
- [P309] "Numbers only. It never had the word…"
- [P217] "Not the same, but flatter. And the…"
- [P23] "It is a beige box with opinions…"

## Suggested notes (copy what you agree with into notes.md)
- Change: [P103]–[P109] recompute the C2 triple so it is softmax-consistent (÷2 → 16/10/74, or ÷√64 → 30/26/44).
- Change: [P135] and [P89], [P187] stop explaining mechanism — hold the fix to ≤2 short utterances and let the event carry it, as [P243] does.
- Change: S4 name the blended quantity as the *value* distinct from the offering cards.
- Change: [P215]–[P237] add a one-beat low-dial callback (the machine repeating its pick) to complete I8.
- Change: S2, S4, S6 give each miniature one beat that tips "one notch past plausible" (the pickled-egg beat is the template).
- Change: vary the frames/templates — one invented-broadcast cutaway; repetition varied (doubling, echo-as-question) instead of five identical triples.
- Change: seed back-channels ("yeah", "well", "right") and accusation-shaped questions ("Are you kidding?") into the family scenes.
- Change: [P58]–[P70] put the position stickers on the cards, not the tickets.
- Overrule candidate: F2 (decoder causal mask) — the spec authorised "every query vs every key"; Overrule it if you accept the simplification, otherwise qualify it for the generating direction.
- Pivot: not indicated. The spine (cutaway-is-the-mechanism, wager ledger) is working; the fixes are local.

## Read
drafts/draft_v1.md · reviews/v1/{accuracy,comprehension,style,lint}.md · reviews/v1/numbered.md
