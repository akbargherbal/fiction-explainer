# Style profile: Family Guy

Grounding: GROUNDED (12 files, 14,366 words, 2,159 cues — seasons **1, 5, 10, 15 and 21**).
Source: dialogue-only subtitles (`styles/family-guy/`, built by `tools/fg_corpus.py --labelled`); measured with `tools/style_profile.py profile styles/family-guy --dialogue`. The stats JSON is the floor for rhythm, not a description of voice.

> **Sample note.** The 12 files are `S01E01,02,03 · S05E01,04 · S10E01,05 · S15E01,05 · S21E01,04,08` — a spread across the show's eras. Subtitle *format* still changes over time (S01 cues are ALL CAPS; later seasons are mixed case with parenthesised delivery tags), so some of what looks like a "style choice" is a subtitle-encoding artefact. The numbers below blend all five seasons.

## Voice in one paragraph

Family Guy has no narrator, no description and no attributions — everything is spoken. The "voice" is a rapid ping-pong of short utterances (median six words) that escalate and deadpan, punctured by hard cuts to unrelated miniature scenes: a character names a feeling or makes a comparison ("this is just like…", "remember when…", "you know what…"), the show jumps to a fake TV show, a fake flashback, a fake ad or a random event, one beat lands the joke, and it cuts back to an irritated reaction. Characters are selfish, loud and confidently wrong; sincerity is almost always a set-up for a puncture; repetition is structure (a phrase said three or four times flat, then inverted). The register is casually vulgar next to sudden mock-formality, and the emotional temperature is sardonic detachment with comic spikes of rage or terror. Nothing is explained; everything is enacted.

## Measured targets

Reference = this corpus in dialogue mode (each non-empty line is one utterance; `dialogue_share = 1.0`). Range = ±35% (floors applied for near-zero metrics). Prose drafts will not match dialogue-mode *counts* like `dialogue_share`; treat the **rhythm and punctuation** rows as the usable targets, and read "utterance" as "beat of speech".

| Metric | Reference | Acceptable range (±35%) |
|---|---|---|
| words | 14,366 | — |
| utterances (lines) | 2,159 | — |
| sent_mean (utterance mean, words) | 6.65 | 4.3 – 9.0 |
| sent_median | 6.0 | 3.9 – 8.1 |
| sent_stdev | 3.27 | 2.1 – 4.4 |
| sent_p90 | 11.0 | 7.2 – 14.9 |
| short_sent_share (≤6 words) | 0.501 | 0.33 – 0.68 |
| long_sent_share (≥30 words) | 0.000 | ≈ 0 |
| para_mean / para_median (= utterance) | 6.65 / 6.0 | 4.3 – 9.0 |
| dialogue_share | 1.000 | (dialogue-only; ~1) |
| commas_per_1k | 84.2 | 55 – 114 |
| semicolons_per_1k | 0.000 | **0** |
| colons_per_1k | 3.69 | 2.4 – 5.0 |
| em_dashes_per_1k | 0.000 | **≈ 0** |
| questions_per_1k | 27.1 | 18 – 37 |
| exclamations_per_1k | 16.4 | 11 – 22 |
| ellipses_per_1k | 4.73 | 3.1 – 6.4 |
| parens_per_1k | 9.12 | 5.9 – 12.3 |
| first_person_per_1k | 71.4 | 46 – 96 |
| second_person_per_1k | 48.2 | 31 – 65 |
| ly_adverbs_per_1k | 10.0 | 6.5 – 13.5 |
| past_tense_hint | 0.437 | 0.28 – 0.59 |
| conj_start_share | 0.082 | 0.05 – 0.11 |
| pronoun_start_share | 0.192 | 0.12 – 0.26 |
| the_start_share | 0.010 | 0.007 – 0.014 |
| mattr_250 (lexical variety) | 0.634 | 0.41 – 0.86 |

Top content words: know (94), right (82), well (67), yeah (60), peter (54), stewie (46), time (43), chris (43), good (41), brian (40), think (36), want (36), okay (35), look (34), gonna (34), come (33), lois (33), back (29), going (27), sorry (27), really (26), guys (24), griffin (22), hell (21), great (21).

