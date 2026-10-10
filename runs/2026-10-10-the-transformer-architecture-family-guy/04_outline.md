# Outline

Working title: **The Answer Box**
POV / tense / narrative distance: **No narrator, no interiority.** POV is not available (profile: "no narrator, therefore no POV"). Present tense, first person, direct address, zero distance; who is speaking is inferred from voice, with sparse delivery tags `(sighs)` / `(deadpan)` as the only stage direction. Family voices must stay distinct (Peter confident-wrong; Lois the doubt/consequence register; Brian the dry correction; Stewie ornate→tantrum; Chris literal; Meg dismissed). Interior stock bit-players get a separate deadpan register (bored clerk, matchmaker, editor) and are **never** tagged as family.
Target length: **~2,540 words**, within 2,500 ±15% (2,125–2,875), split per scene below.
Form: **prose with cutaway beats**; every hard cut is a line containing only `* * *`.

**Scene granularity (note for the writer and reviewers).** Scene = one `* * *` block. The odd-numbered scenes (S1, S3, S5, S7, S9, S11, S13) are **one continuous dinner-table A-plot** chopped by hard cuts; they should read as a single escalating conversation. The even-numbered scenes (S2, S4, S6, S8, S10, S12) are the **cutaways — the only place the mechanism appears**, each a self-contained miniature workplace with its own beginning–punch shape. This is more blocks than the role's default 3–6 because the approved form *is* the cutaway beat; each block is short (130–260 words).

**Wager ledger (pinned before drafting — fix 9).** The bet is the spine, and **every cutaway must move it**, or the cutaway is cut.
- **Stake set (S1):** Peter bets the good chair (the one by the TV) that the box can finish his sentence. His ladder as he loses ground: good chair → the remote for a week → he does the dishes → Meg gets the good chair. The family's side: if it fails, they keep the chair and Peter shuts up about it.
- **Defect → odds move:** S2/C1 mangled long word → Peter loses round 1 → the remote joins the stake. S4/C2 his "it knows where I'm going" is exposed when the early word is swapped → the dishes join. S6/C3 Chris's "it kept our sentences" is corrected → the box's next word is bland/wrong → stake at its highest. S8/C4 the dial is cranked and the answer gets *stranger* → Peter loses the remote outright. S10/C5 Peter forces the clerks single-file, the box jams and times out → Meg takes the chair. S12/C4 callback: the machine re-asks and the final word settles the bet (won on a high-probability draw, not knowledge), then the button undercuts.
- **Rule:** a tableau that teaches nothing, or teaches two things, is cut (profile rule 8).

---

