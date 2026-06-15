---
name: pip-dashboard
description: >
  PIP · Dashboard — generate and open the visual learning dashboard (concepts grouped by project
  and by tech stack, with scores and provenance). Use when the user says "pip dashboard",
  "open the dashboard", "show my stacks", or "show the map". Part of PIP, the learning layer for
  AI-assisted development. Do NOT trigger for the Python package installer — unrelated tool.
metadata:
  version: "0.13.0"
---

# PIP · Dashboard

**Read `${CLAUDE_PLUGIN_ROOT}/shared/core.md` first** — shared rules.

Generate and open the dashboard from the global store:
1. Ensure `~/.pip/state.json` is current (it is, if `pip-learn` has been updating it).
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/render_dashboard.py --open` — it injects the store into the self-contained template (`assets/dashboard.html`) and writes `~/.pip/dashboard.html`, then opens it.
3. No store yet → it renders with template demo data; tell the user it fills in as they learn.

The dashboard opens on a **How to use PIP** panel; the sidebar has two collapsible sections — **Projects** (concepts learned building each) and **Stacks** (each stack's **full concept tree** — everything needed to master it, done and not-done). Nodes show status + score; click one for which project(s) taught it, per-project + aggregate scores, prerequisites, and a "Mark as mastered" action. Full spec in `shared/dashboard.md`.
