---
name: pip-mark
description: >
  PIP · Mark — assert mastery of a concept without a checkpoint, so PIP won't teach it. Use when
  the user says "pip mark X as mastered", "I already know X", or pastes a "pip mark mastered: …"
  line copied from the dashboard's sync banner. Part of PIP, the learning layer for AI-assisted
  development. Do NOT trigger for the Python package installer ("pip install", "pip freeze",
  dependency errors) — unrelated tool.
metadata:
  version: "0.13.0"
---

# PIP · Mark

**Read `${CLAUDE_PLUGIN_ROOT}/shared/core.md` first** — shared rules.

The user can assert mastery without a checkpoint — starting a stack they already know parts of, or confirming a mark made in the dashboard.

1. For each named concept **that isn't locked**, set `selfMastered: true` in the global store **and mark it complete in the per-repo `.pip/progress.md` tree**, and treat it as mastered. A locked concept can't be marked — its prerequisites aren't met yet; say which.
2. **Never teach a self-mastered concept** (treat like `known`); it counts as satisfied for unlocking dependents.
3. Regenerate the dashboard (`scripts/render_dashboard.py`). The mark now holds in **every chat**, because it lives in `~/.pip/state.json`. (The dashboard clears a copied mark from its sync banner immediately, so the user can mark several in a row — no reload needed.)

A self-mark carries no score; offer `pip-revise` or a checkpoint (`pip-learn`) if the user later wants a graded reading.
