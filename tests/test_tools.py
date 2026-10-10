"""Tests for the fiction-explainer tools. Run: python -m unittest discover -s tests -v"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import archive_notes  # noqa: E402
import lock_check  # noqa: E402
import mdutil  # noqa: E402
import new_run  # noqa: E402
import notes_digest  # noqa: E402
import number_paragraphs  # noqa: E402
import run_status  # noqa: E402
import slop_lint  # noqa: E402
import style_profile  # noqa: E402

STORY = """# The Ledger

Marta carried the ledger down to the cellar. The lamp guttered. She set the book on the barrel and counted the jars twice.

"Forty," she said. "There were forty yesterday."

* * *

Her brother came at dusk with the news from the port. He ate standing up.

Nobody mentioned the missing jar.

At midnight the cellar door opened by itself.
"""


def run_cli(main, argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class TmpCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text):
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p


class TestMdutil(unittest.TestCase):
    def test_sentences_protect_abbreviations_and_decimals(self):
        s = mdutil.sentences("Dr. Reyes paid 3.5 coins. She left! Did he follow?")
        self.assertEqual(len(s), 3)
        self.assertTrue(s[0].startswith("Dr. Reyes"))
        self.assertIn("3.5", s[0])

    def test_sentences_keep_closing_quotes(self):
        s = mdutil.sentences('He said, "Go." She went.')
        self.assertEqual(len(s), 2)
        self.assertTrue(s[0].endswith('"'))

    def test_numbered_paragraphs_skip_headings_and_rules(self):
        paras = mdutil.numbered_paragraphs(STORY)
        self.assertEqual([p["id"] for p in paras], [1, 2, 3, 4, 5])
        self.assertEqual([p["scene"] for p in paras], [1, 1, 2, 2, 2][:5])
        self.assertEqual(paras[0]["heading"], "The Ledger")
        self.assertTrue(paras[0]["text"].startswith("Marta"))

    def test_numbering_ignores_keep_markers_and_comments(self):
        wrapped = STORY.replace(
            "Marta carried", "<!-- KEEP -->Marta carried"
        ).replace("twice.", "twice.<!-- /KEEP --><!-- a comment -->")
        self.assertEqual(
            [p["text"] for p in mdutil.numbered_paragraphs(wrapped)],
            [p["text"] for p in mdutil.numbered_paragraphs(STORY)],
        )

    def test_parse_notes_ignores_comments_and_continuations(self):
        notes = """# Notes
## Keep
<!-- - "ignored example" -->
- "the real one"
## Change
- [P3] too chatty,
  make it drier
