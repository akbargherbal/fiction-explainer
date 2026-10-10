# Style review — draft v1

Grounding: GROUNDED (12 files, 14,366 words, seasons 1/5/10/15/21; compared in **dialogue mode** — draft is 2,640 words, well over the 300-word floor, so the comparison is valid). Run-specific emphasis per plan §7/§10: cutaway function, tic discipline, correction length / narrator risk, register whiplash.

## Rubric (1-5, each with evidence as [P#])

| Dimension | Score | Evidence |
|---|---|---|
| **Rhythm** | 3 | The staccato engine is right: half the beats are ≤6 words (measured short_sent_share 0.645 vs ref 0.501), p90 11 matches exactly, no beat reaches 30 words. Real ping-pong: [P53]→[P54], [P86]→[P87], [P244]→[P245]. But the rhythm is *too* regular — almost every line is "X, and Y, and Z" coordination or a three-part repeat, so the acceleration feels metronomic, not escalating. |
| **Diction** | 2 | Clean and unfussy, but the corpus's actual voice is missing. The reference's #2 and #4 content words are **"well" (67)** and **"yeah" (60)** — both appear **zero** times in the draft. Crude/vulgar vocabulary (a favoured register) is absent; the one flash of mock-formal is Stewie [P21], [P23]. Contractions are present but "cannot" (5) rivals "can't" (5), where the show strongly favours the contraction. |
| **Imagery** | 3 | The invented-artefact habit is exactly right and original: slicer/ticket card [P39]-[P49], speed-dating floor [P97]-[P109], six-floor tower [P147]-[P166], vending machine [P199]-[P237], eight clerks [P253]-[P263]. But **five of six cutaways are the same image**: a bored functionary at a processing station, addressed as "sir". One idea, reused; the profile's frame vocabulary (fake TV / ad / news / "we now return to") is unused. |
| **POV & distance** | 3 | Literally correct: no narrator, no interiority, present tense, unattributed dialogue, zero distance. The risk is structural, not literal — the corrections start **explaining mechanism** (see Notes 4), so the piece teaches by having characters narrate the lesson. That is the profile's named worst failure mode wearing Brian's voice. |
| **Scene shape** | 3 | Full cutaway grammar is present and tracked (audit below): hard cuts via `* * *`, buttons, reactions, and a genuine callback in S12. Deficit: three miniatures (S2, S4, S6) are literal procedure with no comic tip — the "one notch past plausible" escalation is thin; only S8 (pickled-egg rise) and S10 (the queue jam) actually escalate. Buttons also repeat the same register ("Next!" / "Toss the pile."). |
| **Dialogue** | 2 | Interruptions and talking-past are real ([P133]-[P135], [P275] "Timeout." / [P276] "Ding."). But voices **flatten toward a single clipped clerk register**: the procedural cutaway syntax bleeds into the family scenes, so Peter, Lois, Brian and the clerks share one sentence shape. Distinctions survive by *function* (Peter asserts, Lois doubts, Brian corrects, Chris is literal [P184]) but not by *music*. |
| **Tone** | 3 | Deadpan temperature held; the sincere beat is correctly punctured ([P332] "It gets us" → [P339] "barely" → [P343] "Ding."). The wager ledger gives Peter's confident-wrongness a cost, per the profile. But the piece is **joke-sparse** — long stretches are procedure with no punch, and register whiplash (crude/collision) is nearly absent. |

**Mean: 2.7**

## Cutaway grammar audit (run-specific)

Set-up → hard cut → escalating miniature → flat button → in-character reaction; and one-concept-per-cutaway.