Read like this: **half of all lines are six words or shorter (50.1%); not one is thirty words.** Roughly one question every 37 words and one exclamation every 61 words — note the exclamation rate (16.4/1k) is now *lower* than the questions rate and far below the early-era-only reading, because later seasons shout less in caps and tag delivery in parentheses instead (parens are up to 9.1/1k). Punctuation is commas, periods, `?`, `!`, ellipses and `(delivery tags)` — **no semicolons, no em dashes**. First and second person dominate. The content-word list is almost entirely interactional ("know, right, well, yeah, come, think, want, okay") — this voice runs on talk, not on things.

## Point of view, tense, narrative distance

- **No narrator, therefore no POV and no interiority.** We never get inside a head; every thought a character has is spoken aloud, however implausible. There is no descriptive camera — the subtitles contain zero scene-setting.
- **Present tense, first person, direct address.** Characters refer to "I", "you", "we"; they talk *at* each other and past each other. Past tense appears inside flashback/cutaway set-ups ("remember when…", "like the time…"), never as narration.
- **Distance is zero and unattributed.** The speaker's name usually arrives only as a `SPEAKER:` tag or in the other character's reply; dialogue is naked. For this run's prose form, the writer may tag minimally but must not drift into a guiding narrator.

## Sentence and paragraph rhythm

- **Utterance length is the whole game.** Mean 6.65, median 6, p90 11; 50% of lines are ≤6 words; the longest speech in 2,159 cues never reaches 30 words. Long turns exist only as **comic over-extension** (a character refusing to stop, or an elaborate Stewie aria) — the length itself is the joke.
- **Real paragraphs are absent.** In the source, one cue = one line. The equivalent unit in prose is the *exchange*, not the paragraph: 2–6 short lines, then a beat, then a cut.
- **Staccato and interruptive.** Characters cut in, finish each other's insults, repeat a word back as a question, or answer a statement with a one-word dismissal. Rhythm rises by *acceleration and repetition*, not by subordination.
- **Punctuation palette.** Commas 84/1k; questions 27/1k; exclamations 16/1k; ellipses 4.7/1k; parenthesised delivery tags 9/1k. **Zero semicolons and zero em dashes** — anything that reads as "written prose punctuation" is off-voice.

## Diction and register

