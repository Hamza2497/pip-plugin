---
name: pip-import
description: >
  PIP · Import — backfill concepts from projects the user already built (a git repo OR a plain
  local folder) so the dashboard reflects real history. Use when the user says "pip import",
  "add my existing projects", or "backfill" a repo or folder path. Part of PIP, the learning layer for
  AI-assisted development. Do NOT trigger for the Python package installer that shares the name
  ("pip install", "pip uninstall", "pip freeze", "pip list", requirements/venv errors) — unrelated tool.
metadata:
  version: "0.13.0"
---

# PIP · Import

**Read `${CLAUDE_PLUGIN_ROOT}/shared/core.md` first** — shared rules (especially **Token efficiency**: this is the heaviest read PIP does).

Pull the concepts the user has *already* learned into the global store. For each project they point at — a **git repo or a plain local project folder** (one or several):

1. **Read it token-efficiently** — always go through the **cheap-model bulk pass** (core — Token efficiency): it triages the file tree and summarises the high-signal files into a compact candidate-concept list (`{concept, file:line, evidence}`); the host then dedups and **places each by the resolution order** (`shared/method.md`) under its **stack(s)**. Never have the host read the whole project. If it's a git repo, use `git log` too; a plain folder works from its files. For a big project, triage first and summarise only what carries real logic — don't ingest everything.
2. **Offer a short mastery quiz, run through `pip-quiz` (sampling intensity)** — a handful of quick questions sampling the project's important/representative concepts (not one per concept). The user can skip it.
3. **`pip-quiz` scores each sampled concept** (out of 10; mastered 9–10, passed 6–8) and records it. **Passing a concept passes its prerequisites transitively** — if they clearly use X and X depends on Y, mark Y mastered too (a fast, reasonable assumption; revisable later) as a `learnedIn` entry `{project, score, code, date}`.
4. Concepts neither quizzed nor inferred stay **learned-but-ungraded** (`✓`) — provenance only; never invent a score.
5. Regenerate the dashboard (`scripts/render_dashboard.py`).

The quiz is a fast confidence check, not a full checkpoint — any concept can be deepened later via `pip-learn`, or refreshed via `pip-revise`.