2. second item
## Pivot
## Reject
- no animals
"""
        p = mdutil.parse_notes(notes)
        self.assertEqual(p["keep"], ['"the real one"'])
        self.assertEqual(p["change"], ["[P3] too chatty, make it drier", "second item"])
        self.assertEqual(p["pivot"], [])
        self.assertEqual(p["reject"], ["no animals"])


class TestNumberParagraphs(TmpCase):
    def test_render_and_cli(self):
        f = self.write("d.md", STORY)
        view = number_paragraphs.render(STORY)
        self.assertIn("[P1] Marta carried", view)
        self.assertIn("[P5] At midnight", view)
        self.assertIn("scene 2", view)
        out = self.tmp / "v" / "numbered.md"
        code, _, _ = run_cli(number_paragraphs.main, [str(f), "--out", str(out)])
        self.assertEqual(code, 0)
        self.assertTrue(out.is_file())
        self.assertEqual(run_cli(number_paragraphs.main, [str(self.tmp / "nope.md")])[0], 2)


class TestSlopLint(unittest.TestCase):
    def test_clean_text_has_no_flags(self):
        r = slop_lint.analyze(STORY)
        self.assertEqual(r["flags"], [])
        self.assertEqual(r["findings"], [])

    def test_detects_known_tells(self):
        text = (
            "Marta looked at the tapestry of lights. It wasn't fear. It was something older.\n\n"
            '"Go," she said softly. "Now," he replied quietly. "Wait," she asked gently.\n\n'
            "She was not just tired, but hollow. In other words, the system was a loop.\n\n"
            "She realized that kindness was the real lesson."
        )
        r = slop_lint.analyze(text)
        cats = r["counts"]
        self.assertGreaterEqual(cats.get("slop-word", 0), 1)
        self.assertGreaterEqual(cats.get("negation-reversal", 0), 1)
        self.assertGreaterEqual(cats.get("said-adverb", 0), 3)
        self.assertGreaterEqual(cats.get("not-just-but", 0), 1)
        self.assertGreaterEqual(cats.get("explainer-tell", 0), 1)
        self.assertEqual(cats.get("moral-closer"), 1)
        self.assertIn("said-adverb", " ".join(r["flags"]))

    def test_explainer_tell_ignored_inside_dialogue(self):
        text = 'The boy listened. "In other words, essentially, it is a loop," said the cook. "Essentially a loop."'
        self.assertNotIn("explainer-tell", slop_lint.analyze(text)["counts"])

    def test_opener_run(self):
        text = "She sat. She waited. She counted. Then the bell rang."
        r = slop_lint.analyze(text)
        self.assertEqual(r["counts"].get("opener-run"), 1)

    def test_density_flags_need_enough_words(self):
        short = "He ran — fast — far — away."
        self.assertEqual(slop_lint.analyze(short)["flags"], [])
        long = ("The cart rolled — slowly — down the hill. " * 40)
        self.assertTrue(any("em-dash" in f for f in slop_lint.analyze(long)["flags"]))

    def test_ignore_and_override(self):
        long = ("The cart rolled — slowly — down the hill. " * 40)
        self.assertFalse(any("em-dash" in f for f in slop_lint.analyze(long, ignore=["em-dash"])["flags"]))
        self.assertFalse(any("em-dash" in f for f in slop_lint.analyze(long, overrides={"em-dash": 500})["flags"]))

    def test_cli_out_and_strict(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_text("A tapestry of light. " * 5, encoding="utf-8")
            out = Path(d) / "r" / "lint.md"
            code, stdout, _ = run_cli(slop_lint.main, [str(f), "--out", str(out), "--strict"])
            self.assertEqual(code, 1)
            self.assertIn("flag", stdout)
            self.assertIn("slop-word", out.read_text(encoding="utf-8"))


class TestStyleProfile(TmpCase):
    SHORT = "He ran. She hid. They waited. The rain fell. Nobody spoke. It ended. " * 60
    LONG = (
        "When the rain finally came, long after everyone in the valley had stopped believing in it, "
        "the old woman stood at the window and thought about all the years that had passed, "
        "each one slower and heavier than the last, and none of them kind. "
    ) * 25

    def test_compute_basic_numbers(self):
        s = style_profile.compute(self.SHORT)
        self.assertGreater(s["words"], 300)
        self.assertAlmostEqual(s["metrics"]["sent_mean"], 2.5, delta=0.6)
        self.assertEqual(s["metrics"]["dialogue_share"], 0)
        self.assertGreater(s["metrics"]["short_sent_share"], 0.9)

    def test_dialogue_share_detected(self):
        t = '"Hello there my friend." He nodded and walked away from the door slowly.'
        self.assertGreater(style_profile.compute(t)["metrics"]["dialogue_share"], 0.3)

    def test_compare_flags_long_vs_short(self):
        ref, dr = style_profile.compute(self.SHORT), style_profile.compute(self.LONG)
        rows = {r["metric"]: r for r in style_profile.compare(ref, dr)}
        self.assertEqual(rows["sent_mean"]["flag"], "HIGH")
        self.assertEqual(rows["short_sent_share"]["flag"], "LOW")
        same = {r["metric"]: r["flag"] for r in style_profile.compare(ref, ref)}
        self.assertTrue(all(f == "OK" for f in same.values()))

    def test_cli_profile_and_compare(self):
        ref_dir = self.tmp / "styles" / "x"
        self.write("styles/x/a.txt", self.SHORT)
        self.write("styles/x/README.md", "ignored")
        draft = self.write("d.md", "# T\n\n" + self.LONG)
        out = self.tmp / "stats.json"
        code, stdout, _ = run_cli(style_profile.main, ["profile", str(ref_dir), "--out", str(out)])
        self.assertEqual(code, 0)
        self.assertIn("sent_mean", json.loads(out.read_text())["metrics"])
        code, stdout, _ = run_cli(style_profile.main, ["compare", "--reference", str(ref_dir), "--draft", str(draft)])
        self.assertEqual(code, 0)
        self.assertIn("sent_mean", stdout)
        self.assertIn("HIGH", stdout)

    def test_missing_excerpts_is_a_clean_error(self):
        code, _, err = run_cli(style_profile.main, ["profile", str(self.tmp / "empty")])
        self.assertEqual(code, 2)
        self.assertIn("no .txt/.md excerpts", err)


class TestStyleProfileDialogue(TmpCase):
    DIALOGUE = (
        "HELLO THERE FRIEND HOW ARE YOU\n"
        "Shut up, Meg\n"
        "I like eating red carpet\n"
        "No, you shut up, Meg\n"
    ) * 30

    def test_lines_are_utterances_and_share_is_one(self):
        s = style_profile.compute(self.DIALOGUE, as_dialogue=True)
        self.assertTrue(s["dialogue"])
        self.assertEqual(s["metrics"]["dialogue_share"], 1.0)
        self.assertEqual(s["sentences"], 120)
        self.assertGreater(s["metrics"]["sent_mean"], 3)
        self.assertLess(s["metrics"]["sent_mean"], 7)

    def test_default_mode_is_unchanged(self):
        t = '"Hello there my friend." He nodded and walked away from the door slowly.'
        s = style_profile.compute(t)
        self.assertFalse(s["dialogue"])
        self.assertGreater(s["metrics"]["dialogue_share"], 0.3)

    def test_cli_dialogue_profile_and_compare(self):
        ref_dir = self.tmp / "styles" / "family-guy"
        self.write("styles/family-guy/excerpt.txt", self.DIALOGUE)
        out = self.tmp / "stats.json"
        code, stdout, _ = run_cli(style_profile.main,
                                  ["profile", str(ref_dir), "--dialogue", "--out", str(out)])
        self.assertEqual(code, 0)
        self.assertIn("Dialogue mode", stdout)
        self.assertEqual(json.loads(out.read_text())["metrics"]["dialogue_share"], 1.0)
        draft = self.write("d.md", "# T\n\n" + self.SHORT)
        code, stdout, _ = run_cli(style_profile.main, [
            "compare", "--reference", str(ref_dir), "--draft", str(draft), "--dialogue"])
        self.assertEqual(code, 0)
        self.assertIn("dialogue mode", stdout)

    SHORT = "He ran. She hid. They waited. The rain fell. Nobody spoke. It ended. " * 60


class TestLockCheck(TmpCase):
    def test_check_ok_missing_unmarked(self):
        old = "One.\n\n<!-- KEEP -->Two stays.<!-- /KEEP -->\n\nThree."
        ok = "One!\n\n<!-- KEEP -->Two stays.<!-- /KEEP -->\n\nThree changed."
        gone = "One.\n\nThree."
        unmarked = "One.\n\nTwo stays.\n\nThree."
        self.assertEqual(lock_check.check(old, ok), ([], []))
        self.assertEqual(lock_check.check(old, gone)[0], ["Two stays."])
        self.assertEqual(lock_check.check(old, unmarked)[1], ["Two stays."])

    def test_check_tolerates_whitespace_reflow(self):
        old = "<!-- KEEP -->Two\nstays here.<!-- /KEEP -->"
        new = "<!-- KEEP -->Two stays\nhere.<!-- /KEEP -->"
        self.assertEqual(lock_check.check(old, new), ([], []))

    def test_apply_exact_ellipsis_and_not_found(self):
        notes = '## Keep\n- "counted the jars twice"\n- "Her brother came ... missing jar."\n- "text that is not there"\n- no quote here\n'
        out, res = lock_check.apply_keeps(STORY, notes)
        status = {q: s for s, q in res}
        self.assertEqual(status["counted the jars twice"], "LOCKED")
        self.assertEqual(status["Her brother came ... missing jar."], "LOCKED")
        self.assertEqual(status["text that is not there"], "NOT_FOUND")
        self.assertEqual(status["no quote here"], "NO_QUOTE")
        blocks = [mdutil.norm_ws(b) for b in mdutil.keep_blocks(out)]
        self.assertIn("counted the jars twice", blocks)
        self.assertTrue(any(b.startswith("Her brother came") and b.endswith("missing jar.") for b in blocks))
        self.assertEqual(mdutil.clean(out).split(), STORY.split())

    def test_apply_ambiguous_and_idempotent(self):
        text = "The jar. Later, the jar again."
        _, res = lock_check.apply_keeps(text, '## Keep\n- "the jar"\n')
        self.assertEqual(res[0][0], "AMBIGUOUS")
        once, _ = lock_check.apply_keeps(STORY, '## Keep\n- "counted the jars twice"\n')
        twice, res2 = lock_check.apply_keeps(once, '## Keep\n- "counted the jars twice"\n')
        self.assertEqual(once, twice)
        self.assertEqual(res2[0][0], "ALREADY_LOCKED")

    def test_apply_curly_quotes(self):
        _, res = lock_check.apply_keeps(STORY, "## Keep\n- “counted the jars twice”\n")
        self.assertEqual(res[0][0], "LOCKED")

    def test_adopt_locks_changed_and_new_paragraphs_only(self):
        edited = STORY.replace("The lamp guttered.", "The lamp guttered and died.") + "\nA new last paragraph by the human.\n"
        out, n = lock_check.adopt(STORY, edited)
        self.assertEqual(n, 2)
        blocks = [mdutil.norm_ws(b) for b in mdutil.keep_blocks(out)]
        self.assertTrue(any("guttered and died" in b for b in blocks))
        self.assertTrue(any("new last paragraph" in b for b in blocks))
        self.assertFalse(any(b.startswith('"Forty,"') for b in blocks))
        self.assertIn("# The Ledger", out)

    def test_diff(self):
        new = STORY.replace("The lamp guttered.", "The lamp guttered and died.")
        d = lock_check.diff(STORY, new)
        self.assertEqual(d["new_or_changed_ids"], [1])
        self.assertEqual(d["unchanged"], d["new_paragraphs"] - 1)

    def test_cli_flow(self):
        draft = self.write("drafts/draft_v1.md", STORY)
        notes = self.write("notes.md", '## Keep\n- "counted the jars twice"\n- "nope nope"\n')
        locked = self.tmp / "drafts" / "draft_v1.locked.md"
        code, out, _ = run_cli(lock_check.main, ["apply", "--draft", str(draft), "--notes", str(notes), "--out", str(locked)])
        self.assertEqual(code, 1)
        self.assertIn("NOT_FOUND", out)
        self.assertTrue(locked.is_file())
        good = self.write("drafts/draft_v2.md", STORY.replace("The lamp guttered.", "The lamp died.").replace(
            "counted the jars twice", "<!-- KEEP -->counted the jars twice<!-- /KEEP -->"))
        self.assertEqual(run_cli(lock_check.main, ["check", "--old", str(locked), "--new", str(good)])[0], 0)
        bad = self.write("drafts/draft_v3.md", STORY.replace("counted the jars twice", "counted jars"))
        code, out, _ = run_cli(lock_check.main, ["check", "--old", str(locked), "--new", str(bad)])
        self.assertEqual(code, 1)
        self.assertIn("MISSING", out)
        code, out, _ = run_cli(lock_check.main, ["list", str(locked)])
        self.assertIn("1 locked block", out)


class TestRunStatus(TmpCase):
    def make_run(self):
        run = self.tmp / "runs" / "r1"
        run.mkdir(parents=True)
        (run / "brief.md").write_text("# Brief", encoding="utf-8")
        return run

    def touch(self, run, *names):
        for n in names:
            p = run / n
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("x", encoding="utf-8")

    def test_progression(self):
        run = self.make_run()
        s = run_status.status(run)
        self.assertEqual(s["todo"], ["research", "style_profile"])
        self.touch(run, "01_spec.md", "01_questions.md")
        self.assertEqual(run_status.status(run)["todo"], ["style_profile"])
        self.touch(run, "05_style_profile.md")
        self.assertEqual(run_status.status(run)["stage"], "premises")
        self.touch(run, "02_premises.md")
        self.assertEqual(run_status.status(run)["stage"], "premise_choice")
        self.touch(run, "03_premise_choice.md")
        self.assertEqual(run_status.status(run)["stage"], "outline")
        self.touch(run, "04_outline.md")
        self.assertEqual(run_status.status(run)["stage"], "draft")
        self.touch(run, "drafts/draft_v1.md", "drafts/draft_v1.locked.md")
        s = run_status.status(run)
        self.assertEqual((s["round"], s["stage"]), (1, "numbered"))
        self.touch(run, "reviews/v1/numbered.md")
        self.assertEqual(run_status.status(run)["todo"], ["cold_read", "style_review", "lint", "accuracy"])
        self.touch(run, "reviews/v1/cold_read.md", "reviews/v1/lint.md")
        self.assertEqual(run_status.status(run)["todo"], ["style_review", "accuracy", "grade"])
        self.touch(run, "reviews/v1/style.md", "reviews/v1/accuracy.md", "reviews/v1/comprehension.md")
        self.assertEqual(run_status.status(run)["stage"], "digest")
        self.touch(run, "reviews/v1/digest.md")
        self.assertEqual(run_status.status(run)["stage"], "await_human")

    def test_notes_trigger_revise_and_draft_v2_resets(self):
        run = self.make_run()
        self.touch(run, "01_spec.md", "01_questions.md", "05_style_profile.md", "02_premises.md",
                   "03_premise_choice.md", "04_outline.md", "drafts/draft_v1.md")
        for f in ("numbered", "cold_read", "style", "lint", "accuracy", "comprehension", "digest"):
            self.touch(run, f"reviews/v1/{f}.md")
        (run / "notes.md").write_text("## Change\n- tighten scene 2\n", encoding="utf-8")
        s = run_status.status(run)
        self.assertTrue(s["notes_pending"])
        self.assertEqual(s["stage"], "revise")
        self.touch(run, "drafts/draft_v2.md")
        (run / "notes.md").write_text("## Change\n<!-- nothing -->\n", encoding="utf-8")
        s = run_status.status(run)
        self.assertEqual((s["round"], s["stage"]), (2, "numbered"))

    def test_archive_plan_forces_replan_and_refuses_duplicates(self):
        run = self.make_run()
        self.touch(run, "01_spec.md", "01_questions.md", "05_style_profile.md", "02_premises.md",
                   "03_premise_choice.md", "04_outline.md")
        moved = run_status.archive_plan(run, "round_1")
        self.assertEqual(len(moved), 3)
        self.assertTrue((run / "plans_archive" / "round_1" / "04_outline.md").is_file())
        self.assertEqual(run_status.status(run)["stage"], "premises")
        with self.assertRaises(FileExistsError):
            run_status.archive_plan(run, "round_1")

    def test_ignores_non_canonical_draft_names(self):
        run = self.make_run()
        self.touch(run, "drafts/draft_v1.md", "drafts/draft_v7.locked.md", "drafts/draft_v9.edited.md", "drafts/draft_v2.changes.md")
        self.assertEqual(run_status.latest_draft(run), 1)

    def test_latest_and_cli(self):
        runs = self.tmp / "runs"
        a = runs / "a"
        b = runs / "b"
        a.mkdir(parents=True)
        b.mkdir(parents=True)
        (a / "brief.md").write_text("x")
        (b / "brief.md").write_text("x")
        import os
        os.utime(a / "brief.md", (1, 1))
        self.assertEqual(run_status.latest_run(runs).name, "b")
        code, out, _ = run_cli(run_status.main, ["latest", "--runs-dir", str(runs)])
        self.assertEqual(code, 0)
        self.assertEqual(Path(out.strip()).name, "b")
        code, out, _ = run_cli(run_status.main, ["status", str(b)])
        self.assertEqual(json.loads(out)["stage"], "research")
        self.assertEqual(run_cli(run_status.main, ["status", str(self.tmp / "none")])[0], 2)
        self.assertEqual(run_cli(run_status.main, ["latest", "--runs-dir", str(self.tmp / "empty")])[0], 1)


class TestNewRunAndNotes(TmpCase):
    def test_create_run_and_collision(self):
        styles = self.tmp / "styles"
        (styles / "terry-pratchett").mkdir(parents=True)
        (styles / "terry-pratchett" / "a.txt").write_text("text", encoding="utf-8")
        info = new_run.create_run("Python asyncio event loop", "Terry Pratchett", self.tmp / "runs", styles, today="2026-10-08")
        run = Path(info["run_dir"])
        self.assertEqual(info["style_slug"], "terry-pratchett")
        self.assertEqual(info["excerpt_files"], 1)
        brief = (run / "brief.md").read_text(encoding="utf-8")
        self.assertIn("Python asyncio event loop", brief)
        self.assertIn("styles/terry-pratchett/", brief)
        self.assertNotIn("{", brief)
        for sub in ("drafts", "reviews", "notes_history", "scratch"):
            self.assertTrue((run / sub).is_dir())
        self.assertIn("responding to draft v1", (run / "notes.md").read_text(encoding="utf-8"))
        again = new_run.create_run("Python asyncio event loop", "Terry Pratchett", self.tmp / "runs", styles, today="2026-10-08")
        self.assertNotEqual(again["run_dir"], info["run_dir"])
        self.assertTrue(again["run_dir"].endswith("-2"))
        none = new_run.create_run("X", "Unknown Author", self.tmp / "runs", styles, today="2026-10-08")
        self.assertEqual(none["excerpt_files"], 0)

    def test_fresh_run_is_in_the_expected_first_stage(self):
        info = new_run.create_run("X", "Y", self.tmp / "runs", self.tmp / "styles", today="2026-10-08")
        s = run_status.status(info["run_dir"])
        self.assertEqual(s["todo"], ["research", "style_profile"])
        self.assertFalse(s["notes_pending"])

    def test_archive_notes(self):
        run = self.tmp / "run"
        run.mkdir()
        self.assertIsNone(archive_notes.archive(run, 1))
        (run / "notes.md").write_text("## Change\n- fix [P2]\n", encoding="utf-8")
        dest = archive_notes.archive(run, 1)
        self.assertEqual(dest.name, "round_1.md")
        self.assertIn("fix [P2]", dest.read_text(encoding="utf-8"))
        fresh = (run / "notes.md").read_text(encoding="utf-8")
        self.assertIn("responding to draft v2", fresh)
        self.assertFalse(any(mdutil.parse_notes(fresh).values()))
        self.assertIsNone(archive_notes.archive(run, 2))

    def test_notes_digest(self):
        for name, bullet in (("r1", "drier dialogue in scene two"), ("r2", "make dialogue drier and shorter")):
            d = self.tmp / "runs" / name
            d.mkdir(parents=True)
            (d / "notes.md").write_text(f"## Change\n- {bullet}\n", encoding="utf-8")
        data = notes_digest.collect(self.tmp / "runs")
        self.assertEqual(data["runs"], 2)
        terms = dict(notes_digest.top_terms(data["sections"]["change"], 10))
        self.assertEqual(terms.get("dialogue"), 2)
        self.assertEqual(terms.get("drier"), 2)
        self.assertIn("Recurring terms", notes_digest.render(data, 10))


if __name__ == "__main__":
    unittest.main()
