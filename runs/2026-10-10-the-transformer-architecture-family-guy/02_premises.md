# Premises — the transformer architecture, in the style of Family Guy

Role: planner (premises mode) · Run: `2026-10-10-the-transformer-architecture-family-guy` · Date: 2026-10-10.
Read: `brief.md`, `01_spec.md`, `01_questions.md`, `05_style_profile.md`, `05_style_evidence.md`, `plans/family-guy-transformer.md` §6/§9/§12. No Pivot log entry; no `plans_archive/` constraint.

**The run-specific requirement this file must satisfy:** the three premises differ in **cutaway strategy** — *how the cutaways are organised against the concepts* — not merely in setting or characters. Family Guy's teaching engine here is: **a cutaway IS one piece of the transformer, and the family's reaction on the cut-back corrects the oversimplification the cutaway just made** (profile §"Cutaway and running-gag grammar", rule 6). So the axis that separates these premises is the *structure of the cutaway sequence*.

**Two axes, and how each premise sits on them.**

| | Cutaway strategy (the separating axis) | Kind (the planner's spread) |
|---|---|---|
| **A** | One continuous A-plot; cutaways are the **only** place the mechanism appears, and each cutaway is *consequence-linked* — its defect shows up as a wrong next word back in the A-plot, and the family diagnoses it. | **Literal, in-universe:** the family really owns the machine; the cutaways are its literal internals. |
| **B** | A **retelling loop**: a spoken frame ("remember when…", "this is just like…") launches an analogical cutaway; a correction forces the *same* cutaway to be retold differently next time. The lesson is the delta between retellings. | **Analogical / allegorical:** every cutaway is an explicit stand-in, and the arc is the analogies getting fixed. |
| **C** | An **ordered relay inside a mock episode**: cold open → a main-plot problem that escalates *stage by stage* → cutaways land in forward-pass order (C1→C2→C3→C4) as different genre-framed artefacts → a callback cutaway returns changed → tag. | **Third kind:** a structural/procedural skeleton (episode form), cutaways framed as invented programmes. |

No premise is decided here — the judge picks in `03_premise_choice.md`. This file is deliberately honest about strain and coverage so the judge and fact-checker can use it.

Shared constraints (all three): no narrator (no "in other words", no lecture); no real people as characters; spoken set-up required before every cut; `* * *` is the hard cut; one concept per cutaway; the correction lives in a character's reaction, never in narration; one callback; 2,500 words ±15%.

---

## Premise A — The Answer Box

- **Cutaway strategy (signature):** a single continuous dinner-table A-plot; the mechanism is shown *only* inside the box. Each internal cutaway ends in a defect, the box's next word comes out wrong at the table, and the family's reaction names the defect. The A-plot stakes (a bet) rise with every cutaway.
- **Logline:** Peter buys a literal home "answer box" and bets the family it can finish any sentence; while the bet runs at the table, hard cuts take us *inside* the box, where the transformer actually happens as a bored workplace — and every internal mistake surfaces as a mangled next word at the table.
- **Situation / central metaphor:** no metaphor for the machine — the machine is real, in the living room, and the cutaways are its literal interior rendered as a miniature workplace comedy. The only metaphor is *register*: the internals are staffed and tedious, which is how the story keeps them mechanical rather than "thinking."

**Spine (what happens, in order, as events):**
1. Dinner. Peter introduces the box he bought off a truck. Brian doubts it. A wager is set: it has to finish Peter's sentence; loser loses the good chair / pays / gets Meg's room.
2. First attempt mangles a long word. Cutaway (inside): a butcher's slicer chops the sentence into odd sub-word tickets, a clerk tickets each and pulls a laminated number-card per ticket.
3. Cut back: the box's guess is odd; Brian corrects the family's belief that the box "looked the word up."
4. Second attempt: Peter sets up a sentence where a word from the start matters. Cutaway (inside): a speed-dating floor — every token holds a wanted card and an offering card, a matchmaker scores every pair, stamps a scaling mark, turns scores into percentages that must total 100%, and each token leaves with a blended drink.
5. Cut back: changing one word at the start changes the box's next word; the family argues about "what it's paying attention to."
6. Third attempt: Peter wants a "better" answer and demands the box "think harder." Cutaway (inside): a six-floor office tower passes the same document up; each floor re-tosses the whole pile, then each worker only fixes their own page, then re-files the original on top and smooths the binder.
7. Fourth attempt: Peter cranks the "creativity" dial. Cutaway (inside): a vending machine shows a bar chart of chances for every snack in the building, rolls a weighted die, drops the pick, and asks again with the pick added.
8. Final attempt: the sentence must be finished to settle the bet. Cutaway (inside): eight identical clerks with different glasses rank "who matters" at the same instant and an editor staples the lists side by side; Peter orders them to go one at a time and the queue jams.
9. Callback: the slicer cutaway returns, now that the family knows a ticket is not a meaning.
10. Button: a ticky sincere beat about the box "understanding them" is punctured by one more wrong word.

**Cutaway strategy — how it enacts the concepts:** the A-plot is pure stakes and reaction; the teaching is entirely inside. Because each cutaway's defect has a *consequence at the table*, the sequence can't degrade into unrelated jokes: every joke is load-bearing. Corrections are reactions to the *result*, not explanations of the machine (Brian corrects the family's belief, not the viewer).

**Mapping table:**

| Concept | Story element | Fidelity | Where it breaks |
|---|---|---|---|
| C1 tokens→embeddings | Inside: meat-slicer chops words into sub-word tickets; clerk pulls a laminated number-card per ticket | EXACT | The card is shown as a physical object; a viewer may think the card *is* the vector. Fixed by a reaction: the card has no meaning, the same ticket always draws the same card. |
| C2 self-attention (Q/K/V, scale, softmax) | Inside: speed-dating floor; wanted card / offering card; matchmaker scores all pairs, stamps "÷√64", splits 100%, blends drinks | ANALOGOUS | The matchmaker could read as a chooser (M2). Fixed because changing who is in the room changes every percentage — there is no master list. |
| C3 block and stack | Inside: six-floor office tower; attention re-tosses the pile, feed-forward fixes each worker's own page only, original re-filed on top (residual), binder smoothed (norm) | ANALOGOUS | "Floors passing a document" can imply a sentence library (M3). Fixed by a reaction: no recipe is ever written down. |
| C4 next-token + sampling | Inside: vending machine bar chart + weighted die; pick dropped and the machine re-asks with the pick added; creativity dial | EXACT | The dial gag risks teaching M4 (creativity at no cost). Fixed: turning it up yields stranger, not truer, picks. |
| C5 multi-head (SHOULD) | Inside: eight identical clerks, different glasses, simultaneous rankings, stapled side by side; Peter forces a queue and jams it | EXACT | "Eight clerks" can read as a sequence (M5-adjacent). Fixed by the jam showing parallel, not chained. |
| C6 position (folded) | Short beat only: tickets get no name-tags and order doesn't matter until coloured stickers are slapped on | ANALOGOUS | Easy to drop; the brief allows keeping C5 as the one SHOULD and folding C6 into C1/C2 (spec §1 decision #7). |

- **Concepts it can carry:** C1, C2, C3, C4 (all MUST) + **C5** as the one SHOULD; **C6 folded** into the C1/C2 beats as name-tags. Drops the context-window/KV-cache optional.
- **Cannot carry:** training/backprop, RLHF, encoder–decoder, retrieval/tools, long-context — correctly out of scope (spec §1).
- **Misconceptions it risks teaching by accident:** M3 and M4 are the live ones (a "thinking box" and a "creativity dial" are the natural shapes here). M1 is deliberately staged and corrected.

**Wrong-then-corrected beats (M1–M5 become scenes, not disclaimers):**
- **M1** (looks things up / knows facts) — held by *Peter* at the slicer: the clerk pulls a card and Peter assumes the card holds the word's meaning. Corrected on cut-back by *Brian*: the same ticket always pulls the same card and the card is only numbers; the box never looks anything up.
- **M2** (attention = understanding) — held by *Peter* at the speed-dating floor ("the matchmaker decides what matters"). Corrected by *Lois*: swap anyone in the room and the percentages all change; nobody is deciding.
- **M3** (stores whole sentences) — held by *Chris* at the office tower ("so it kept our old sentences upstairs"). Corrected by *Brian*: nothing is filed as text; the pile is re-mixed each floor.
- **M4** (free creativity dial) — held by *Peter* at the vending machine: he turns the dial up expecting better answers. Corrected by the *result* (pickled eggs) and *Lois*: it only makes stranger picks likelier, not truer.
- **M5** (plans the whole sentence) — held by *Peter* at the table ("tell it the whole plan then"), corrected inside the vending machine, which asks again after every single pick. Callback: the machine re-asks after the callback pick.

**Literalness anchors:** (1) inside the box, no worker ever *understands* the meaning — a clerk can state the rule ("same ticket, same card") but can't read what the ticket says; (2) the percentages change when the cast changes, which is the anti-M2 proof; (3) the vending machine re-asks with the appended pick, the anti-plan proof.

**Style fit:** helps — the A-plot is pure ping-pong dialogue and stakes, and every `* * *` is a hard cut, exactly the show's grammar. The internal workplaces give the cutaways their own tiny beginning–punch shape (profile §cutaway step 4). Fights — the internal scenes have no family voices until the cut-back; they need a stock bit-player register (bored clerk, matchmaker, editor) and must not acquire a narrator. Register whiplash (crude verse next to mock-formal) can live in the clerk's deadpan.

**Cliché risk (and how it collapses):**
- *Into unconnected jokes:* if the bet doesn't escalate and each internal defect doesn't change the odds, the internals become random-cutaway syndrome. Guardrail: every cutaway moves the wager.
- *Into a lecture:* if Brian's corrections become explanations of the mechanism, a narrator has snuck into Brian's mouth (the worst failure mode in the profile). Guardrail: he corrects a *belief*, in one or two beats, and the next attempt shows it.
- *Lazy version:* "the family finds a magic box that says funny wrong things" with pretty cutaways and no wager.

---

## Premise B — Remember When I Explained It

- **Cutaway strategy (signature):** a **retelling loop**. Peter is telling a story out loud to a family that keeps interrupting; every "remember when…" / "this is just like…" opens an analogical cutaway. Each analogy is wrong in exactly one way (M1–M5); on the cut-back a family member corrects it; Peter then *retells the same moment* in the next cycle, and the cutaway returns changed. The teaching is the visible difference between the wrong retelling and the fixed one.
- **Logline:** Peter insists he can explain the family's machine, and holds forth at the table with a string of "remember when…" stories; each story is a wrong little analogy, each is shot down, and the story gets retold a notch closer to true until the same cutaway finally lands right.
- **Situation / central metaphor:** the whole piece is an argument Peter is losing in front of his family. The frame is *spoken* — a character talking is not a narrator (profile: characters "think aloud"; the rule bans a narration voice, not dialogue). The cutaways are his analogies, and their unreliability is the comedy.

**Spine (what happens, in order, as events):**
1. Frame open (mid-argument): Peter claims he alone understands the machine; Brian and Lois call it. The stake: if Peter's explanation survives five challenges, he gets something (the good chair / the last word / to be called smart once).
2. Cycle 1 — M3/M1: Peter's first story is a filing cabinet of every sentence the machine ever saw, reading answers back. Cutaway: a cabinet pulls a sentence verbatim. Cut back: Brian corrects — only numbers are stored, text is rebuilt each time.
3. Cycle 2 — C1: Peter retells it as a butcher's slicer. He still insists the slicer "looks up what the meat means." Cutaway: the slicer and its tickets. Cut back: Brian — tickets are ids, cards are numbers, no meaning.
4. Cycle 3 — C2: Peter retells as speed dating, and adds "the matchmaker decides what matters." Cutaway: the dating floor. Cut back: Lois — swap the cast, all percentages change; nobody decides.
5. Cycle 4 — C3: Peter retells as a relay of tables passing a dish; he drops the per-position part. Cutaway: the dinner relay. Cut back: Brian — the feed-forward never mixes the plates; only attention does.
6. Cycle 5 — C4/M4/M5: Peter retells as a vending machine, and turns up "creativity" to prove he can make it smarter. Cutaway: the vending machine. Cut back: the result and Lois — stranger, not smarter; and it never planned the sentence, it picked one token and asked again.
7. Callback: Peter tells the cabinet story one last time, now correctly — the same cutaway returns and lands differently.
8. Button: he immediately overclaims that he invented the machine and is punctured.

**Cutaway strategy — how it enacts the concepts:** the loop turns the misconception into the engine. Because the *same* cutaway is re-shot after a correction, the viewer sees exactly what changed and what didn't — that is teaching by delta, and it is impossible to mistake for a lecture, since every claim is Peter's and every fix is a character's.

**Mapping table:**

| Concept | Story element | Fidelity | Where it breaks |
|---|---|---|---|
| C1 tokens→embeddings | Retelling 1: filing cabinet of sentences (wrong) → Retelling 2: butcher's slicer + tickets + number-cards (right) | EXACT after retell | The cabinet is *deliberately* wrong (M3); risk only if the audience reads the cabinet as the true account. The retelling fixes it on screen. |
| C2 self-attention | Retelling 3: speed-dating floor, wanted/offering cards, scaling stamp, 100% split, blended drink | ANALOGOUS | The matchmaker can read as a decider; fixed by the cast-change test in the cut-back, then shown again in the callback. |
| C3 block and stack | Retelling 4: relay of dinner tables; attention mixes the pot, each guest fixes only their plate, original poured back on top, lumps smoothed | ANALOGOUS | "Guests fixing plates" can imply storage; fixed by Peter's own retelling dropping the recipe-book (no sentence store). |
| C4 next-token + sampling | Retelling 5: vending machine bar chart + weighted die, re-asks after each pick; creativity dial | EXACT | Temperature gag risks M4; deliberately staged and corrected (stranger ≠ truer). |
| C5 multi-head (SHOULD) | Short beat inside retelling 3: a row of identical matchmakers with different glasses, rankings stapled side by side | ANALOGOUS | If it becomes a second full cutaway it breaks "one concept per cutaway"; keep it a beat, not a scene. |
| C6 position (folded) | A dropped sticker in retelling 2 flips the sentence's tickets until name-tags are re-applied | ANALOGOUS | Folded; must not grow its own cutaway. |

- **Concepts it can carry:** C1, C2, C3, C4 + **C5** as a beat; **C6 folded**. Drops the optional context window.
- **Cannot carry:** same out-of-scope list; also this frame has the *least* room for C5/C6, since the retelling structure eats runtime.
- **Misconceptions it risks teaching by accident:** the whole premise is built from wrong analogies (that is the point), so the risk is the audience remembering the *funny wrong* version. Mitigation is structural: every wrong cutaway is immediately corrected on screen and at least one (the cabinet) is retold correctly in the callback.
- **Wrong-then-corrected beats (M1–M5):** all five are *scenes*, and each is the cutaway's premise rather than a disclaimer.
  - **M1** — Peter's cabinet reads facts back; corrected by Brian ("only numbers are in the weights").
  - **M2** — Peter's matchmaker "decides what matters"; corrected by the cast-swap demonstration (Lois).
  - **M3** — the cabinet of whole sentences; corrected by Brian and the callback retelling.
  - **M4** — Peter turns up creativity to get a *better* answer; corrected by the worse pick and Lois.
  - **M5** — Peter claims the machine planned the sentence; corrected by re-running the pick loop on screen.

**Literalness anchors:** (1) every retelling is spoken by Peter and challenged in dialogue, so the audience sees the *claim* fail, not just hears a right answer; (2) the callback shows the corrected cabinet — the concrete before/after is the anchor; (3) C2's cast-swap test is re-shown inside the callback.

**Style fit:** helps — this is the purest version of the show's "remember when…" and "this is just like…" set-up formulas (evidence E13–E16), and it gives repetition-as-structure a natural home: the phrase is said three or four times, then inverted, and the same cutaway recurs (profile step 7). Fights — the frame is dangerously close to a monologue, and the profile forbids slow burn and explanation. Peter must be *interrupted* constantly; the family's corrections must be the connective tissue, and the frame must never become Peter explaining correctly.

**Cliché risk (and how it collapses):**
- *Into a lecture:* if Peter starts narrating the correct mechanism, the frame *is* the banned narrator. Guardrail: Peter is never right on his own; only the interruptions carry the truth.
- *Into unconnected jokes:* if the retellings don't visibly build on each other, it's the same wrong joke five times. Guardrail: each cycle must fix exactly one thing and keep everything else.
- *Lazy version:* "Peter tells the story of a machine, badly" with cutaways that never get corrected.

---

## Premise C — The Griffin Family Answer Hour

- **Cutaway strategy (signature):** an **ordered relay inside a mock episode**. The main plot is a family scheme whose escalating problem walks the transformer pipeline in order: each complication can only be solved by the *next* stage, so the cutaways land in forward-pass order (C1→C2→C3→C4), each framed as a *different invented programme* ("We now return to…" / a fake ad / a fake courtroom / a fake game show). A cold-open cutaway seeds the theme, and a callback cutaway returns in the tag.
- **Logline:** the family tries to win a competition by fielding their machine as a contestant, and as the competition heats up they are dragged one stage deeper into how it works, until the final question can only be answered by knowing that it samples one word at a time.
- **Situation / central metaphor:** a fake episode of a fake show — cold open, main plot, tag — where the pipeline becomes a *relay race*: to get past round one you need to have solved round zero, and so on. The cutaways are genre parodies because the family smuggles pieces of the machine into different formats (an ad, a trial, a relay, a game show) to "make it presentable."

**Spine (what happens, in order, as events):**
1. Cold open (fake ad / fake bit): a gadget ad that claims "it just knows things"; the button punctures it; the family reacts and the stakes for the competition are set.
2. Round 1 — the entry is rejected for a garbled word. Cutaway framed as a fake commercial: the slicer and tickets (C1). Cut back: the family fixes the entry.
3. Round 2 — the family realise the machine's answer keeps shifting depending on an early word; a fake courtroom cutaway stages the scoring and softmax (C2). Cut back: they argue about "what it's paying attention to" and lose time.
4. Round 3 — the machine still isn't "finished" enough; a fake relay/tower cutaway stages the block and stack (C3). Cut back: a family member claims it must have memorised old answers; corrected.
5. Final question — the competition demands a sentence the machine hasn't seen. A fake game-show cutaway stages the sampler and the creativity dial (C4); Peter cranks it and blows the round.
6. Multi-head beat (C5) inside the relay: eight identical hosts give simultaneous rankings; Peter forces them single-file and jams the show.
7. Callback: the cold-open fake ad returns, now describing the machine correctly; it lands differently.
8. Tag: one last confident-wrong line, cut to black.

**Cutaway strategy — how it enacts the concepts:** the relay forces the concepts into **pipeline order**, so the coverage matrix is nearly automatic — the main-plot escalation *is* the forward pass. The genre frames keep the cutaways varied (an ad, a trial, a relay, a game show) so the piece doesn't read as one repeated analogy. The callback closes the loop the show's grammar asks for.

**Mapping table:**

| Concept | Story element | Fidelity | Where it breaks |
|---|---|---|---|
| C1 tokens→embeddings | Fake-commercial cutaway: slicer chops the entry, tickets + number-cards | EXACT | Same card-is-vector risk as A; fixed by a reaction in the main plot. |
| C2 self-attention | Fake-courtroom cutaway: the prosecution scores every word against every word, scales, splits 100%, blends | ANALOGOUS | "Courtroom decides" reads as intent (M2); fixed by the cast-change test and by the sentence shifting mid-round. |
| C3 block and stack | Fake-relay cutaway: stations pass the entry down the line; attention mixes, per-station fixes its own page, original re-added, smoothed | ANALOGOUS | Relay can imply ranked storage (M3); fixed by a reaction and by stacking = depth, not memory. |
| C4 next-token + sampling | Fake-game-show cutaway: a board of chances, a weighted wheel, one pick per turn, re-spin with the pick added; creativity dial | EXACT | Temperature risks M4; deliberately staged, corrected by result. |
| C5 multi-head (SHOULD) | Beat inside the relay: eight identical hosts rank at once; lists stapled side by side; forced queue jams | EXACT | Must stay one beat; a second cutaway breaks one-concept-per-cutaway. |
| C6 position (folded) | A name-tag mix-up in the ad cutaway that changes the sentence until stickers are re-applied | ANALOGOUS | Folded; keep to a beat. |

- **Concepts it can carry:** C1, C2, C3, C4 + **C5**; **C6 folded**. Because the relay walks the pipeline anyway, this premise has the most room for the SHOULDs and can use them as beats without squeezing the plot.
- **Cannot carry:** out-of-scope list as above; also the optional context-window is the first cut if the episode runs long.
- **Misconceptions it risks teaching by accident:** the "it just knows things" fake ad (M1) and the competitive framing ("it's brilliant") gently push toward M1/M2 if not corrected. The relay also risks implying the stages run *in sequence as separate workers* rather than the block repeating — a C3 slip toward a pipeline-of-experts, which the reactions must catch.

**Wrong-then-corrected beats (M1–M5):**
- **M1** — the cold-open ad claims it "just knows"; corrected by the C1 ad (it tickets words, it doesn't know them) and by a main-plot line.
- **M2** — the courtroom "arguments" about which word is important; corrected by the cast-change test in the main plot.
- **M3** — a family member claims the relay station has memorised old entries; corrected by a station worker's flat denial.
- **M4** — Peter cranks the creativity dial to win the final round and loses it; corrected by result and Lois.
- **M5** — a fake press-conference beat where the machine "announces its plan"; cut back and re-run the pick loop to show one token at a time.

**Literalness anchors:** (1) the machine is a real object the family is really competing with; (2) the ordered relay is walked *once as itself* in the callback, so the audience sees the true pipeline rather than only the parody frames; (3) each round's failure is a consequence of the previous round's missing stage — the relay's cause-and-effect is the anti-lecture proof.

**Style fit:** helps — the mock-episode skeleton (cold open → main plot → tag), the "We now return to…" frame (evidence E18), and the callback the plan requires are all native to the show. Different genre frames per cutaway fight the "one repeated analogy" trap the profile warns about. Fights — this is the most *constructed* premise, so it risks feeling like a syllabus with jokes bolted on; the main plot's stakes must bite at every round or it collapses into "the pages of a textbook, dressed up."

**Cliché risk (and how it collapses):**
- *Into unconnected jokes:* if each round is won the same way and the cutaways just advance a checklist, it becomes the "cutaway as a list item" trap (profile lazy-pastiche). Guardrail: each round's *failure* must cost something and force the next stage.
- *Into a lecture:* if the relay is run in order with nobody wrong, the order itself narrates the mechanism. Guardrail: someone must confidently misread each station, and the reaction must fix it.
- *Lazy version:* a mock awards-show with five themed cutaways and no stakes connecting them.

---

## Spread check (for the judge)

| | A — The Answer Box | B — Remember When I Explained It | C — The Griffin Family Answer Hour |
|---|---|---|---|
| Cutaway organisation | Single A-plot; cutaways are consequence-linked internals (only place the mechanism appears) | Retelling loop; same cutaway returns corrected (delta is the lesson) | Ordered relay; cutaways in forward-pass order, genre-framed, cold open + callback |
| Kind | Literal, in-universe | Analogical / allegorical | Structural / procedural (mock episode) |
| MUST carried | C1–C4 | C1–C4 | C1–C4 |
| SHOULD | C5 (C6 folded) | C5 as a beat (C6 folded) | C5 (C6 folded); most room for both |
| Strongest | Ties every joke to stakes; hard to lecture | Turns misconceptions into the engine; safest against a narrator | Pipeline order makes coverage automatic; best callback |
| Weakest | Internal scenes need a stock-player register; M3/M4 pressure | Frame can slide into monologue; retelling eats runtime | Can feel syllabus-y; one-concept-per-cutaway under pressure |
| If it fails, it fails by | Random-cutaway syndrome / Brian explaining | Peter narrating (banned) | Relay-as-list |

**Honesty notes.** No premise carries all of C1–C6 with zero strain; C5 and C6 are load-bearing only as one-shoulder beats, and C6 is folded in all three (per brief §"Hard constraints" and spec §1 decision #7). Premise B is the most original cutaway strategy and the most exposed to a narrator; Premise C is the safest coverage and the most at risk of a constructed lecture; Premise A is the best fit to the "one cutaway = one mechanism + reaction" engine but asks the writer to hold a wager and an interior register at once. All three keep the mechanism in events and the corrections in characters' mouths, as the profile requires.
