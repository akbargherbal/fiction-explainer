DECISION: A

# Premise choice — the transformer architecture, in the style of Family Guy

Role: premise-judge (fresh context; not the planner) · Run: `2026-10-10-the-transformer-architecture-family-guy` · Date: 2026-10-10.
Read: `brief.md`, `01_spec.md`, `02_premises.md`, `05_style_profile.md`, `05_style_evidence.md`.

## Scores (1-5, with one line of evidence each)

| Criterion | A | B | C |
|---|---|---|---|
| **Fidelity** — mapping exactness; severity of "where it breaks" | **4** — the machine is literal, so C1 and C4 are EXACT (I5, I2) and C2/C3 are analogous only in register, with each break named and fixed in-story | **3** — the true account is never shown literally; it exists only as the delta between Peter's retellings, so fidelity is carried by the audience holding the comparison | **3** — the relay form structurally implies ordered specialist stages, which the premise itself admits risks a C3 slip toward a pipeline-of-experts (I6/I7) |
| **Coverage** — MUST concepts the premise can dramatize | **4** — C1–C4 each get a full internals cutaway, C5 a full cutaway, C6 folded into the C1/C2 beats (spec §1 decision #7) | **3** — the retelling loop eats runtime (planner's own note); C5 is demoted to a beat, C6 to a sticker gag, leaving the least room for the SHOULD concepts | **5** — forward-pass order makes C1→C4 automatic and leaves the most room for C5/C6 as beats |
| **Drama** — would a reader want to read it | **5** — an escalating wager ("the good chair", Meg's room) makes every cutaway cost something at the table | **4** — losing an argument in front of your family is a strong frame, but the scene is static: a table, five interruptions | **4** — the competition has stakes, but rounds risk reading as a procedural checklist |
| **Style fit** — against the profile, including its negative space | **5** — set-up line → `* * *` → mini-scene → in-character reaction is exactly profile rule 6; the wager is pure ping-pong dialogue | **3** — the frame is one long Peter monologue, precisely the profile's "dangerously close to a monologue" and the narrator's doorway | **3** — the mock-episode skeleton (cold open → plot → tag) and "We now return to…" (E18) are native, but the built relay fights the "no slow burn" rule |
| **Freshness** — distance from the obvious / cliché version | **3** — "family buys a magic box" is familiar, but interns-as-tedious-workplace rather than a "brain" is fresh | **5** — the retelling loop is the most original cutaway organisation; the lesson-by-delta is new | **3** — mock awards/game-show + genre parodies is the well-trodden version of this show |
| **Risk** — chance of teaching a misconception (M#) by accident (5 = highest risk) | **3** — M3/M4 are the live shapes here (a "thinking box", a "creativity dial"), but both are explicitly staged and corrected | **4** — the whole engine is a wrong analogy; the risk is the audience keeping the *funny wrong* cabinet (M3/M1) after the correction scrolls past | **4** — the cold-open "it just knows" ad (M1) plus the relay's sequential stages teaching C3 as chained experts |

(Direction note for the Risk row: a **higher** number means **more** risk, so A's 3 is the best score on that row.)

## Decision

A wins on the two criteria the role says to weigh heaviest — Fidelity and Risk — and it is the only premise whose cutaway strategy *is* the run's central bet rather than a frame around it. In A the cutaway is the mechanism itself, played as a literal interior (C1 = sliced tickets and laminated number-cards, C2 = the speed-dating floor, C3 = the six-floor office, C4 = the vending machine), so the model never has to be approximated by a whole-cloth metaphor and I1/I2/I5 are dramatisable directly; the audience is shown the thing, not a likeness of it. That literalism also produces A's structural guardrail against both failure modes: every internal defect surfaces as the *next wrong word at the table*, and because the family is betting on that outcome, every joke is load-bearing and the wager's odds change each beat — so it cannot degrade into random-cutaway syndrome, while the correction lives in Brian's or Lois's reaction to the *result*, not in an explanation of the machine. B is the most original and the safest against a narrator (only characters ever claim the mechanism), but its truth is a delta the viewer must hold across a five-cycle monologue frame the profile names as the banned narrator's doorway, and it has the thinnest coverage. C has the best coverage and callback but its ordered relay stages risk asserting a false structure (I6/I7) and it is the most likely to read as a syllabus with jokes bolted on. Recommendation: **A**.

Caveat for the outline: A's M3/M4 shapes are real and must be fixed, not waved at — a "thinking box" and a "creativity dial" are exactly the two objects that teach the wrong thing if the corrections are lazy.

## Required fixes for the outline

1. **C2 / M2 (the biggest live risk).** The speed-dating matchmaker must never be given a decision voice ("decides what matters"). Protect I1 by making the *cast-swap consequence* on-stage: change one early word at the table and show a different set of percentages in the cutaway, so the anti-M2 proof is an event. The matchmaker narrates a procedure ("every wanted card against every offering card"), never a preference.
2. **C3 / M3.** The six-floor office must not imply a library. Add a worker who tries to file the document and is told flatly there is no cabinet, and render the residual as "the original is added back on top", not "the old version is kept"; I7 must be visible as add, not store.
3. **C1 / M1 + I5.** The laminated number-card must be shown as numbers only; the clerk holds it up and cannot read the ticket it answers ("same ticket, same card"), so no scene implies the card holds the word's meaning. Peter's "it looked up the word" must be corrected by Brian in **one or two beats**, as a belief-correction.
4. **C4 / M4 + I8.** The "creativity" dial must produce *stranger, not truer*: Peter cranks it, the bar chart visibly flattens (more mass on the pickled-egg token), and the wrong guess costs him ground in the wager. No scene may show a higher dial earning a better answer.
5. **C4 / M5 + I2.** The vending machine must re-ask after **every** appended pick, including inside the callback; the bet must be settled by that loop, never by the box "deciding on its answer" first. Peter's "tell it the whole plan" is the staged wrong belief, punctured by the machine asking again mid-sentence.
6. **C5 / I4.** The eight-clerk cutaway must land *parallel, not chained*: the rankings arrive simultaneously and the jam is caused by Peter forcing them single-file. No head may be shown feeding the next.
7. **C6 / I3 (folded).** Keep position to a beat, not a cutaway: tokens with no name-tags where swapping two changes nothing, then stickers applied and the same swap flips the sentence. It must not grow its own `* * *`.
8. **Narrator guard (profile: worst failure mode).** Brian's and Lois's corrections fix a *belief* in ≤2 short utterances and then stop; the *next attempt* must be what demonstrates the mechanism. If any correction runs past two beats or names an equation, treat it as a defect in review.
9. **Anti-random-cutaway guard.** Before drafting, pin the wager's ledger so each internal defect measurably changes the odds; a cutaway that does not move the bet is cut, per profile rule 8 (one concept per cutaway, and a cutaway that teaches nothing is not allowed).
10. **Interior register.** The stock bit-players (bored clerk, matchmaker, editor) need a deadpan voice distinct from the family, and none of them may *understand* the ticket, page or card. Register whiplash (crude next to mock-formal) can live in the clerk; the family voices must not flatten toward Peter's.

## Rejected

- **B — Remember When I Explained It:** lost on Risk and Style fit — the pedagogy depends on the audience retaining the *corrected* version over a deliberately funny wrong analogy, inside a monologue frame the profile flags as the banned narrator's doorway, and it has the thinnest coverage.
- **C — The Griffin Family Answer Hour:** lost on Fidelity — the ordered relay's specialist stages privately assert a false structure (that stages are sequential workers rather than one block repeated, I6/I7) and it is the most exposed to collapsing into a constructed lecture.