## Scene 1 — Table: the truck box and the wager (~200 words)
- Carries: no MUST concept (spine + ledger; plants M1 in Peter's mouth).
- Teaches: none — sets stakes only.
- Misconception staged: **M1** planted — Peter's sales line is that the box "knows" words; it "just knows stuff." Not yet corrected.
- Beats:
  - Cold open mid-argument: Peter hauls in a beige box bought "off a guy in a truck"; Brian is already doubting it.
  - Peter claims it finishes any sentence and "knows the word"; Brian asks him to prove it; the wager forms around the good chair.
  - Peter says one word from the start of a sentence "steers" the whole thing — the set-up line for the C1 cutaway.
  - Button: a flat dismissal of Meg; cut away.
- Style notes: open mid-conversation; ping-pong, most utterances ≤8 words; a phrase repeated 3× deadpan ("it knows. It knows. It knows.") then punctured; questions as accusations ("Are you kidding?").
- Must not: let anyone explain the box; no interiority; do not yet correct M1.

`* * *`

## Scene 2 — CUTAWAY: the slicer and the number-cards (~240 words) — **C1**
- Carries: **C1** tokens→embeddings (primary); **C6** position is carried as a folded tail beat (**not** a second cutaway — no extra `* * *`).
- Teaches: through a bored clerk's procedure, not explanation — a conveyor slicer chops a long word into odd sub-word chunks, stamps a numbered ticket per chunk, and the clerk pulls one laminated card per ticket and holds it up.
- Misconception staged: **M1/I5** — a viewer may read the card as the word's meaning; the clerk's deadpan blocks it.
- Beats:
  - Peter's sentence runs down the slicer and a long word comes out in chunks; each chunk gets a numbered ticket.
  - The clerk pulls a laminated card per ticket; the card shows **numbers only**; a second, identical ticket pulls the identical card (flat beat: "same ticket, same card").
  - The clerk cannot read the ticket it answers — holds the card up to the ticket, shrugs, files nothing (registers the anti-meaning beat without saying it).
  - **C6 folded beat:** a ticket has no position tag; the clerk swaps two tickets in the tray and the reading does not change; a sticker machine slaps a coloured numbered sticker on each ticket, and the same swap now flips the reading.
  - Button: the clerk deadpans a non-answer; hard cut.
- Style notes: stock bit-player register — flat, procedural, no understanding; register whiplash can live here (mock-formal deadpan beside crude); short beats, one repetition then inversion.
- Must not: give the card a meaning or the clerk comprehension (I5); let the C6 beat grow its own cutaway or run past ~3 short beats (fix 7); imply a fact was fetched (I1).

`* * *`

## Scene 3 — Table: the mangled word and the first correction (~150 words)
- Carries: **M1** correction point; set-up for C2.
- Teaches: none directly — the **event** (a wrong next word) is the correction.
- Misconception staged/corrected: **M1** — held by Peter ("see? it looked up the word"); corrected by Brian in **≤2 short utterances** ("It didn't look up anything. Same ticket, same card."). Then stop.
- Beats:
  - The box spits a mangled next word ("unbeliev-" something); Peter is triumphant anyway.
  - Peter claims it "looked up" the word; Brian's one-two correction (belief-level, not mechanism-level).
  - Peter resets with a sentence where a word at the very start matters; set-up line for the C2 cutaway.
  - Ledger: the mangled word costs Peter round 1 — the remote joins the stake.
- Style notes: correction is two bullets of dialogue, no lecture; Brian dry, Peter loud; end on the set-up line, then cut.
- Must not: let Brian name softmax, vectors, or an equation (fix 8 defect); let the correction run past two beats.

`* * *`

## Scene 4 — CUTAWAY: the speed-dating floor (~260 words) — **C2**
- Carries: **C2** self-attention (Q/K/V, scaled dot-product, softmax).
- Teaches: through the matchmaker's **procedure**, never a preference — every token holds a wanted card (query) and an offering card (key); every wanted card is scored against every offering card; each score is stamped "÷√64"; the stamps become a percentage split that must total 100% (softmax); each token leaves with a blended drink (value).
- Misconception staged/corrected: **M2** — the floor *looks* like the matchmaker deciding what matters; the correction is an **on-stage event**, not a line: mid-cutaway, the A-plot sentence's early word is swapped (echoed into the floor), and every percentage on all the cards changes at once. Nobody flinched; no master list exists.
- Beats:
  - The floor is laid out: wanted cards (query) on one side, offering cards (key) on the other; a bored matchmaker reads the rule off a card ("every wanted card against every offering card") — procedure, not judgement.
  - Scores come back; the matchmaker stamps "÷√64" on each; the percentages are forced to total 100%; each token's drink is mixed in exactly those percentages.
  - **The anti-M2 proof:** a word at the start of the sentence is swapped upstairs and every percentage on the floor rearranges — same room, different cast, different weights.
  - Button: the matchmaker is asked to "just tell us who matters" and flatly refuses; hard cut.
- Style notes: deadpan procedural voice; one repetition then inversion ("every card. Every card. Every card."); no semicolons/em dashes; the swap is shown as an event, never narrated.
- Must not: give the matchmaker a preference or a "decides what matters" line (fix 1, M2); imply any fact is fetched from a stored table (I1); let the drinking/blend gag bury the 100% beat.

`* * *`

## Scene 5 — Table: the swapped word and the second correction (~150 words)
- Carries: **M2** correction point; set-up for C3.
- Teaches: none directly — the **consequence** (output shifts with an early word) corrects.
- Misconception staged/corrected: **M2** — held by Peter ("so it knows where I'm going, it's paying attention like a person"); corrected by **Lois** in ≤2 short utterances ("Nobody's deciding. Watch." / "Change the start and it changes everything."). Then stop.
- Beats:
  - The box's next word changes when Peter changes the first word of his sentence; Peter reads this as the box "understanding" his intent.
  - Lois's two-beat correction, then Peter immediately over-asserts and loses ground (ledger: the dishes join the stake).
  - Peter demands a "better" answer and tells the box to "think harder"; set-up line for the C3 cutaway.
- Style notes: Lois = voice of doubt/consequence, ignored; Peter's certainty outruns sense; questions as accusations; end on the set-up.
- Must not: let Lois explain attention; let the scene become a demonstration narrated aloud (the swap already happened in S4).

`* * *`

## Scene 6 — CUTAWAY: the six-floor office tower (~260 words) — **C3**
- Carries: **C3** the transformer block and the stack.
- Teaches: through events — a document is passed up six identical floors; each floor (a) re-tosses the whole pile together (attention mixes across tokens), (b) each worker quietly fixes **only their own page** (feed-forward is per-position, no mixing), (c) the original is **added back on top** of the changed page (residual = add, not keep), (d) the binder is smoothed (normalisation); six floors, each a little more finished.
- Misconception staged/corrected: **M3** — Chris's later belief that the tower is a library; corrected here by a worker who tries to file the document and is told flatly **there is no cabinet**; the residual beat is staged as pouring the original *down onto* the page, never "keeping a copy."
- Beats:
  - The document reaches floor one; the pile is tossed together so every page touches every other (across-token mixing).
  - Each worker edits only their own page and will not touch a neighbour's (per-position, I6).
  - A worker tries to file the page in a cabinet and is told there is no cabinet; nothing is stored (M3/I7).
  - The original page is added back on top and the binder smoothed; the process repeats up six floors, no recipe written down (depth, not memory).
  - Button: a worker deadpans that it is "more finished, not more filed"; hard cut.
- Style notes: stock bit-player register, flat and procedural; repetition as structure ("floors. Floors. Floors.") then inversion; no softness.
- Must not: imply a library/archive (M3, I7); imply a worker mixes pages (I6); let "added back on top" read as "the old version was kept" (fix 2); imply stacking adds a sentence store.

`* * *`

## Scene 7 — Table: the third correction (~150 words)
- Carries: **M3** correction point; set-up for C4.
- Teaches: none directly — the box's bland/wrong next word plus Brian's two beats correct.
- Misconception staged/corrected: **M3** — held by **Chris** ("so it kept our old sentences upstairs, from before"); corrected by **Brian** in ≤2 short utterances ("Nothing's filed. It's remixed every floor."). Then stop.
- Beats:
  - The box's next word is wrong and boring; Chris reasons it must have "kept our old sentences."
  - Brian's two-beat belief-correction; Peter, unbothered, reaches for a dial labelled "creativity" — set-up line for the C4 cutaway.
  - Ledger: the bland word pushes the stake to its highest so far.
- Style notes: Chris sweet, literal; Brian dry; Peter's non-sequitur as logic; end on the dial.
- Must not: let Brian describe residual/normalisation mechanics; run the correction past two beats.

`* * *`

## Scene 8 — CUTAWAY: the vending machine (~260 words) — **C4**
- Carries: **C4** next-token prediction and sampling.
- Teaches: through events — a vending machine shows a **bar chart of chances** for every snack in the building (one bar per vocabulary token), rolls a **weighted die** (weighted by the bars), drops the pick into the tray, then **asks itself again with the pick added** (append-and-repeat); the "creativity" dial **flattens** the chart.
- Misconception staged/corrected: **M4** — Peter cranks the dial expecting a *truer* answer; the chart visibly flattens and more mass moves onto the **pickled-egg** bar; the pick gets stranger, not better. **M5** — Peter says he will "just tell it the whole plan"; the machine asks again **mid-sentence**, puncturing the idea of a plan.
- Beats:
  - The machine shows the bars; it does not "know" what Peter wants — it rolls the weighted die.
  - It drops a pick, then immediately re-asks with the pick appended (loop shown once, cleanly).
  - Peter cranks "creativity"; the bars flatten; the pickled-egg bar gains mass; it coughs out a strange pick (the error light is Peter's belief, not the machine's function — M4).
  - Peter starts to state his "whole plan"; the machine re-asks halfway through his sentence (M5 punctured).
  - Button: a flat line from the machine's speaker; hard cut.
- Style notes: deadpan machine voice (delivery tags sparingly); one repetition then inversion; keep the dice/chart concrete; no equation.
- Must not: show a higher dial earning a *better* answer (fix 4, M4); show the machine "deciding on its answer" before emitting (fix 5, M5); imply a lookup (M1); let the pick be "read off" rather than drawn (I2).

`* * *`

## Scene 9 — Table: from stranger to plan-less (~160 words)
- Carries: **M4** and **M5** correction points; set-up for C5.
- Teaches: none directly — the result and Lois's two beats correct.
- Misconception staged/corrected: **M4** — corrected by the **result** (the wrong pick costs Peter ground) and **Lois** in ≤2 short utterances ("It's not smarter. It's stranger."). **M5** — corrected by the machine's mid-sentence re-ask, restated by **Brian** in ≤2 beats ("It doesn't plan. It picks one and asks again."). Then stop.
- Beats:
  - The strange pick is wrong; Peter loses the remote outright (ledger).
  - Lois's M4 two-beat correction; Brian's M5 two-beat correction; Peter ignores both.
  - Peter bellows at the box to "do it one at a time" — set-up line for the C5 cutaway.
- Style notes: two short corrections, back to back, no lectures; Peter shouts; end on his order; cut.
- Must not: let either correction name logits or temperature maths; let corrections run long enough to become narration (fix 8).

`* * *`

## Scene 10 — CUTAWAY: the eight clerks (~200 words) — **C5**
- Carries: **C5** multi-head attention.
- Teaches: through events — **eight identical clerks**, each in differently coloured glasses, receive the **same** cards **at the same instant** and announce a different "who-matters" ranking simultaneously; a stern editor staples the eight lists **side by side** (concatenation) and merges them once.
- Misconception staged/corrected: **M5-adjacent / I4** — the clerks could read as a sequence; Peter's voice from the box's speaker **forces them single-file**, and the whole thing jams (queue, stutter, error). Parallel works; chained does not.
- Beats:
  - Eight clones, same cards, eight rankings arrive at once; no clerk feeds the next.
  - The editor staples the lists side by side and merges them once.
  - Peter bellows "one at a time!"; the clones line up; the line jams and the box stalls (ledger: the timeout costs Peter the good chair; Meg is told she can have it).
  - Button: a flat deadpan from the editor; hard cut.
- Style notes: deadpan bit-players; repetition then inversion; keep the eight simultaneous, never sequential.
- Must not: show a head feeding the next head (I4, fix 6); let the cutaway become a second concept or exceed its one job.

`* * *`

## Scene 11 — Table: the final stakes (~140 words)
- Carries: no MUST concept (spine).
- Teaches: none.
- Misconception staged: none new; the family's confidence that the box will fail is now near total.
- Beats:
  - The box has stalled; Peter's chair is as good as Meg's; the family smells blood.
  - Peter makes one last attempt — the sentence must be finished to settle the bet; the family names what is on the line.
  - Set-up line: Peter says the box will "finish it, all by itself"; hard cut to the callback.
- Style notes: escalate; short beats; a phrase repeated then inverted; no resolution yet.
- Must not: resolve the bet here; let anyone explain the mechanism.

`* * *`

## Scene 12 — CALLBACK CUTAWAY: the machine asks again (~240 words) — **C4 (callback) + C1 callback beat**
- Carries: **C4** (primary callback job); **C1** lands as a one-beat callback image, not a second cutaway.
- Teaches: through events — the **vending machine returns and lands differently**: the family (and reader) now watch it as a chance distribution, not a guru. It shows the bars, rolls the die, drops the pick, and **re-asks after the appended pick**, looping until the sentence is finished. This is the **event that settles the bet** — the sentence is completed by the loop, never by the box "deciding on its answer" first.
- Misconception staged/corrected: **M5** (residual) — the loop, shown again, is the proof there was never a plan. **M1** (residual) — the **C1 callback beat**: as the appended word goes back down the line, the slicer clerk flashes past holding the same card ("same ticket, same card"), landing differently now because everyone knows the card means nothing.
- Beats:
  - The bars appear; the die rolls; the pick drops; the machine re-asks with the pick added — repeated until the last word.
  - **C1 callback beat (one image, one line):** the appended token goes back down the slicer line and the clerk holds up the same card.
  - The final word lands; the sentence is finished; the bet is settled by the loop (won on a high-probability draw — luck of the distribution, not knowledge).
  - Button: the machine asks one more time, into silence.
- Style notes: deadpan; the callback must be visibly *different* from S8 — the same machine read correctly, calm instead of cranked; callbacks land on shape change, not a repeated joke.
- Must not: let the box "decide" the sentence first (fix 5); turn the C1 callback beat into a full second cutaway (one-concept rule); imply the win proves the box "knew" (M1).

`* * *`

## Scene 13 — Table: the button (~130 words)
- Carries: no MUST concept (button only).
- Teaches: none — the sincere beat is punctured, as the profile requires.
- Misconception staged/corrected: **M1** given one last laugh — a briefly sincere "maybe it understands us" is undercut by one more wrong word.
- Beats:
  - Peter wins the bet and, for one beat, goes sincere ("it gets us, Lois").
  - The box appends one more word — wrong, and mildly insulting; the family reacts; Meg starts to say something and is cut off.
  - Final flat line; cut to black.
- Style notes: no earned sentiment — the warmth is a set-up for the puncture (profile); close on the button, not resolution.
- Must not: end on a moral or a stated lesson; let the sincere beat survive un-punctured.

---

## Coverage matrix

Every MUST concept has at least one scene where it is **shown happening**, not named.

| Concept | Priority | Scene(s) | Dramatized via (event / consequence / dialogue / image) |
|---|---|---|---|
| **C1** Tokens → embeddings | MUST | **S2** (full cutaway); **S12** (callback beat) | A slicer chops a long word into odd sub-word chunks; each chunk gets a numbered ticket; a bored clerk pulls the same laminated **numbers-only** card per identical ticket and cannot read the ticket it answers; no card holds a meaning or a fact. Callback: the same card flashes past and now reads as "numbers, not meaning." |
| **C6** Position (folded) | SHOULD (folded, not a cutaway) | **S2** tail beat only | Tickets carry no position tag, so swapping two changes nothing; a sticker machine slaps coloured numbered stickers on, and the same swap flips the reading. |
| **C2** Self-attention (Q/K/V · softmax) | MUST | **S4** | Speed-dating floor: every wanted card (query) is scored against every offering card (key); each score stamped "÷√64"; the row becomes a percentage split that must total 100% (softmax); each token leaves with a blended drink (value). The cast-swap event changes every percentage at once — the weights come from the current input, not a list. |
| **C3** The block and the stack | MUST | **S6** | Six-floor office: each floor re-tosses the whole pile (attention mixes tokens), each worker fixes only their own page (feed-forward per-position), the original is added back on top (residual add), the binder is smoothed (normalisation); six floors refine, and a worker told there is **no cabinet** shows nothing is stored. |
| **C4** Next-token prediction and sampling | MUST | **S8** (full cutaway); **S12** (callback) | Vending machine: a bar chart of chances for every snack; a weighted die instead of "knowing"; a pick drops and the machine **re-asks with the pick added**; the creativity dial **flattens** the chart and the pick turns stranger. Callback: the loop runs to the last word and settles the bet. |
| **C5** Multi-head attention | SHOULD | **S10** | Eight identical clerks, different glasses, receive the same cards at the same instant and announce eight rankings simultaneously; the editor staples the lists **side by side**; forcing them single-file jams the box. |

**MUST coverage: 4 / 4** (C1, C2, C3, C4 each shown happening). SHOULD: C5 shown (S10); C6 folded as a beat (S2), never a cutaway.

## Misconception defeat matrix

| M# | Belief | Held by | Staged in | Defeated by (event / ≤2-utterance correction) |
|---|---|---|---|---|
| **M1** | It looks things up / "knows" facts | Peter (S1, S3) | S2 (card looks like a meaning), S3 | S3 Brian, ≤2 beats: "It didn't look up anything. Same ticket, same card." Then S4 shows weights recomputed from the input. |
| **M2** | Attention = understanding / deliberate focus | Peter (S4) | S4 (matchmaker looks like a decider) | S4 **event**: swap one early word and every percentage on the floor changes; S5 Lois, ≤2 beats: "Nobody's deciding." |
| **M3** | It stores whole sentences and retrieves them | Chris (S6) | S6 (tower looks like a library) | S6 a worker is told flatly **there is no cabinet**; S7 Brian, ≤2 beats: "Nothing's filed. It's remixed every floor." |
| **M4** | Temperature is a free creativity dial | Peter (S8) | S8 (the dial) | S8 **event**: the chart flattens, pickled-egg mass rises, the pick is stranger; the wrong pick costs Peter ground; S9 Lois, ≤2 beats: "It's not smarter. It's stranger." |
| **M5** | It plans the whole sentence first | Peter (S8/S9) | S8 ("tell it the whole plan") | S8/S12 **event**: the machine re-asks **after every appended pick**, including mid-sentence and in the callback; S9 Brian, ≤2 beats: "It doesn't plan. It picks one and asks again." |

## Invariants watchlist

| Invariant | Scenes where it is at risk | How to stay safe |
|---|---|---|
| **I1** weights from the current input, nothing fetched | S4 (matchmaker could look like a lookup) | Matchmaker narrates a **procedure**, never a preference; the cast-swap event is the proof; no master list anywhere; never "finds"/"pulls up." |
| **I2** output is a distribution; the token is sampled | S8, S12 (machine could look like it "decides") | Keep the bar chart and the weighted die on screen; the machine re-asks rather than decrees; no "knows what Peter wants." |
| **I3** order-blind without position | S2 (folded C6 beat) | Show the swap changing **nothing** before the stickers, then the same swap flipping the reading after; keep it a beat, no `* * *`. |
| **I4** heads are parallel, concatenated | S10 | Eight rankings arrive **simultaneously**, stapled side by side; the jam comes only from Peter forcing a queue; no head feeds the next. |
| **I5** embedding = numbers, not a definition | S2 | Card is numbers only; clerk cannot read the ticket; "same ticket, same card"; no card, file or sentence holds meaning. |
| **I6** feed-forward is per-position | S6 | Each worker fixes only their own page and refuses a neighbour's; mixing happens only in the re-toss. |
| **I7** residual = add, not store | S6 | Stage the original being **poured back on top**, not "kept"; the no-cabinet beat kills the memory reading. |
| **I8** temperature reshapes the same distribution | S8, S12 | The dial flattens the existing chart; low dial ≈ the top bar; no scene shows a higher dial earning a *better* answer. |

## Ending

What the reader should be able to predict or do afterwards, with no stated moral:
- Predict that changing an **early word** changes the next-word chances, because the weights are computed fresh from the current input (Q2, Q5).
- Explain why the same prompt can give two answers, and why a low dial gives the same answer twice — **without** claiming low dial = more true (Q7, I8).
- Say that no fact store exists: answers come from learned weights plus a distribution that is sampled (Q8, M1).
- Say that "attention" is a mechanical weighted average, not comprehension (Q9, M2).
- Say that the block repeats to refine and **stores nothing** (Q3, M3, I6/I7).
- Say that the model **emits one token, appends it, and re-runs** — there was never a plan (Q4, M5).
- Button: the one sincere "it understands us" beat is punctured by one more wrong word, so the last impression is the mechanism, not a lesson.
