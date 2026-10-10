"""Tests for tools/fg_corpus.py. Run: python -m unittest discover -s tests -v"""
from __future__ import annotations

import contextlib
import io
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import fg_corpus  # noqa: E402

SRT = """1
00:00:01,000 --> 00:00:03,000
<i>Hello</i> there, friend.

2
00:00:04,000 --> 00:00:06,000
\u266a la la la \u266a

3
00:00:07,000 --> 00:00:09,000
WILL BE 4 HOURS IN THE

4
00:00:10,000 --> 00:00:12,000
SNAKEPIT. I\u2019m afraid.
"""

HI_SRT = """1
00:00:01,000 --> 00:00:03,000
PETER: Shut up, Meg.

2
00:00:04,000 --> 00:00:06,000
[LOIS]: Peter, no.
"""


def run_cli(main, argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


def make_db(path: Path):
    con = sqlite3.connect(path)
    con.executescript(
        """
        CREATE TABLE episodes (id INTEGER PRIMARY KEY, season INTEGER, episode INTEGER,
                               title TEXT, title_pretty TEXT, year INTEGER);
        CREATE TABLE subtitles (id INTEGER PRIMARY KEY, episode_id INTEGER, language TEXT,
                                variant TEXT, is_default INTEGER, release_name TEXT,
                                cues INTEGER, content TEXT);
        """
    )
    for ep in (1, 2):
        con.execute("INSERT INTO episodes VALUES (?,?,?,?,?,?)",
                    (1000 + ep, 1, ep, "t", "T", 1999))
    # episode 1: default (no tags) + HI (tags)
    con.execute("INSERT INTO subtitles VALUES (?,?,?,?,?,?,?,?)",
                (1, 1001, "en", "non-HI", 1, "r.srt", 3, SRT))
    con.execute("INSERT INTO subtitles VALUES (?,?,?,?,?,?,?,?)",
                (2, 1001, "en", "HI", 0, "hi.srt", 2, HI_SRT))
    con.execute("INSERT INTO subtitles VALUES (?,?,?,?,?,?,?,?)",
                (3, 1002, "en", "non-HI", 1, "r.srt", 1, SRT))
    # season 2: one episode, default subtitle only
    con.execute("INSERT INTO episodes VALUES (?,?,?,?,?,?)", (2001, 2, 1, "t", "T", 2000))
    con.execute("INSERT INTO subtitles VALUES (?,?,?,?,?,?,?,?)",
                (4, 2001, "en", "non-HI", 1, "r.srt", 1, SRT))
    con.commit()
    con.close()


class TmpCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()


class TestParseSrt(unittest.TestCase):
    def test_cleans_tags_music_quotes_and_wrapping(self):
        cues = fg_corpus.parse_srt(SRT)
        self.assertEqual([c.text for c in cues], [
            "Hello there, friend.",
            "WILL BE 4 HOURS IN THE",
            "SNAKEPIT. I'm afraid.",
        ])
        self.assertAlmostEqual(cues[0].start, 1.0)
        self.assertAlmostEqual(cues[2].end, 12.0)

    def test_speaker_tags_only_when_labelled(self):
        plain = fg_corpus.parse_srt(HI_SRT)
        self.assertEqual(plain[0].speaker, None)
        self.assertEqual(plain[0].text, "PETER: Shut up, Meg.")
        tagged = fg_corpus.parse_srt(HI_SRT, labelled=True)
        self.assertEqual((tagged[0].speaker, tagged[0].text), ("PETER", "Shut up, Meg."))
        self.assertEqual((tagged[1].speaker, tagged[1].text), ("LOIS", "Peter, no."))

    def test_split_speaker_rejects_non_names(self):
        self.assertEqual(fg_corpus.split_speaker("no colon here"), (None, "no colon here"))
        self.assertEqual(fg_corpus.split_speaker("A B C D: too many"),
                         (None, "A B C D: too many"))


class TestSampling(unittest.TestCase):
    def test_evenly_pick(self):
        self.assertEqual(fg_corpus.evenly_pick([1, 2, 3], 5), [1, 2, 3])
        self.assertEqual(fg_corpus.evenly_pick(list(range(10)), 3), [0, 4, 9])

    def test_pick_blocks_short_and_spread(self):
        self.assertEqual(fg_corpus.pick_blocks(5, 3, 60), [(0, 5)])
        self.assertEqual(fg_corpus.pick_blocks(5, 1, 2), [(0, 5)])
        blocks = fg_corpus.pick_blocks(300, 3, 60)
        self.assertEqual(blocks[0][0], 0)
        self.assertEqual(blocks[-1][1], 300)
        self.assertTrue(all(hi - lo <= 60 for lo, hi in blocks))
        # no overlapping/adjacent merges for a big episode
        self.assertEqual(len(blocks), 3)


class TestBuild(TmpCase):
    def test_writes_excerpts_and_citations(self):
        fg = self.tmp / "FG"
        (fg / "data").mkdir(parents=True)
        make_db(fg / "data" / "family_guy_subtitles.db")
        out = self.tmp / "styles" / "family-guy"
        info = fg_corpus.build(fg, out, seasons=[1], episodes_per_season=5,
                               blocks=1, block_cues=60, target_words=1000, labelled=True)
        self.assertEqual(info["files"], 2)
        self.assertFalse(info["reached_target"])
        rows = [json.loads(l) for l in (out / "citations.jsonl").read_text().splitlines()]
        self.assertEqual(len(rows), info["cues"])
        self.assertEqual(rows[0]["speaker"], "PETER")
        self.assertEqual(rows[0]["file"], "excerpt-S01E01.txt")
        self.assertEqual(rows[0]["line"], 1)
        # excerpt lines line up with the citation rows
        excerpt = (out / "excerpt-S01E01.txt").read_text().splitlines()
        self.assertEqual(excerpt[0], "PETER: Shut up, Meg.")
        self.assertEqual(len(excerpt), sum(1 for r in rows if r["file"] == "excerpt-S01E01.txt"))

    def test_unlabelled_uses_default_even_when_hi_exists(self):
        fg = self.tmp / "FG"
        (fg / "data").mkdir(parents=True)
        make_db(fg / "data" / "family_guy_subtitles.db")
        out = self.tmp / "styles" / "fg"
        info = fg_corpus.build(fg, out, seasons=[1], episodes_per_season=5,
                               blocks=1, block_cues=60, target_words=1000, labelled=False)
        self.assertEqual(info["files"], 2)
        first = (out / "excerpt-S01E01.txt").read_text().splitlines()[0]
        self.assertEqual(first, "Hello there, friend.")

    def test_target_spreads_across_all_requested_seasons(self):
        fg = self.tmp / "FG"
        (fg / "data").mkdir(parents=True)
        make_db(fg / "data" / "family_guy_subtitles.db")
        out = self.tmp / "styles" / "fg"
        fg_corpus.build(fg, out, seasons=[1, 2], episodes_per_season=5,
                        blocks=1, block_cues=60, target_words=4, labelled=False)
        seasons = {json.loads(l)["season"] for l in (out / "citations.jsonl").read_text().splitlines()}
        self.assertEqual(seasons, {1, 2})

    def test_missing_db_and_unknown_season_are_clean_errors(self):
        code, _, err = run_cli(fg_corpus.main, ["--out", str(self.tmp / "o"), "--fg-dir", str(self.tmp / "nope")])
        self.assertEqual(code, 2)
        self.assertIn("no subtitle database", err)
        fg = self.tmp / "FG"
        (fg / "data").mkdir(parents=True)
        make_db(fg / "data" / "family_guy_subtitles.db")
        code, _, err = run_cli(fg_corpus.main, ["--out", str(self.tmp / "o"), "--fg-dir", str(fg), "--seasons", "9"])
        self.assertEqual(code, 2)
        self.assertIn("season(s) not in the database", err)


if __name__ == "__main__":
    unittest.main()
