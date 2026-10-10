# Accuracy audit — draft v1

BLOCKERS: 1 · WARN: 2 · NOTE: 4 · Coverage: MUST 4/4 dramatized

Read: `01_spec.md`, `04_outline.md`, `02_premises.md` (mapping labels), story via `reviews/v1/numbered.md`.
Code: `scratch/attention_demo.py` (researcher's), `scratch/f1_scene4_numbers.py` (written for this audit).
Numbers below are exact printed output.

## Findings

### F1 BLOCKER — [P103]–[P109]
- **Story states or implies:** the row is scored `Two, one, and five`, every score is `divide[d] by root sixty four`, the row is forced to `add up to one hundred percent`, and the blend is `Sixty him, twenty five her, fifteen the other one` — i.e. scores `[2,1,5]`, divisor `√64 = 8`, weights `[0.60, 0.25, 0.15]`.
- **Spec / evidence:** spec C2 + §6 (scaled dot-product demo). Ran `scratch/f1_scene4_numbers.py`:
  ```
  raw scores: [2. 1. 5.]
  sqrt(64)=8 (story's divisor)      -> weights [0.2996 0.2644 0.4360] = [29.96 26.44 43.60]
  sqrt(4)=2  (spec demo's d_k=4)    -> weights [0.1643 0.0996 0.7361] = [16.43  9.96 73.61]
  story claims weights = [0.60 0.25 0.15]
  closest divisor to reproduce [.60 .25 .15]: c = 20.0 err = 0.55755
  ```
  No divisor on `[2,1,5]` produces `[0.60,0.25,0.15]` (best-fit error 0.56 over a 20k-point grid). Read in the order given, the highest score (5) gets the *smallest* share (15%) — softmax is monotonic in its logits, so that is impossible. The spec's own demo uses the same raw scores `[2,1,5]` but `d_k = 4`, `√d_k = 2` (`01_spec.md` §6, `attention_demo.py` §3); the draft borrows those scores but the `d_k = 64` divisor.
- **Why it matters:** C2 is a MUST concept and this is its only worked number set. It is arithmetically false and, in reading order, inverts the "better match → bigger weight" relationship the scene is built to teach. The surrounding mechanism (score → scale → softmax → % → blend, row sums to 100) is dramatized correctly, so the defect is local to the three figures.
- **Fix direction (no rewrite):** recompute the triple so it is softmax-consistent — either keep the demo's `÷2` (`16 / 10 / 74`) or use `÷√64 = ÷8` (`30 / 26 / 44`).

### F2 WARN — [P99]–[P101], [P123]
- **Story states or implies:** every wanted card is matched against every offering card, `No exceptions`; `That first word meets every card. That's the whole job.` (all-to-all query–key comparison with no mask).
- **Spec / evidence:** the run targets the ChatGPT family, which is *decoder-only*; decoder self-attention is causally masked — position `i` can attend only to positions `≤ i`, with future scores set to `−inf` before the softmax. Source: Wikipedia, *Transformer (deep learning)* lead + §3.7.3 Masked attention (`en.wikipedia.org/wiki/Transformer_(deep_learning)`, revision 1379435465, fetched 2026-10-10), and causal-masking references (Raschka FAQ, *Causal Attention in GPT-Style Language Models*). `01_spec.md` line 185 records the researcher reading "masked attention", yet C2 says "every query vs every key" and §6's demo is unmasked.
- **Why it matters:** "no exceptions" implies a token can use words that come *after* it; for a GPT-style model the future is invisible. This is imprecision, not an M# (M1–M5 are unaffected), and the spec/outline explicitly authorised full attention — so the human may Overrule.
- **Fix direction (no rewrite):** qualify the all-to-all claim for the generating direction, or leave as spec-sanctioned simplification.

### F3 NOTE — [P148]–[P167]
- **Story:** per floor — toss the whole pile (attention, [P148]), each worker fixes only their own page (feed-forward, [P150]–[P153]), `Pour the original back on top` (residual, [P162]–[P166]), `smooth the binder` (norm, [P167]).
- **Spec:** C3 — *each* of the two sub-layers is wrapped as `LayerNorm(x + Sublayer(x))`. The story shows only the feed-forward wrap; the attention sub-layer's residual + normalisation is never shown.
- **Why it matters:** omission, not falsehood; a careful viewer could infer the residual wraps only the feed-forward. The shown residual is correctly rendered as *add*, not keep ([P165]–[P166]).
- **Fix direction:** one extra beat pouring the original back after the toss as well.

### F4 NOTE — [P215]–[P237]
- **Story:** the temperature thread is one-directional — turn the dial *up* ([P212]–[P237]) so the chart `flatten[s]` and the pick turns `stranger`. Low temperature (sharpen toward the top token / ≈ greedy) is never dramatised.
- **Spec:** C4 and I8 both describe the low end; answer-key Q7 and the outline's ending ("why a low dial gives the same answer twice") depend on it. `attention_demo.py` §2 shows the low end (T=0.5 → max `0.8668` vs T=2.0 → max `0.5065`).
- **Why it matters:** half of I8 is absent, so a reader cannot support the promised "low dial = same answer" inference from the text.
- **Fix direction:** a one-beat callback on the low dial (the machine picking the same token twice).

### F5 NOTE — [P58]–[P70]
- **Story:** position is added as stickers on the **tickets** ([P64]–[P66]) and swapping tickets `flips the reading` ([P67]–[P69]).
- **Spec:** C6 — positional information is *added to the embeddings* (the vectors/`cards`), not to the token ids (`tickets`).
- **Why it matters:** mapping slippage — the order-sensitivity effect is right, but position is attached one layer too early. `02_premises.md` L51 licensed name-tags, so this is minor.
- **Fix direction:** put the sticker on the card; keep the ticket/tray swap as the trigger.

### F6 NOTE — [P71]
- **Story:** `Stickers matter, and the cards don't.` Read alone, the embeddings don't matter — the opposite of I5 (the vector is the only thing the model sees).
- **Spec:** I5 / M1. The next two lines repair it: [P72] `And the cards are the meaning, right?` → [P73] `Cards are numbers, sir. Meaning is not in the building.`
- **Why it matters:** small — the exchange makes clear "the cards don't [carry meaning/position]", so a reader following the dialogue is unlikely to keep the literal reading.
- **Fix direction:** make the dropped verb explicit in one phrase.

## Invariants

| Invariant | Status | Paragraphs |
|---|---|---|
| I1 weights from current input; nothing fetched | OK | S4 cast-swap rescoring [P113]–[P119], [P125], `no last list` [P128]–[P129]; slicer `we don't ask questions` [P74]–[P75] |
| I2 output is a distribution; token is sampled | OK | bars + `weighted die` + re-ask [P199]–[P211]; `It drew the likely one, and it got lucky` [P323] |
| I3 order-blind without position | OK | [P58]–[P70]; the set-reading `didn't move` [P61]–[P63] matches the spec's own C6 phrasing (demo shows the rows permute) |
| I4 heads are parallel, concatenated | OK | eight simultaneous rankings [P253]–[P265]; forced queue jams [P266]–[P282] |
| I5 embedding is numbers, not a definition | OK | `Numbers only` [P43]–[P45], [P47], `Meaning is not in the building` [P73], `Numbers only. It never had the word` [P310] |
| I6 feed-forward is per-position | OK | `fix your page, and only your page` [P150]–[P153] |
| I7 residual = add, not store | OK | `We add the original. Nobody is keeping anything here` [P162]–[P166]; `no cabinet` [P156]–[P161] |
| I8 temperature reshapes the same distribution | OK (high-T only) | flatten + rising pickled-egg bar [P215]–[P219], [P237]; low-T direction absent (F4) |

## Coverage

| Concept | Priority | Status | Paragraphs |
|---|---|---|---|
| C1 tokens → embeddings | MUST | DRAMATIZED | S2 [P34]–[P81]; callback [P307]–[P310] |
| C2 self-attention Q/K/V · softmax | MUST | DRAMATIZED | S4 [P97]–[P131] (numbers wrong — F1) |
| C3 block and stack | MUST | DRAMATIZED | S6 [P147]–[P180] |
| C4 next-token prediction + sampling | MUST | DRAMATIZED | S8 [P199]–[P237]; callback S12 [P296]–[P323] |
| C5 multi-head attention | SHOULD | DRAMATIZED | S10 [P253]–[P282] |
| C6 position (folded) | SHOULD | DRAMATIZED (beat) | S2 [P56]–[P70] |

MUST coverage: **4 / 4**. All five staged misconceptions (M1–M5) are raised in-character and corrected by an event and/or ≤2-utterance reply; none survives as a taught belief.

## Metaphor strain

Mapping labels come from `02_premises.md` (the chosen premise A); `04_outline.md` uses none.

| Row | Label | Breaking part | Does the story lean on it? |
|---|---|---|---|
| C2 speed-dating matchmaker | ANALOGOUS (L47) | matchmaker reads as a chooser (M2) | **No.** Procedure read off a card [P99], the cast-swap rescoring [P113]–[P119], and the flat refusal [P125]–[P127] defuse it. (F1 is an arithmetic slip, not the metaphor.) |
| C3 six-floor office tower | ANALOGOUS (L48) | tower reads as a sentence library (M3) | **No.** `There is no cabinet` [P156]–[P161] and `More finished, not more filed` [P175]–[P178]. (F3 is an omission, not the metaphor.) |
| C6 position folded into C1 | ANALOGOUS (L51) | easy to drop / position vs embeddings | **Mild.** Kept to a beat with no extra `* * *`; but stickers land on tickets, not cards (F5). |
| C5 eight clerks | EXACT (L50) | clerks read as a sequence | **No.** The forced queue jams the box [P266]–[P282], showing parallel not chained. |

## Unverifiable

- `Ninety two snacks` [P201], [P297]: set size for the cutaway is narrative, not a source claim.
- The exact next-word choices attributed to the machine ([P181], [P229]/[P231], [P317], [P337]): narrative, no external check.
- Whether any real 2017 model emits exactly the spec's 3-token demo numbers: the demo is a stylised `d_k = 4` example, not the paper's `d_k = 64` — the draft mixes the two (see F1).
