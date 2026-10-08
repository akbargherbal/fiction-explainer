---
description: Run the full fiction-explainer pipeline for a concept in a given style
argument-hint: <concept> | <style or author> [--length N] [--form "..."] [--audience "..."] [--review-plan] [--resume run]
---

You are the orchestrator of the fiction-explainer pipeline.

1. Read `PIPELINE.md` and `AGENTS.md` in full.
2. Execute **Procedure A (Initial run)**, then **Procedure R (Review wave)**, exactly as written, with these arguments:

$ARGUMENTS

Reminders:
- Do not write story prose, spec content or reviews yourself; dispatch the owning agent.
- Pass file paths, not contents, to agents. Dispatch independent steps in parallel.
- Ask the human at most one short question, and only if the concept or the style is missing.
- When finished, report as Procedure A4 says: where the draft and digest are, the headline numbers, and the next step.
