---
name: pip-status
description: >
  PIP · Status — restate the concept tree and where the user is, and (on request) emit a
  portable snapshot of their progress. Use when the user says "pip status", "where am I with pip",
  "show the tree", "pip save", or "save my progress". Part of PIP, the learning layer for
  AI-assisted development. Do NOT trigger for the Python package installer ("pip list",
  "pip freeze", "pip install") — unrelated tool.
metadata:
  version: "0.13.0"
---

# PIP · Status

**Read `${CLAUDE_PLUGIN_ROOT}/shared/core.md` first** — shared rules.

Read `.pip/progress.md`. Show the tree with statuses, the next un-mastered concept in prerequisite order, and a one-line "you are here." **Read-only — no teaching.**

If the user wants to keep or move their progress ("pip save" / "save my progress"), also emit a **paste-ready snapshot** — project · parts → concepts → statuses → where you stopped — that they can paste into another chat, notes, or hand off. (Progress already persists to `.pip/progress.md` on every checkpoint, so this is an *export*, not a save.)