| Cutaway | Set-up | Miniature + escalation | Button | Reaction / correction | Concepts |
|---|---|---|---|---|---|
| **S2** slicer [P34]-[P81] | [P24] "one word… steers the whole sentence" | ✓ procedure; escalation weak | [P81] "That's the sentence." | S3 [P82] Peter + [P87]/[P89] Brian | **C1 + folded C6 — two** |
| **S4** speed-dating [P97]-[P131] | [P96] "the first word is the whole sentence" | ✓ cast-swap changes every % | [P131] "Extremely." | S5 [P132] + [P135] Lois | C2 ✓ |
| **S6** tower [P147]-[P180] | [P146] "Think harder, box!" | ✓ procedure; escalation weak | [P180] "Toss the pile." | S7 [P181] Chris + [P187] Brian | C3 ✓ |
| **S8** vending [P199]-[P237] | [P197]-[P198] the dial | ✓ **strongest** — [P217], [P225] | [P237] "Chances are flat." | S9 [P238] + [P243]/[P248] | C4 ✓ |
| **S10** clerks [P253]-[P282] | [P250]-[P252] "One at a time!" | ✓ jam/timeout [P270]-[P276] | [P282] "Then it stays stuck." | S11 [P283] | C5 ✓ |
| **S12** callback [P296]-[P327] | [P295] "all by itself" | ✓ re-read calm, shape changed | [P327] "It asks again into nothing." | S13 [P328] | **C4 callback + C1 beat — two** |

Verdict: the *spine* of the device is executed. Two rule-strain points — S2 and S12 each carry a second concept (C6, C1) — and the set-up lines are assertions rather than the profile's named opener formulas.

## Measured drift

`style_profile.py compare --dialogue` reports **no metric outside tolerance**. That is a genuine strength (the draft is not obviously prose-shaped), but the near-boundary rows are the real story:

- **questions_per_1k 17.8 vs 27.1 (-34%)** — at the edge. The reference's questions are *accusations* ("Are you kidding?"); the draft's are mostly flat procedural queries ("What about the tray?"). [P13] is the rare true accusation.
- **first_person -35% / second_person -32%** — both at the edge. Family Guy runs on "I" declarations and direct address; the procedural cutaways push the draft toward third-person object talk.
- **mattr_250 0.474 vs 0.634 (-25%)** — low lexical variety, consistent with the flattening observed in Dialogue.
- **semicolons 0, em dashes 0** — matches the reference exactly; zero drift. (Per the run instruction, either would have been an automatic flag; there are none.)

None of these *by themselves* fails the voice, but together they describe a draft that is rhythmically on-model and lexically off-model.

## Closest to the voice / furthest from it

- **Closest: [P225]** "It's more random. Pickled egg. Pickled egg. Pickled egg." — the one place a cutaway escalates past plausible into a real gag while still teaching (temperature flattening), and the repetition inverts the expectation.
- **Closest: [P243]** "It's not smarter. It's stranger. You turned up noise, and noise is loud." — correction in a character's mouth, ≤2 sentences, no mechanism lecture. This is the model the other corrections should follow.
- **Closest: [P309]** "Numbers only. It never had the word. It only ever had numbers." — callback that carries C1 and lands differently, exactly the profile's callback rule.
- **Furthest: [P135]** "Nobody's deciding. It added up percentages, and everything changes when you change the start." — a character explaining the mechanism, three clauses deep; the narrator-risk the profile names as the worst failure.
- **Furthest: [P192]-[P197]** — Peter's "new plan / I make it creative" run is largely restatement; the family scenes here are process, not personality.

## Pastiche tells

Surface mechanics deployed without the habit underneath them:

1. **The same stock bit-player in every cutaway.** The profile's "stock bit-player whose whole existence is the gag" is real, but using a bored "sir"-addressed functionary five times converts a device into a template.
2. **Repetition as one template.** Five triple-repeats — [P12], [P101], [P121], [P173], [P225] — are all the identical `X. X. X.` shape. The show varies repetition (doubling "you know what", stacking "no no no", echoing a word back as a question).
3. **No named cutaway opener.** The profile lists attested set-up buttons ("Remember when…", "This is just like…", "We now return to…", "Meanwhile…"); the draft launches every cut on a bare assertion, so the cuts are legible but not *framed*.
4. **"Ding." as a recurring button** [P276], [P324], [P336], [P343] — deployed for shape; it starts to read as a tic by the third use.

## Slop triage

