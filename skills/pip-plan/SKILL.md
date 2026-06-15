---
name: pip-plan
description: >
  PIP · Plan — turn a project plan into a learning concept tree. Use when the user says
  "pip plan", "plan this with pip", "what do I need to learn here", or right after they finish
  planning a project and want the concepts to learn from it. Part of PIP, the learning layer for
  AI-assisted development — it teaches the concepts behind code and never writes production code.
  Do NOT trigger for the Python package installer that shares the name: "pip install" /
  "pip uninstall" / "pip freeze" / "pip list", requirements/venv/dependency errors are an
  unrelated tool, not PIP.
metadata:
  version: "0.13.0"
---

# PIP · Plan

**Read `${CLAUDE_PLUGIN_ROOT}/shared/core.md` first** — it carries the rules every PIP skill shares (the inviolable rule, the package-installer guard, how to ask/quiz via the popup, token efficiency, where PIP runs, the two stores, scoring tiers, voice).

PIP works alongside the user as they build. The flow, in order:

1. **Get the plan**, in priority order: **the plan already in this conversation** (just worked out here, or in the message that invoked PIP — use it directly, don't ask for a paste); a **plan file/doc** the user points at (`pip plan plan.md`, any `.md`/`.txt`, an issue); a **plan pasted** now; or — failing all — the **repo** itself (repo-awareness, step 6).
2. **Identify the stack(s)** the plan belongs to (e.g. Python · AI, .NET · Backend, Frontend · React, DevOps) from its tech.
3. **Ensure each stack's curriculum exists.** If a stack is new to the user, generate its **defensible full curriculum** — the standard concepts needed to master it — as the stack tree (`shared/method.md` — Stack curricula). If it already exists in the global store, reuse it; don't regenerate.
4. **Select the project's execution scope** = the concepts the project actually **builds** (relevant to it, including ones already mastered — those show green). The displayed **tree** is this scope **closed under prerequisites**: pull in the full prerequisite chain of every concept, even ones the project doesn't build, so every prerequisite stays **visible** and nothing is locked by a hidden prereq. A prerequisite can be in a project's tree without its dependents — never the reverse. Concepts in the tree but **outside the execution scope** are prerequisites the project doesn't build — `pip-learn` gives them a brief explanation + simple quiz, capped at 5 (a modest understanding), since they're required to *understand* what they lead to but aren't executed here.
5. **Split the plan into parts and attach each selected concept to its part** — the part of the plan where the concept is actually exercised. `.pip/progress.md` is grouped by part, and the part list is written to the project's **`parts`** field in the global store (ordered `{name, concepts}`) so the dashboard's right nav groups the learning plan + concept queue by part. **Harmony rule:** order parts so a concept's prerequisites fall in the **same or an earlier part**, never a later one — part order must agree with prerequisite order. Concepts are *ideas, not actions* ("how Alembic tracks the migration head", not "run `alembic upgrade`").
6. **Tie each concept to code** when a repo exists, using the host's own tools (no server): `Glob`/`Read` README, manifests (`pyproject.toml`, `*.csproj`…), entry points; sample real source; `Bash: git log --oneline -n 30`, `git log -p -n <k> -- <path>`. Record `path:line`/commit. For a large repo, route the bulk read through the **cheap-model bulk pass** (core — Token efficiency) and judge from its summary.
7. **Reconcile with the global store** using canonical naming + dedup-by-meaning (`shared/method.md` — Concept identity): an already-known concept stays one node, never a duplicate; prerequisites point backward only (cycle-free). Place any concept that needs a home by the **resolution order** — current stack → other stacks (reuse, make it shared) → a new node only after real scrutiny.
8. **Present the per-part tree; confirm before teaching.** Then the user builds a part; `pip-learn` teaches that part's concepts and scores them. **When a part is finished, run `pip-review` automatically** to catch concepts they actually used that the plan didn't anticipate. Status flows up: each concept turns green on both the project tree and the stack tree. **When the whole project wraps up, offer a `pip-quiz` wrap-up** across the concepts it taught.
