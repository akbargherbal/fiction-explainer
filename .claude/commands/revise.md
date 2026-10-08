---
description: Run the next fiction-explainer round from your notes.md (Keep / Change / Pivot / Reject / Overrule)
argument-hint: [run-slug]
---

You are the orchestrator of the fiction-explainer pipeline.

1. Read `PIPELINE.md` and `AGENTS.md` in full.
2. Execute **Procedure V (Revision)**, which ends with **Procedure R (Review wave)**, exactly as written.

Run to revise (empty means the latest run, from `python tools/run_status.py latest`):

$ARGUMENTS

Reminders:
- Accuracy blockers are always fixed unless the notes Overrule them.
- If any Keep quote could not be matched, say which ones in your final report so the human can fix the quote.
- At revision round 3 or later, recommend a Pivot or stopping, as `PIPELINE.md` says.
- Do not write story prose yourself; dispatch the `writer`.
