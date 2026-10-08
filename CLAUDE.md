@AGENTS.md

# Claude Code specifics

- Subagents live in `.claude/agents/` and are invoked **by name** with the Agent/Task tool. Slash commands: `/explain` (full run) and `/revise` (next round after you write `notes.md`).
- You are the **orchestrator** in the main session. Follow [PIPELINE.md](PIPELINE.md) exactly. Do not write story prose, spec content or reviews yourself; dispatch the role that owns it.
- Keep the main context light: pass **paths**, not contents, to subagents, and use `python tools/run_status.py status <run>` instead of re-reading files to find out what is next.
- Dispatch independent steps **in a single message with multiple Agent calls** so they run in parallel (the review wave and the research + style-profile wave).
- After every dispatch, verify the expected output file exists. Retry once with the failure noted; on a second failure stop and tell the human what is missing.
- Run Python tools as `python tools/<name>.py ...` from the repo root. If your system only has `python3`, substitute it.
