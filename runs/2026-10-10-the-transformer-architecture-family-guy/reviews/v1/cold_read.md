# Cold read — v1

## Part 1 — What I think this was about

This is a *Family Guy*-flavoured story about Peter buying a beige box off a guy in a truck that "finishes your sentences," and then betting the family's good chair that it can finish one sentence. Through a run of surreal factory and office scenes — a slicing line, a tray with tickets and stickers, a bar where drinks are poured in percentages, a pile of pages being tossed and re-fixed floor by floor, and a room of bars and a weighted die — the box is revealed to never "know" any word: it turns sentences into numbered tickets (never the words), uses stickers to remember order, compares every card against every other card, scores and rescales those scores into percentages, blends them into a drink, stacks this over several floors while adding the original back on top, and finally picks one snack at a time weighted by probability until a sentence is complete.

I think the subject is the **Transformer architecture**, i.e. how a modern large language model actually generates text: tokenisation into numeric ids, position/order information added because the raw numbers are order-blind, self-attention (every token against every token) with scaled scores and a softmax over them, residual connections plus layer norm as the stack repeats, temperature sampling (the "creativity" dial flattening the probability bars), multi-head attention (the eight parallel ranking lists merged into one), and autoregressive next-token-at-a-time decoding.

What I now understand, that I did not before watching it dramatised, is why attention rescales *everything* when a single early word changes (each score is normalised against all the others), and why "creativity" makes output stranger rather than smarter (it flattens the distribution toward uniform). The story also lands the point that the box is remixing the current input only — nothing is "filed," so it has no memory of past sentences.

## Part 2 — Experience

**Where I was lost or confused.**
- Scene 2, the slicer/ticket segment [P34–P81] is the hardest stretch to map. I followed "same ticket, same card" and the swap-the-tickets test [P60–P63] vs the stickers [P64–P71] only after re-reading it twice; my first pass had no anchor for what a "card" was.
- The drinks in scene 4 [P103–P112]: "Sixty him, twenty five her, fifteen the other one" and "he's part other people" [P111] landed as a joke before I understood it was a weighted blend of values.
- The scene 10 stall [P266–P282]: I grasped that "one at a time" jams the line, but I was unsure whether the intended point was a queue/throughput thing or something about the model architecture, and it stayed slightly ambiguous.
- [P62–P63] "Same reading, so swap them back." / "Same reading again, and nothing changed at all." — I had to infer this was showing order-blindness rather than a defect.

**Where I was bored, or felt lectured.**
- The repeated "same ticket, same card" / "Next!" formula wears out by scene 3; it starts to feel like the story is drilling a phrase at me rather than showing me something.
- Scene 5 [P132–P146] reads as a rerun of scene 4's point ("nobody's deciding," everything changes when the start changes) with no new mechanic — this is where I most felt lectured, especially [P135].
- The echo-triples — "Every card. Every card. Every card." [P101], "All of them. All of them. All of them." [P121], "Floors. Floors. Floors." [P173] — feel like a teaching tic rather than dialogue, and they stack up.
- The "it knows" / "it doesn't know" back-and-forth [P82–P91, P132–P141] repeats more than it advances.

**Moments I will remember in a week.**
- "Divide every score by root sixty four." [P104] — oddly catchy and clearly load-bearing.
- The pickled egg climbing from a sliver to a slice as the dial goes up [P217–P219], and "It's more random. Pickled egg. Pickled egg. Pickled egg." [P225].
- "You turned up noise, and noise is loud." [P243].
- "It asks again into nothing. It always asks again." [P327], and the closing "Ding." [P343].
- The payoff sentence assembling itself: "The boat... is... unbelievable." [P315–P317].

**One thing I would cut.**
Scene 5 [P132–P146]. It restates the attention conclusion scene 4 already dramatised, and cutting it would tighten the middle without losing any mechanic.

## Part 3 — Quiz answers

