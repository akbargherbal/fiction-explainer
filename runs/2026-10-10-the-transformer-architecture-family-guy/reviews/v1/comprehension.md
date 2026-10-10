# Comprehension — draft v1

Supported & correct: 6 / 10 · Misconception probes passed: 2 / 2

Graded against `01_spec.md` §7. Only CORRECT-SUPPORTED counts as taught by the story. Locators checked against `reviews/v1/numbered.md` where needed.

| Q | Verdict | Basis | Note |
|---|---|---|---|
| Q1 | CORRECT-SUPPORTED | FROM THE TEXT [P35–P45, P73, P310] | Slice → sub-word fragments, numbers-only "card", meaning not stored: all located. The id → embedding-row step ("table lookup") is only implied by "same ticket, same card" and not restated; still correct. |
| Q2 | PARTIAL | text [P97–P109, P125] | Query=wanted / key=offering / 100% softmax row / weights blended into the drink are all right; but the **÷√d_k scaling is omitted** even though the story stages it [P104] and the key names it, and the drink is described as merging "the offerings" (keys) rather than the values. Learned-projection origin correctly flagged as prior. |
| Q3 | CORRECT-SUPPORTED | text [P148, P162–P174] | Attention (toss) + per-position fix, "add the original back on top" = residual/add, "smooth the binder" = norm, repeat per floor = depth. Only the label "feed-forward" is prior; both operations are located in the text. |
| Q4 | CORRECT-SUPPORTED | text [P200–P211, P299–P317] | One bar per token, weighted die = sample, pick dropped, re-ask with the pick appended and repeat to the end. Final-vector/logits naming is prior, structure is text. |
| Q5 | CORRECT-SUPPORTED | text [P99, P119, P122–P125, P135] | Early word joins every query–key comparison; changing it rescores everything; nothing is looked up. Exactly the key's "weights recomputed from the current input." |
| Q6 | CORRECT-PRIOR-KNOWLEDGE | text premise [P129, P157, P161, P187] + prior derivation | The answer is right, but the truncation/context-window prediction is inferred from prior knowledge (the reader says so); the story never stages a context window — it is the spec's optional concept that the outline cut. |
| Q7 | PARTIAL | text [P215–P227, P237, P241–P243] + prior | Sampling and "not truer, it's stranger" are supported; the **low-temperature half was never shown** (the machine only ever cranks the dial *up*), so "a low dial gives the same answer" is the reader's inversion, tagged partly prior. Matches accuracy F4. |
| Q8 | CORRECT-SUPPORTED | text [P73, P87, P89, P310] | M1 probe: correctly **False**, with the "no lookup / no meaning stored" locators that support it. |
| Q9 | CORRECT-SUPPORTED | text [P125, P133–P135, P145] | M2 probe: correctly **False**; "weighting is arithmetic, not intent" is the key's point. |
| Q10 | CORRECT-PRIOR-KNOWLEDGE | text statelessness [P161, P187] + prior | Correct account of where the picture breaks, but only the statelessness is from the text; context/RLHF/tools/decoding constraints are prior. Greedy/beam and reasoning modes are not named. |

## Teaching failures

- **Q2 — C2 (self-attention Q/K/V · softmax) · scene S4.** The scaling is on-stage ([P104] "Divide every score by root sixty four") but never lands, for two compounding reasons: the scene never shows the scaled scores, and the percentages it does show ([P109] "Sixty him, twenty five her, fifteen") do not follow from the scores and divisor ([P103]–[P104]) — so the "÷√64" stamp reads as flavour and the reader drops it (see `accuracy.md` F1). The stage also never labels the blended quantity as a *value* distinct from the offering keys, so the reader merges "the offerings." Fix direction: make the scaling's effect visible and softmax-consistent.
- **Q6 — context window (spec's optional concept, cut from the plan) · no scene.** The outline deliberately dropped the context-window/KV-cache optional, so nothing was meant to carry Q6. The reader built a correct answer by inference from the "only the current input, nothing filed" premise ([P129], [P161], [P187]); this is a scope gap, not a scene that failed. Direction: leave as prior-knowledge transfer, or add the optional beat if Q6 is to be story-supported.
- **Q7 — C4 / I8 (temperature) · scene S8 (vending machine).** The cutaway enacts only the high end of the dial ([P212]–[P237]: flatten → stranger). Low temperature (peaked bars ≈ greedy → the same pick twice) is never performed, so the "both runs agree" half had to be inferred. Direction: one low-dial callback beat (the machine repeating its pick) — same as accuracy F4.
- **Q10 — product boundary · no scene (by design).** The fiction is about the model loop, not the app around it, so greedy/beam decoding, instruction tuning/RLHF, tool use and constrained decoding are inherently prior knowledge. The one story-borne element (memoryless, one-bare-sentence input) did land ([P161], [P187]). No fix needed beyond acknowledging the boundary is out of the story's scope.

## Reader experience

- Scene 2 (slicer/tickets) [P34–P81] was the hardest stretch: no anchor for what a "card" was on first pass; the swap-vs-stickers contrast took two readings.
- Scene 4's drink percentages read as a joke before landing as a weighted blend; [P109]/[P111] needed re-reading.
- Scene 10's stall [P266–P282] stayed ambiguous — unclear whether the point was queue/throughput or architecture.
- Repetition read as a teaching tic rather than dialogue: "same ticket, same card"/"Next!", the echo-triples [P101, P121, P173], and the "it knows / doesn't know" exchange; Scene 5 [P132–P146] was felt as a rerun of Scene 4 and the most "lectured" stretch — the reader would cut it.
- Memorable anchors that did land: "Divide every score by root sixty four" [P104], the pickled-egg climb and repetition [P217–P225], "noise is loud" [P243], "It asks again into nothing" [P327], and the assembled payoff sentence [P315–P317].
