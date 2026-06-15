---
name: pip-review
description: >
  PIP · Review — after a project step is built, reconcile the concept tree with the code:
  discover concepts the user actually used but didn't plan, fold them in, and confirm the step's
  concepts are covered. Use when the user says "pip review" / "review this step", and run it
  automatically after each step of a project. Part of PIP, the learning layer for AI-assisted
  development. Do NOT trigger for the Python package installer ("pip install", "pip freeze",
  dependency errors) — that's an unrelated tool.
metadata:
  version: "0.13.0"
---

# PIP · Review

**Read `${CLAUDE_PLUGIN_ROOT}/shared/core.md` first** — shared rules.

Review = **reconcile** the tree with reality after a step. Two jobs: confirm what was planned, and catch what wasn't. It is **not** a second teaching mode — it *finds and places* concepts and hands the teaching to `pip-learn`.

1. **See what was built.** Read the code the user actually wrote for this step (repo-awareness — `git diff` since the last step, the part's files). Route a large diff through the **cheap-model bulk pass** (core — Token efficiency).
2. **Catch emergent concepts.** Find concepts the code demonstrates that **weren't in the project tree** — things that came up while building that the plan didn't anticipate. Apply canonical naming + dedup-by-meaning so an emergent concept that already exists under another name isn't duplicated (`shared/method.md` — Concept identity).
3. **For each emergent concept, place it by the resolution order** (`shared/method.md` — Placing a concept) — these nodes follow the *same* generation rules as every other node; they must be real concepts in the stack curricula, not ad-hoc additions:
   a. **Already in the current stack's curriculum?** (match by meaning) — use that node; just attach the user's `learnedIn`.
   b. **In another stack's curriculum?** It's the *same* concept — add the current stack to its `stacks` array (it becomes shared/multi-stack) and reuse it; never create a duplicate.
   c. **In no stack?** Only then consider a new node, and **scrutinise first**: dedup-by-meaning across the whole registry (it may exist under another name), and confirm it's a standard, defensible concept for the stack. If it's a one-off, a tool/command, or noise, don't add it — don't grow stacks carelessly.
   Then hand off to **`pip-learn`** to teach it (using the user's own code as the example); Learn calls **`pip-quiz`** to check + score. Review *finds and places*; Learn *teaches*; `pip-quiz` *scores*.
4. **Confirm the planned concepts** of the step are checkpointed; hand any skipped ones to `pip-learn`.
5. Regenerate the dashboard — the new nodes appear in the project tree and their stack, and the step's concepts recolor.

This is what keeps the tree honest to what was *actually built*, not just what was planned.
