# styles/

Put style excerpts here, one folder per style target:

```
styles/<style-slug>/
    excerpt-01.txt
    excerpt-02.md
    ...
```

The slug is the style name lower-cased and hyphenated: `Jorge Luis Borges` → `jorge-luis-borges`, `cosy mystery` → `cosy-mystery`. `python tools/new_run.py` prints the slug it expects.

## What to put in

- 3-10 excerpts, roughly 5,000+ words in total (more is better for the measured stats).
- A mix of narration and dialogue, and of openings, middles and endings.
- Prose that is *representative*, not the author's most famous showpiece paragraph.
- Plain text or Markdown. Strip page numbers, running headers and footnotes.

## Dialogue-only corpora (subtitles, screenplays)

Some style targets are dialogue only and carry no quote marks, so the usual
`dialogue_share` measurement reads zero. Two tools handle that:

- `python tools/fg_corpus.py --out styles/<slug> [--labelled]` builds excerpts
  from the read-only `FG_Subtitles` database next to this repo (one cue per line,
  plus a `citations.jsonl` mapping each line to `S##E## @ mm:ss`). `--labelled`
  prefers the hearing-impaired subtitles so lines carry `SPEAKER:` tags; set
  `FG_SUBTITLES_DIR` or `--fg-dir` if the clone lives elsewhere.
- `python tools/style_profile.py profile styles/<slug> --dialogue` treats each
  non-empty line as one utterance and sets dialogue share to 1.0. Pass the same
  `--dialogue` flag to `compare` for the reference.

`citations.jsonl` is not an excerpt (`corpus_files` ignores `.jsonl`); it exists so
reviewers can cite a line without copying subtitle text into a run file.

## Copyright

Excerpts are analysed locally to build a style profile and measured stats. They are never copied into `runs/`, and `styles/*/` is git-ignored so they cannot be pushed by accident. Only add text you have the right to analyse.

For a **genre** target ("cosy mystery", "epistolary horror") with no specific author, excerpts are optional; without them the profile is marked `UNGROUNDED` and rests on genre conventions known to the model.
