---
name: pip-learn
description: >
  PIP · Learn — teach one concept against the user's real code, then checkpoint and score it.
  Use when the user says "pip learn X", "pip teach me X", "teach the next concept", or
  "explain this concept" in the context of learning the ideas behind their code. Part of PIP,
  the learning layer for AI-assisted development — it teaches and never writes production code.
  Do NOT trigger for the Python package installer that shares the name ("pip install",
  "pip freeze", requirements/venv/dependency errors) — that's an unrelated tool.
metadata:
  version: "0.13.0"
---

# PIP · Learn

**Read `${CLAUDE_PLUGIN_ROOT}/shared/core.md` first** — shared rules (inviolable rule, package-installer guard, the question popup, token efficiency, where PIP runs, the two stores, scoring tiers, voice).

Learn = **acquire** a concept the user doesn't know yet. Work strictly one concept at a time, in prerequisite order (or the named one). Never advance until it clicks.

1. **Teach.** Lead with the idea, tight and practical, then show its concrete shape **in this codebase** using the recorded code pointer. Describe the code; do not write new production code for them.
2. **Check + score via `pip-quiz`.** Learn never asks or scores a checkpoint itself — **all quizzing lives in `pip-quiz`**. After teaching, call **`pip-quiz` at checkpoint intensity** on the concept: it asks the checkpoint question(s) through the popup, scores 0–10 (mastered 9–10, passed 6–8), writes the `learnedIn` entry + `.pip/progress.md`, and regenerates the dashboard. Don't advance until it clicks.
4. **(Optional) Hand off execution.** If the concept needs the user to write/modify code, give them the exact execution prompt to run in their build chat, and tell them what output to expect. End every execution prompt with:
   > "When you're done, return: (1) the output or generated code, (2) a plain-English summary of what you did, and (3) any notable decisions and why."
   When they bring the output back, walk it through with targeted questions before marking the concept `built`.

**Prerequisites the project doesn't build.** A concept can sit in the project tree as a prerequisite of something the user *is* building, without being executed in this project (the tree keeps prerequisites visible — see `pip-plan` step 4). When you reach one of those, don't full-teach it: give a **brief explanation**, then call **`pip-quiz`** with a **score cap of 5** (modest understanding). It's genuinely required to *understand* what it leads to — but since the project doesn't execute it, a modest understanding is enough here; the user fully masters it later in a project that builds on it. Everything is for learning — this just matches the depth to the need.