- **opener-run (5): [P12] "it" ×3, [P101] "every" ×3, [P121] "all" ×3, [P173] "floors" ×3, [P225] "pickled" ×3.** The claim "deliberate repetition" is **correct**: the profile makes repetition-as-structure explicit ("repeat a phrase 3-4× deadpan, then invert"), and each of these does invert ([P13], [P125], [P227]). Individually: acceptable in this voice. **Collectively: a real defect** — five instances of the *same* device with the same shape is a formula, not structure. Do not change the device; change the *uniformity*.
- **negation-reversal (1): [P85] "It is not a word. It is a fragment."** — not slop. It is an in-character correction in the profile's approved belief-fixing register, and it is exactly the "wrong-then-right" shape the outline asks for. Acceptable.
- Density metrics (em-dash 0, triplet 2.6, ly-adverb 6.8) are all comfortably inside limits and match the reference's punctuation discipline. No other findings.

## Best passages (keep candidates)

- [P23] "It is a beige box with opinions…" — the only real register whiplash; mock-formal beside the mundane.
- [P217] "Not the same, but flatter. And the…" — concrete, escalating, and teaching (temperature) in one image.
- [P225] "It's more random. Pickled egg. Pickled…" — escalation + structured repetition that lands.
- [P243] "It's not smarter. It's stranger. You…" — the model correction: taut, in-character, no lecture.
- [P309] "Numbers only. It never had the word…" — a callback that teaches C1 again, differently.

## Notes for the writer

1. **Cutaways are procedural, not absurd (S2 [P44]-[P54], S4, S6).** The profile asks for escalation "one notch past plausible"; these run as literal walkthroughs, so the joke never arrives. Direction: give each miniature a beat where the procedure tips into absurdity — [P217]'s pickled egg is the template. Where: S2, S4, S6.
2. **Vary the cutaway frame.** Five of six miniatures are the same bored functionary at a station. Direction: swap at least one for an invented-format frame (a fake broadcast, ad, or "we now return to…") — the profile's cutaway is an artefact, not always a workplace.
3. **Use at least one named opener formula.** Every cut launches on a bare assertion. Direction: seed one attested set-up button ("Remember when…", "This is just like…", "We now return to…") so the hard cut is framed as well as legible.
4. **Stop the corrections lecturing ([P89], [P135], [P187]).** [P135] is the clearest case — "It added up percentages, and everything changes when you change the start" is mechanism narration in a character's mouth, the profile's named worst failure mode. Direction: keep the fix at belief-level in ≤2 short utterances; let the *event* carry the mechanism, as [P243] and [P248] already do.
5. **Restore the corpus's filler diction.** "well" and "yeah" are the reference's #2/#4 content words and appear zero times in 2,640 words. Direction: seed back-channels ("yeah", "well", "right", "look") into the family scenes, which currently run on content words only.
6. **Let the crude register show.** The profile favours crude vocabulary colliding with mock-formal; the draft has almost none, and Stewie gets two lines. Direction: give Stewie one grandiosity-curdling-into-tantrum beat and let the family's cruder register surface, so the whiplash is audible rather than only implied.
7. **Differentiate voices by sentence shape, not just function.** Almost every speaker shares the "X, and Y, and Z" coordination and the triple-repeat. Direction: give Peter assertions, Brian flat queries, Lois consequence-clauses as *distinct syntax*, so they don't all sound like the clerks.
8. **Vary the repetition templates.** [P12], [P101], [P121], [P173], [P225] are the same `X. X. X.` device five times. Direction: keep repetition-as-structure but change its shape — doubling, escalation, a word echoed back as a question — as the show does.
9. **Tighten S2 to one concept.** The ticket-swap/sticker beat ([P58]-[P71]) enacts C6 inside the C1 cutaway. Direction: per the one-concept rule, either reduce C6 to a single image or promote it to its own short block.
10. **Raise the accusation questions.** Questions run -34% vs reference and are mostly procedural. Direction: convert some flat queries into accusation-shaped questions ("Are you kidding…"), which the profile marks as the show's default.
11. **Give [P192]-[P197] personality.** Peter's "new plan / I make it creative" run restates rather than escalates. Direction: let his certainty outrun sense in a way that adds a beat, not a repetition.