- **Favoured:** contractions and elisions (`gonna`, `wanna`, `'cause`), back-channel words (`yeah`, `well`, `right`, `okay`, `oh`, `hey`), direct address (`Lois`, `Peter`, `Brian`), crude/vulgar vocabulary, insults, brand and media nouns, and plain concrete objects (house, couch, dinner, school, bar, mall).
- **Register whiplash is a feature, not noise:** the crudest line can sit beside mock-formal or antique diction (Stewie's "vile woman", "wretched", "harridan", "victory is mine"). The collision is the joke.
- **Avoided registers:** literary narration, adjectival scene-painting, formal connectives ("therefore", "however"), hedging, and anything that sounds *written*. Also basically absent: semicolons, em dashes, subordinate clauses stacked more than one deep.
- **Lazy-pastiche warning:** catchphrases are *not* the diction. "Giggity", "what the deuce", "victory is mine", "shut up, Meg" are real and frequent (see evidence), but the voice lives in the ordinary filler — "yeah", "well", "right", "look", "come on" — far more than in the tic words.

## Imagery and reference domains

- **Pop culture is the reference store** — TV, film, music, commercials, news formats, period sitcoms. But the reference is always *doing a joke*, never decoration: the show invents a fake programme and cuts to it.
- **Meta/self-aware framing:** fake announcer lines ("we now return to…"), fake ads, fake news segments. This is the cutaway's own grammar (below).
- **Domestic and mundane setting:** the house, the dinner table, the couch, the school, the bar, the mall. Grand abstractions are always dragged down to a household object.
- **Run constraint:** the show name-checks real people constantly, but AGENTS rule 10 bans real people as characters here. Keep the *type* — invented shows, generic formats, stock bit-players — and drop the real names.

## How scenes open and close

- **Open mid-conversation.** There is no establishing beat: a character is already complaining, planning, or insulting. The first line usually states a position; the second undermines it.
- **Close on the button.** A scene ends on the punch, not on resolution — often a flat repetition, a non-sequitur, or a character refusing to engage. Then a hard cut.
- **Named cutaway openers** (all attested in the corpus): "We now return to…" (fake-TV frame), "Remember when…" / "Remember the time…" (flashback frame), "This is just like…" / "Like the time…" / "This is worse than…" (comparison frame), and "Meanwhile…" (cross-cut). These are set-up formulas the writer can use as scene-opening buttons.
- **One callback:** the plan asks that at least one cutaway return and land differently — the show does this when a gag or phrase recurs with the stakes changed.

## Dialogue habits

- **Ping-pong, not monologue.** Lines are short; replies arrive fast; interruptions and overlaps are constant. Characters talk past each other and answer the wrong question.
- **Repetition as escalation.** A word or phrase is repeated three or four times deadpan, then inverted (see the deadpan "a while" exchange, S05E08; the shouted all-caps repetitions in S01). Repetition is *structure*, not stammer.
- **Questions as weapons.** "Are you kidding?", "What the hell…?", "You know what?" — questions are accusations, not requests for information.
- **Delivery tags** in parentheses ("(sighs)", "(laughs)", "(weakly)") carry the only stage direction the subtitles keep; in prose they become minimal action beats.
- **No attributions inside the line.** The line is the speech; who said it is inferred from voice and context. Keep tags sparse and let diction identify the speaker.
- **Insults are the register of intimacy.** Family members bond by insulting; the harshest line is often affectionate.

## Cutaway and running-gag grammar (run-specific)

This is the show's engine and the run's teaching engine. The machine:

1. **Set-up line (in the A-plot).** A character makes a claim, a comparison, or invokes a memory in **one short utterance** — "this is just like…", "remember when…", "you know what…", or simply *asserts something false confidently*. The set-up must be specific enough to launch a scene, and it is spoken, never narrated.
2. **Hard cut.** No transition, no "suddenly", no description. The show just lands somewhere else. **In this run the cut is the `* * *` separator.**
3. **The cutaway is a self-contained miniature scene**, usually framed as an invented artefact: a fake TV show ("we now return to…"), a fake flashback ("remember when…"), a fake news/weather/ad segment, or a stock bit-player whose whole existence is the gag.
4. **Escalation.** The premise is pushed exactly one notch past plausible: a second character reacts, a mundane detail is delivered deadpan, or the bit repeats and grows. The cutaway should have its own tiny beginning–punch shape, not just be one line.
5. **The button.** One line lands it — often flat, often a repetition, often the last beat of silence before the cut. Don't explain the joke; the flatness is the landing.
6. **Hard cut back.** Return to the A-plot and let someone **react** — usually doubt or annoyance (Lois or Brian). *The reaction is where the correction lives.* In this run the reaction must fix the oversimplification the cutaway just made, without any narrator saying so.
7. **Running gags / repetition.** A device or phrase returns across the episode. A phrase is said 3–4× deadpan and then inverted. At least one cutaway returns later and lands differently (the callback the plan requires).
8. **Run rule: one concept per cutaway.** If a cutaway enacts two concepts or none, cut it. A bad analogy inside a cutaway is allowed only if events fix it (that is how misconceptions get dramatised rather than contradicted).

## Character voices (run-specific)

Speech habits, not catchphrase karaoke. Use these to distinguish speakers when tags are absent.

- **Peter** — loud, confident and wrong; initiates cutaways by comparing an ordinary moment to something absurd ("this is just like…", "this is worse than…"). Summons Lois by name; treats a non-sequitur as airtight logic; casually dismisses Meg; crude and proud of it. The comedy is **certainty outrunning sense**.
- **Lois** — the straight man and the voice of doubt: "Peter, you can't…", "you're not going to…". Tries to impose consequences; is usually ignored or shouted down. Occasionally as crude or worse than Peter, which is the joke. She is the family's *conscience* register, not its moral narrator.
- **Stewie** — ornate, theatrical, villain-register diction ("vile woman", "wretched", "harridan", "blast you", "victory is mine") in a baby's body, alternating with an infantile agenda (his teddy bear Rupert, "Mommy"). The pattern is **grandiosity curdling into tantrum** — elaborate sentences that collapse into a scream or a petty demand.
- **Brian** — the sceptical question and the smug high-minded stance. Punctures others with a flat query or a dry correction; wants to be taken seriously (writing, politics, "as the voice of reason"). His pretension is the target.
- **Quagmire** — a single reflex tic ("giggity") fired at the wrong moment, plus a leering register and the verbal habit "all right". The tic is funny because it is **involuntary and ill-timed**; a tic planted for its own sake is pastiche.
- **Chris** — sweet, dim, literal, agreeable; the innocent straight man. Takes things at face value and says "dude". His simplicity sets up others' cruelty or absurdity.
- **Meg** — the ignored one. Her lines are cut off, answered with a flat dismissal ("shut up, Meg"), or used as a punchline. The joke is the **dismissal**, not Meg — write her as seeking approval in a family that withholds it.

## Humor, irony, emotional temperature

- **Sardonic detachment, fast escalation, non-sequitur.** The default temperature is low and deadpan; rage, terror and disgust arrive as comic spikes (all-caps in the early era, parenthesised screams later).
- **Irony machine:** a sincere or "very special lesson" register is set up only to be punctured immediately after. An episode that ends on a moral note usually undercuts it in the next line.
- **Confident wrongness:** the funniest stance is a character being certain and incorrect, not a character being stupid. Someone who is *right* (usually Lois) is ignored.
- **No earned sentiment.** Warmth can appear for one beat, but it is either used as a set-up or immediately stepped on. Sustained sincerity is off-voice.

## Negative space — what this voice never does

- No narrator and no explanation: no "in other words", "essentially", "think of it like", no moralising voice-over.
- No interior monologue, no lyrical description, no scene-setting, no weather-for-mood.
- No semicolons, no em dashes, no formal connectives.
- No slow burn: jokes arrive every few lines, not at the end of a paragraph.
- No ambiguity of meaning — the joke must be legible on first read.
- No real people as characters (run constraint).
- No sustained seriousness or unresolved tenderness.
- No cutaway that teaches nothing, and no cutaway that teaches two things (run constraint).

## Lazy-pastiche traps — what a shallow imitation gets wrong

- **Catchphrase karaoke:** "giggity", "victory is mine", "shut up, Meg" dropped in with no scene, escalation or reaction underneath them. The tic is the surface; the habit is the target.
- **Random-cutaway syndrome:** cutting away for no reason to a random pop reference. Every cutaway needs a set-up, an escalation and a reaction that does work.
- **Swearing as the joke:** profanity substituting for structure. The show is crude, but crudeness is a texture, not the punchline.
- **A narrator sneaking in to explain the lesson** — the single worst failure mode for this run.
- **The cutaway as a list item:** a one-line "and then this happened" instead of a miniature scene with its own escalation.
- **Dated real-world references** and real celebrities (also banned here).
- **Sentimentality:** making the family nice, or letting a sincere ending stand un-punctured.
- **Flattening the voices:** everyone sounding like Peter. The profile above exists so they don't.

## Writer's checklist

- **Do** keep most speech beats ≤ ~8 words; half ≤ 6. Never write a 30-word utterance unless the length is the joke.
- **Do** open scenes mid-conversation and end on a button, then cut (`* * *`).
- **Do** give every cutaway the full four-step shape: set-up line → hard cut → escalating miniature with a flat button → hard cut back to an in-character reaction.
- **Do** put the concept correction in a *character's reaction*, never in narration.
- **Do** enforce one concept per cutaway; cut anything that does two or none.
- **Do** use repetition structurally: repeat a phrase 3–4× deadpan, then invert.
- **Do** keep the punctuation palette to commas, periods, `?`, `!`, ellipses, and sparse `(delivery tags)`; **no semicolons, no em dashes**.
- **Don't** use a narrator or any explanatory connectives ("essentially", "in other words", "think of it like").
- **Don't** write interior monologue or descriptive scene-setting.
- **Don't** deploy a catchphrase without the habit, scene and reaction that earn it.
- **Don't** name real people; keep references as invented formats and generic bit-players.
- **Don't** let a sincere or moralising beat survive un-punctured.
