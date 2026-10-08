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

## Copyright

Excerpts are analysed locally to build a style profile and measured stats. They are never copied into `runs/`, and `styles/*/` is git-ignored so they cannot be pushed by accident. Only add text you have the right to analyse.

For a **genre** target ("cosy mystery", "epistolary horror") with no specific author, excerpts are optional; without them the profile is marked `UNGROUNDED` and rests on genre conventions known to the model.
