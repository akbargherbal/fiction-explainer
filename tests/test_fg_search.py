"""Tests for tools/fg_search.py. Run: python -m unittest discover -s tests -v"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import fg_search  # noqa: E402

RESULTS = [{"season": 5, "episode": 12, "start": 434.0, "end": 436.0,
            "cue_from": 0, "cue_to": 6, "chunk_id": 7, "text": "PETER: I did not do this."}]

GOOD_STUB = textwrap.dedent(
    """\
    import json, sys
    print(json.dumps(%s))
    """
) % (json.dumps(RESULTS),)

ABORT_STUB = textwrap.dedent(
    """\
    import sys
    print("aborted", file=sys.stderr)
    sys.exit(1)
    """
)


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

    def stub(self, name, body):
        d = self.tmp / name
        d.mkdir(parents=True)
        (d / "search.py").write_text(body, encoding="utf-8")
        return d


class TestArgv(unittest.TestCase):
    def test_mode_mapping_and_flags(self):
        fg = Path("/fg")
        self.assertEqual(fg_search.build_fg_argv(fg, "literal", "giggity", 20, None, None, False, False, False, False)[1:],
                         ["/fg/search.py", "--exact", "giggity", "--json", "--limit", "20"])
        regex = fg_search.build_fg_argv(fg, "regex", "\\(weakly\\)", 5, 1, 2, True, False, True, False)
        self.assertIn("--regex", regex)
        self.assertIn("-i", regex)
        self.assertIn("--no-dedupe", regex)
        self.assertIn("--season", regex)
        semantic = fg_search.build_fg_argv(fg, "semantic", "a scene", 3, None, None, False, True, False, False)
        self.assertIn("--semantic", semantic)
        self.assertIn("--yes", semantic)
        self.assertNotIn("--yes", fg_search.build_fg_argv(fg, "semantic", "x", 3, None, None, False, False, False, False))

    def test_slugify(self):
        self.assertEqual(fg_search.slugify("Peter does something foolish!"), "peter-does-something-foolish")
        self.assertEqual(fg_search.slugify("!!!"), "query")


class TestRunSearch(TmpCase):
    def test_returns_results(self):
        fg = self.stub("good", GOOD_STUB)
        results, _ = fg_search.run_search(fg, "literal", "giggity", limit=5)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["season"], 5)

    def test_missing_script_is_clean_error(self):
        with self.assertRaises(FileNotFoundError):
            fg_search.run_search(self.tmp / "nope", "literal", "x")

    def test_declined_download_is_explained(self):
        fg = self.stub("abort", ABORT_STUB)
        with self.assertRaises(RuntimeError) as cm:
            fg_search.run_search(fg, "semantic", "x")
        self.assertIn("--yes", str(cm.exception))


class TestCli(TmpCase):
    def test_writes_hits_under_run_scratch_and_prints_summary(self):
        fg = self.stub("good", GOOD_STUB)
        run = self.tmp / "runs" / "r1"
        run.mkdir(parents=True)
        code, out, err = run_cli(fg_search.main, [
            "--fg-dir", str(fg), "--literal", "I did not do this", "--out", str(run)])
        self.assertEqual(code, 0)
        self.assertIn("S05E12", out)
        self.assertIn("07:14", out)
        hits = list((run / "scratch" / "fg_hits").glob("literal-*.json"))
        self.assertEqual(len(hits), 1)
        payload = json.loads(hits[0].read_text())
        self.assertEqual(payload["mode"], "literal")
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["season"], 5)

    def test_no_text_drops_cue_text(self):
        fg = self.stub("good", GOOD_STUB)
        run = self.tmp / "runs" / "r1"
        run.mkdir(parents=True)
        code, _, _ = run_cli(fg_search.main, [
            "--fg-dir", str(fg), "--literal", "x", "--out", str(run), "--no-text"])
        self.assertEqual(code, 0)
        hit = next((run / "scratch" / "fg_hits").glob("*.json"))
        self.assertNotIn("text", json.loads(hit.read_text())["results"][0])

    def test_missing_fg_dir_is_error_code_2(self):
        code, _, err = run_cli(fg_search.main, ["--fg-dir", str(self.tmp / "nope"), "--literal", "x"])
        self.assertEqual(code, 2)
        self.assertIn("no search.py", err)


if __name__ == "__main__":
    unittest.main()
