# Style evidence — Family Guy mechanics, citation-backed

Run: `2026-10-10-the-transformer-architecture-family-guy` · Role: style-critic (profile mode) · Date: 2026-10-10.

Method: literal and regex search over the read-only `FG_Subtitles` corpus via `tools/fg_search.py`; raw hits are in `scratch/fg_hits/*.json` (with `S##E## @ mm:ss`). Semantic/hybrid were **not** run for this artifact (the index/model download was in progress elsewhere — literal/regex are exact and offline, so they carry all frequency claims). Counts come from the `count` field of each hit payload; a count equal to the `--limit` I passed is written `≥N (cap N)` because the search was truncated.

> Copyright note: subtitle text is **not** reproduced here. Each row paraphrases the observed mechanic and cites its location. No excerpt is quoted beyond a few-word catchphrase.

Evidence rows: **30** (numbered E1–E30). Coverage: recurring gags/tic words (E1–E12), cutaway set-ups (E13–E20), character speech habits (E21–E25), repetition & format (E26–E28), negative findings (E29–E30).

## Recurring gags and tic words

| # | Mechanic | Citation(s) | Observed |
|---|---|---|---|
| E1 | Quagmire's reflex tic "giggity" | `S17E15 @ 00:07:00`, `S15E03 @ 00:07:16`, `S08E05 @ 00:20:10`, `S04E25 @ 00:11:30`, `S09E12 @ 00:00:52` | **≥25 hits (cap 25).** Blurted involuntarily; in S17E15 a character is *told* he said it and apologises. The tic is funny because it is ill-timed, not because it recurs. |
| E2 | Quagmire's tic deployed as a question/echo | `S15E03 @ 00:07:16` | The tic is repeated back at him ("is that a giggity?"), i.e. the show treats its own catchphrase as an object. |
| E3 | "shut up, Meg" as the family's default dismissal | `S11E17 @ 00:20:39`, `S17E07 @ 00:05:34`, `S07E05 @ 00:13:27`, `S13E01 @ 00:13:20`, `S10E02 @ 00:07:48`, `S16E18 @ 00:19:10` | **≥15 hits (cap 15).** Repeated 3–4× in a row (S11E17) and escalated to a return ("no, you shut up, Meg", S17E07). The joke is the dismissal. |
| E4 | Stewie's "what the deuce" | `S21E18 @ 00:17:43`, `S02E17 @ 00:02:21`, `S02E15 @ 00:07:39`, `S04E22 @ 00:10:34`, `S13E01 @ 00:11:20` | **≥25 hits (cap 25).** In S13E01 a character lists it among the show's recognised catchphrases — the show is self-aware about its tics. |
| E5 | Stewie's "victory is mine" | `S01E02 @ 00:19:55`, `S01E01 @ 00:18:01`, `S02E12 @ 00:20:28`, `S01E03 @ 00:21:08` | **6 hits.** Archaic villain register, usually immediately punctured by the ordinary consequence. |
| E6 | Stewie's "damn you" directed at people *and* objects | `S02E17 @ 00:20:25` (directed at ice cream), `S01E01 @ 00:18:01`, `S04E08 @ 00:17:09`, `S01E02 @ 00:01:11` | **≥20 hits (cap 20).** Grandiose curse aimed at a trivial target — the register mismatch is the pattern. |
| E7 | Stewie's ornate diction ("wretched", "vile", "harridan") | `S01E01 @ 00:20:17`, `S10E05 @ 00:05:13`, `S02E15 @ 00:09:58`, `S02E14 @ 00:14:02` | **≥12 hits (cap 12)** for "wretched" alone. Formal/archaic adjectives in a baby's mouth, next to crude lines. |
| E8 | Stewie's "blast" / stage-villain curse | `S03E11 @ 00:11:35`, `S02E16 @ 00:00:34` | **≥12 hits (cap 12).** "Blast you…" constructions; comic-book villainy as a speech habit. |
| E9 | Stewie's teddy bear Rupert as a scene partner | `S02E18 @ 00:02:07`, `S16E11 @ 00:06:15`, `S11E06 @ 00:15:52`, `S11E18 @ 00:03:09`, `S21E03 @ 00:16:29` | **≥12 hits (cap 12).** Stewie addresses the bear as a confidant — the infantile register under the grandiosity. |
| E10 | Peter's "oh my god" (shared exclamation) | `S03E03 @ 00:16:41`, `S08E03 @ 00:07:08`, `S04E09 @ 00:13:53`, `S03E14 @ 00:09:21` | **≥15 hits (cap 15).** Often repeated 3–4× in a row; a family-wide exclamation, not one character's. |
| E11 | "are you kidding (me)" as scepticism | `S03E02 @ 00:20:28`, `S11E13 @ 00:01:01`, `S16E08 @ 00:12:33`, `S12E04 @ 00:08:46` | **≥12 hits (cap 12).** Questions used as accusations, not requests for information. |
| E12 | Slang filler "dude" | `S02E14 @ 00:00:32`, `S15E01 @ 00:12:36`, `S05E13 @ 00:10:30`, `S16E02 @ 00:12:21` | **≥12 hits (cap 12).** Diffuse slang across characters — **not** a reliable Chris-only marker; don't over-assign it. |

