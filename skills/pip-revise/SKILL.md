---
name: pip-revise
description: >
  PIP · Revise — a quick, brief refresher on a concept the user already mastered, when it
  resurfaces in a new project. Use when the user says "pip revise X", "refresh me on X", or
  "quick refresher". Part of PIP, the learning layer for AI-assisted development. Do NOT trigger
  for the Python package installer ("pip install", "pip freeze", dependency errors) — unrelated tool.
metadata:
  version: "0.13.0"
---

# PIP · Revise

**Read `${CLAUDE_PLUGIN_ROOT}/shared/core.md` first** — shared rules.

Revise = **refresh** a concept the user already mastered — fast, not a re-teach.

1. Give a **brief** refresher — the core idea in two to four sentences, tied to where it shows up in the current code. No checkpoint by default.
2. Offer to **expand**: "want the full breakdown, or a checkpoint?" — only go deeper if the user asks (a fresh checkpoint runs through `pip-learn`).
3. A revise is **read-only** on scores: it never lowers an existing score. Only a fresh checkpoint the user opts into can change it.

This is the opposite of `pip-learn` — keep it short.