**Q1. What the text is broken into, and what each piece becomes; what is *not* stored.**
The input is sliced on the line ("Long one coming down the line, so slice it" → "Unbeliev... / ...able." [P35–P37]), so a sentence is broken into fragments, not whole words. Each fragment becomes a ticket/card that is "numbers only" [P44–P45, P52], and the word is explicitly thrown away: "Cards are numbers, sir. Meaning is not in the building" [P73], "It never had the word. It only ever had numbers" [P310]. So what is *not* stored after this step is the word/meaning itself. Tag: **FROM THE TEXT [P35–P45, P73, P310]**.

**Q2. Where the attention scores come from; query vs keys; softmax; what weights are used for.**
The story stages attention as "wanted cards on the left, and offering cards on the right" [P97] under one rule: "every wanted card against every offering card" [P99, P205]. Each wanted/offering pairing produces a score ("Two, one, and five" [P103]); the scores are then normalised so the row "has to add up to one hundred percent" [P106], and those percentages are used to blend the values into one drink ("pour the drink in those exact percentages" [P108], "Sixty him, twenty five her, fifteen the other one" [P109]). So query = the wanted card, keys = the offering cards, softmax = the forced 100% row, and the weights = the drink proportions used to merge the offerings. **Caveat:** the story shows the scores coming from cards matching cards inside the building [P125]; it does *not* say those score numbers are produced by learned weight matrices/projections — that detail is **PRIOR KNOWLEDGE**. Tag: mechanism **FROM THE TEXT [P97–P109, P125]**; learned-projection origin **PRIOR KNOWLEDGE**.

**Q3. The two things a block does; residual + norm; stacking.**
The block/floor does attention ("toss the whole pile together, so every page touches every page" [P148], repeated per floor [P169–P171]) and per-page fixing ("fix your page, and only your page" [P150]). Around it, the original is added back onto the change — "Pour the original back on top... It goes on top of the change" [P162–P166] — which reads as the residual connection — and there is a smoothing step, "smooth the binder, and take the lumps out" [P167], which reads as normalisation. Stacking just repeats the whole floor: "Every floor, and every page, every time" [P171], "Six, and then it's finished" [P174]. **Caveat:** I am mapping "fix your page" to the feed-forward sub-layer on inference, not because the story names two sub-layers — it doesn't clearly separate them. Tag: residual/norm/repeat **FROM THE TEXT [P148, P162–P174]**; "the two things are attention + feed-forward" **PRIOR KNOWLEDGE**.

**Q4. From the final vector to the next word, in order.**
The story ends with the model's output stage as bars and a die: "One bar for every snack in the building" [P200], then "Roll the die. Weighted by the bars" [P203–P204], "dropped into the tray" [P207], then "ask again, with mat in the tray" [P208], and it "always asks again. One snack at a time, every single time" [P211, P306]. So: the model turns its final state into one bar/probability per possible next token, samples one proportionally ("Roll the die. Weighted"), appends that token, and repeats the whole loop until the sentence ends — which we then watch assemble token by token: "The boat... is... unbelievable." [P315–P317]. Tag: **FROM THE TEXT [P200–P211, P299–P317]**. (The intermediate "final vector → logits → softmax" naming is mine; the story shows the bars directly.) The logits-to-bars step is inferable **FROM THE TEXT [P200]**, the naming **PRIOR KNOWLEDGE**.

**Q5. How a distant early word still shifts the next-word chances.**
The story's point is exactly this: "And the first word never even met these cards" [P122], answered by "That first word meets every card. That's the whole job" [P123]. Because every wanted card is scored against every offering card [P99], changing one early word rescores everything — "Every percentage on every card, all at once" [P119], "everything changes when you change the start" [P135]. So the distant word changes the next word by participating in every attention comparison, not by being looked up from a table. Tag: **FROM THE TEXT [P99, P119, P122–P125, P135]**.