## Cutaway set-up formulas

| # | Mechanic | Citation(s) | Observed |
|---|---|---|---|
| E13 | "Remember when…" launches a flashback cutaway | `S02E03 @ 00:07:24`, `S01E02 @ 00:06:40`, `S01E04 @ 00:03:20`, `S01E02 @ 00:08:58`, `S11E15 @ 00:01:05` | **≥15 hits (cap 15).** The archetypal set-up line: spoken comparison + memory, then a hard cut to the scene. |
| E14 | "Remember the time…" variant | `S01E05 @ 00:14:01`, `S02E08 @ 00:03:44` | **4 hits.** Same device, slightly different cue; the show uses both. |
| E15 | "This is just like…" comparison cutaway | `S04E12 @ 00:11:59`, `S05E02 @ 00:05:19`, `S05E09 @ 00:02:46` | **6 hits.** The line is the *set-up*; the cutaway supplies the *scene*. |
| E16 | "Like the time…" comparison cutaway | `S03E22 @ 00:12:01`, `S04E13 @ 00:07:58`, `S04E19 @ 00:11:58` | **5 hits.** Points at a concrete past event; the writer should make the event specific. |
| E17 | "This is worse than…" escalation cutaway | `S07E12 @ 00:14:25`, `S04E05 @ 00:07:06`, `S15E07 @ 00:11:57`, `S21E06 @ 00:14:17` | **11 hits.** S07E12 even has a character note that a line can barely *set up* a cutaway — meta-framing of the device. |
| E18 | "We now return to…" fake-TV cutaway frame | `S03E17 @ 00:13:17`, `S02E15 @ 00:17:04`, `S03E15 @ 00:07:59`, `S06E04 @ 00:11:03`, `S16E18 @ 00:08:37` | **≥20 hits (cap 20).** The cutaway is framed as an invented programme already in progress; an announcer line does the cut, so no narrator voice is needed. |
| E19 | "Meanwhile…" cross-cut | `S08E20 @ 00:24:50`, `S01E07 @ 00:02:14`, `S08E07 @ 00:12:31`, `S15E04 @ 00:16:36` | **14 hits.** A hard location jump signalled by one word — no description of the new place. |
| E20 | "You know what…" set-up/tic (Peter register) | `S07E07 @ 00:11:31`, `S10E08 @ 00:20:34`, `S14E17 @ 00:01:27`, `S13E05 @ 00:11:07`, `S10E21 @ 00:17:23` | **≥20 hits (cap 20).** Frequently doubled ("You know what? You know what?") — repetition as an escalation device. |

## Character speech habits

| # | Mechanic | Citation(s) | Observed |
|---|---|---|---|
| E21 | Lois as the voice of doubt ("Peter, you can't…") | `S02E16 @ 00:09:17`, `S02E19 @ 00:14:17`, `S16E16 @ 00:15:30`, `S12E15 @ 00:11:10` | **≥15 hits (cap 15).** She states the consequence; the joke is that she is ignored. Her function is the *react-and-correct* beat the run needs. |
| E22 | Characters talk past each other / answer the wrong line | `S16E06 @ 00:05:05`, `S07E07 @ 00:11:31`, `S06E09 @ 00:14:18` | Overlap and non-response are constant; the cutaway is sometimes announced *as* the response to a threat. |
| E23 | Stewie's ornate sentence collapsing into a tantrum | `S01E02 @ 00:01:11`, `S02E16 @ 00:00:34`, `S10E05 @ 00:05:13` | Long formal construction → abrupt crude/childish demand. Length is comic; the collapse is the button. |
| E24 | Peter's confident-wrongness / assertions as logic | `S02E03 @ 00:03:43`, `S04E11 @ 00:16:57`, `S02E19 @ 00:14:17` | He asserts a nonsense position as fact; others react. Distinct from Brian's dry scepticism and Stewie's ornate rage. |
| E25 | Vulgar/crude register next to mock-formal | `S04E22 @ 00:10:34`, `S10E05 @ 00:05:13`, `S05E01 @ 00:17:04` | Register whiplash is systematic; the crude line and the antique line sit adjacent. |

