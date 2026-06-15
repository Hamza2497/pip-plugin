---
name: pip-quiz
description: >
  PIP · Quiz — assess the user's understanding of concepts they've already learned, score it, and
  help them close the gaps it reveals. Use when the user says "pip quiz", "quiz me on X",
  "test me on X", or "quiz me on this project" (a wrap-up at the end of a project). Part of PIP,
  the learning layer for AI-assisted development — it tests, re-scores, and points at targeted
  practice; it does not teach from scratch. Do NOT trigger for the Python package installer
  ("pip install" / "pip freeze" / "pip list", requirements/venv/dependency errors) — unrelated tool.
metadata:
  version: "0.14.0"
---

# PIP · Quiz

**Read `${CLAUDE_PLUGIN_ROOT}/shared/core.md` first** — shared rules, especially **Asking the user** and **Quizzes & rescoring**.

Quiz = **assess**. It rigorously tests a concept and writes the result back to the score. It does **not** teach a concept from scratch (that's `pip-learn`), does not discover concepts (`pip-review`), does not self-assert (`pip-mark`), and — unlike `pip-revise` — it can move the score (upward).

## The only place quizzing happens

Every quiz and checkpoint in PIP runs through this skill. `pip-learn`, `pip-review`, and `pip-import` **call `pip-quiz`** rather than asking questions themselves, and the user can call it directly. Callers pick an **intensity**:
- **checkpoint** — from `pip-learn` right after teaching (and `pip-review` via Learn): one question (or two) to set a just-taught concept's first score.
- **sampling** — from `pip-import`: a few questions across many concepts to set initial scores.
- **focused** — the user's "quiz me on X": a full multi-facet quiz on one already-learned concept.
- **wrap-up** — project end: across the project's taught concepts.

**First assessment vs re-assessment:** a checkpoint / sampling / first quiz of a concept *sets* its score. A later quiz of an already-scored concept is **re-assessment** — improvement-first (raise, never lower the displayed score; record `gaps` + `recheck`; see *Quizzes & rescoring* in core).

## Two modes

- **Single concept** — "quiz me on X": a focused quiz on one concept.
- **Project wrap-up** — "quiz me on this project" (offer it when a project wraps up): quiz across the concepts the project **taught** (its `learnedIn` for this project); each concept scored on its own. Capped prerequisites stay capped — a quiz doesn't build them.

**Don't quiz the truly unknown.** Quiz concepts being learned (checkpoint, called by Learn) or already learned (focused/wrap-up). If the *user* asks to quiz a concept they've never encountered, route to `pip-learn` to teach it first — testing-out an unknown concept belongs to `pip-import` / `pip-mark`, not here.

## The quiz (per concept, to the Quiz standard in core)

1. **Generate** questions across **distinct facets** — the *why*, an edge case, a trade-off, a failure mode — grounded in the user's own code (the concept's code pointer). For a wrap-up over a big codebase, route the bulk read through the **cheap-model bulk pass** (core — Token efficiency).
2. **Ask** each through the **popup** (hard multiple-choice + ≥1 "in your own words"); never repeat a logged question; escalate difficulty if the concept was previously unmastered or carries a `recheck` flag (and aim those questions at its recorded `gaps`).
3. **Give diagnostic feedback** on wrong picks (the misconception → the right idea) — but do **not** full-teach here.

## Score, then act (per *Quizzes & rescoring* in core)

- Map the answers to a holistic **0–10** (9–10 nails it incl. edges/trade-offs · 6–8 solid with a gap · ≤5 missed key facets) — same rubric as a checkpoint.
- **Improvement raises** the concept's score. A **weaker** result **never lowers** the displayed score.
- **When it comes out weaker, recognise *what* they're short on and help them fix it — don't just flag:**
  - Record the specific weak facets as the concept's **`gaps`**, set `recheck: true`, bump `difficulty`.
  - **Offer targeted practice on exactly those facets** — a focused `pip-learn` (re-teach just the weak facet against their code) or `pip-revise` — then re-quiz those; a clean re-demonstration raises the score and clears the matching `gaps`.
- Regenerate the dashboard. A multi-concept quiz writes one score per concept (no cross-concept averaging).

## Close with a real readout

Summarise: what's **solid**, what's **shaky and exactly why** (the specific facet/misconception, not "you failed"), and a direct offer to work the weak ones now via targeted `pip-learn` / `pip-revise`. The job isn't to grade — it's to surface gaps and help close them.