**Q6. Context window smaller than the prompt: how the next-word distribution changes, and why.**
The story's model keeps nothing once the current input changes — "There is no last list. There's the score right now" [P129], "There is no cabinet" [P157], "There is no last week. There's this document" [P161], "nothing's filed" [P187]. So if the earliest words are cut off, their attention contributions are simply gone, and the next-word distribution shifts as if those words were never there (the "everything changes when you change the start" logic [P135] now applies to removing rather than changing a word). Tag: premise **FROM THE TEXT [P129, P157, P161, P187]**; the specific truncation prediction itself **PRIOR KNOWLEDGE** (derived from that premise).

**Q7. Same prompt twice differs; low temperature gives the same answer; is low-temp more correct?**
The dice are weighted by the bars and "roll" each turn [P203–P204, P299–P301], which is the sampling randomness — same prompt, different rolls, different answers. The "creativity" dial visibly reshapes the bars: turned up, "chances are flattening quickly" [P215], the pickled egg climbs from "a sliver" to "a slice" [P219], and the model starts repeating a low-probability token [P225]. Turned to maximum, "chances are flat" [P237]. So a low temperature is the un-flattened end of the same dial — the bars stay peaked, so the die lands on the most likely token the same way each time, giving one stable answer from the same model. It does **not** make the answer more factually correct: the story insists creativity is "not truer, it's stranger" [P227] and "It's not smarter. It's stranger" [P241–P243] — turning it down only makes an answer *more likely*, not *more true*. Tag: flattening/temperature **FROM THE TEXT [P215–P227, P237, P241–P243]**; the low-temp-same-answer inversion is inferred from that, so partly **PRIOR KNOWLEDGE**.

**Q8. True/false — the model finds a fact in a training-built store and reads it out.**
**False.** The story is explicit all through: "Meaning is not in the building" [P73], "It didn't look up anything" [P87], "There's no word for it to look up" [P89], "It only ever had numbers" [P310]. The correct answer is produced by computation over numbers, not retrieval from a store; the fact is reconstructed, not read. Tag: **FROM THE TEXT [P73, P87, P89, P310]**.

**Q9. True/false — attention means deliberate focusing like a person concentrating.**
**False.** The story repeatedly denies an agent: "Nobody decided anything" [P125], "Nobody's deciding, Peter" [P133], "Nobody's deciding. It added up percentages" [P135], and "It doesn't think" [P145]. The weighting is arithmetic (scores normalised to 100%), not intent. Tag: **FROM THE TEXT [P125, P133–P135, P145]**.

**Q10. Where the "one token at a time from a distribution" picture breaks down or misleads for a real chat model.**
The story's box is stateless between jobs — "there's no last week," "nothing's filed" [P161, P187] — and works from a bare input with no instructions, no history and no training discipline; it also has to be *told* not to look things up. A real chat model differs exactly there: it conditions on a whole long context (system prompt plus conversation, not one bare sentence), its behaviour is shaped by large-scale training plus instruction tuning/RLHF so "knowing where you're going" partly comes from alignment rather than attention alone, and it can call tools or be constrained by decoding rules. So the story's loop is faithful as the *core decoding step* but misleading about the surrounding machinery: it presents a fresh, memoryless, unaligned next-token engine as if that were the whole chat model. Tag: the story's statelessness **FROM THE TEXT [P161, P187]**; the training/context/alignment omissions **PRIOR KNOWLEDGE**.

## Part 4 — Calibration

I would have got Q1–Q5 and Q8–Q9 right **without** the story, because I already know the transformer architecture; the story's real contribution was not new facts but vivid, transferable framings — softmax as a forced-100% row that rescales everything when one input changes, and temperature as flattening the bars (stranger, not truer). Q6 (truncation) and Q7's low-temperature inversion are the two I completed by inference from the story's premises rather than from anything it showed directly, and Q10 is almost entirely prior knowledge with only the statelessness coming from the text.