## Repetition and subtitle-format evidence

| # | Mechanic | Citation(s) | Observed |
|---|---|---|---|
| E26 | Deadpan repetition of a word, then inversion | `S05E08 @ 00:19:48` → `S05E08 @ 00:20:02` | In the excerpts: "for a while" is repeated and answered flatly ~7 times over ~14 seconds, then broken by a character noting the other is acting weird. Repetition is structure. |
| E27 | Repeated "No, no, no…" refusal avalanche | `S05E08 @ 00:02:21`, `S05E15 @ 00:11:23`, `S05E15 @ 00:11:27`, `S05E15 @ 00:11:31` | Identical short refusals stacked and lengthened ("No, no, no!" → longer), a rhythmic tic the prose can mirror. |
| E28 | Delivery tags as the only stage direction | `S21E04 @ 00:10:27`, `S21E04 @ 00:12:10`, `S21E05 @ 00:17:38`, `S21E05 @ 00:08:19`, `S21E02 @ 00:00:50` | **≥25 hits (cap 25)** for `(sighs|laughs|weakly|laughing)`. Format: `SPEAKER (laughs):` or a bare `(sighs)` line. In prose these become sparse action beats. Also note the era split: S01 cues are ALL CAPS, S05+ mixed case (a formatting artefact, not a style choice). |

## Negative findings (things a pasticheur would get wrong)

| # | Mechanic | Citation(s) | Observed |
|---|---|---|---|
| E29 | "grinds my gears" is **not** in the subtitle corpus | searched `grinds my gears` (0), `really grinds my gears` (0), `gears` (1, unrelated `S17E10 @ 00:14:07`) | The famously attributed Peter catchphrase does not appear. Do **not** deploy it as a canonical tic; it dates to the movie, not the episode dialogue sampled. |
| E30 | Other searched formulas that are absent or rare | `this is like that time` (0); `you've got to be kidding` (1, `S06E06 @ 00:11:06`) | The real set-up formulas are "this is just like…", "like the time…", "this is worse than…" — not the literal phrase a parodist would invent. |

## Post-rebuild note (2026-10-10)

The excerpt corpus was rebuilt after this file was first written (`style_profile.py` now reports **12 files, 14,366 words, seasons 1/5/10/15/21**). The rebuild does **not** affect any frequency claim here — E1–E25 and E28–E30 are cited from literal/regex hits over the **full 18-season DB**, not from the excerpts. Two rows, however, had used *excerpt* citations and must be read with the rebuild in mind:

- **E26** ("a while" deadpan repetition, `S05E08 @ 00:19:48–00:20:02`): `S05E08` is **no longer in the sample**. The DB hit is still real, but the row's parenthetical "in the excerpts" is now stale — treat it as a DB citation, not an excerpt one.
- **E27** (`S05E08 @ 00:02:21`, `S05E15 @ 00:11:23–31`): the `S05E08` and `S05E15` excerpt citations are also **no longer in the sample**; the repetition pattern itself remains valid (it is a show-wide habit visible in the DB hits).
- **E28**'s era-split claim ("S01 caps, later mixed case") is unaffected — S01 and S21 are both in the rebuilt sample, and the new profile's sample note restates it.

No other row depended on the old corpus era.

## How to use this

- The **cutaway engine** is E13–E20: pick a set-up formula, cut hard, play a miniature scene, cut back to a reaction (E21).
- The **tic words** E1–E12 are real but are *texture*: they only work when the scene, escalation and reaction are present. This evidence file is **not** to be handed to the writer as text to reuse (AGENTS rule 4); the profile summarises it.
- The **negative findings** E29–E30 are the strongest anti-pastiche guardrail: the phrases a model "remembers" are not always the phrases the show uses.
