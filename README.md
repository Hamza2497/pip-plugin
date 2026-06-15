# PIP — the learning layer for AI-assisted development

> AI writes the code, you ship it, but you never actually learned it — so you freeze when an interviewer asks *"why did you do it this way?"* PIP fixes that.

PIP is a Claude plugin that rides along while you build. It reads your **real repo and git history**, builds a prerequisite-ordered tree of the **concepts** behind the code that actually exists, then teaches, checkpoints, and **grades** those concepts one at a time — and renders a dashboard of everything you've learned, sliced by project and by tech stack. PIP never writes your production code; it teaches the ideas so every line on your CV is one you can defend.

This is PIP rebuilt as a plugin. The original was a hosted web app (FastAPI · Postgres · pgvector · a React canvas) that had to *ask you to describe* your project. As a plugin it lives in the session where you actually code, so it reads the code directly — and needs no server, no database, and no API key.

---

## The problem it solves

When an agent writes most of the code, comprehension silently falls behind delivery. You can ship a feature without being able to explain the dependency-injection container, the SSE stream, or why the migration runs the way it does. PIP closes that gap by turning the code you ship into a graded, defensible curriculum — in the same order you build it.

## How it works (the loop)

1. **Plan** — give PIP your project plan (or let it read the repo). It maps the plan onto the concepts you'll learn and splits them across the plan's parts.
2. **Build** — you build a part with your AI coding tool as usual.
3. **Learn** — PIP teaches each concept in that part *against your actual code*, then checkpoints and scores it.
4. **Review** — after each part, PIP reconciles the tree with what you really built and folds in concepts you used but didn't plan.
5. **Quiz** — at any point (and at project wrap-up) PIP rigorously tests what you've learned, raising scores as you improve and pinpointing exactly what's still shaky.

Everything flows into a single dashboard so you can see, per concept, how well you can defend it.

## Install

**Cowork** — install the `.plugin` from Settings → Capabilities (or the install card), and you're done.

**Claude Code** — add the plugin directory as a local plugin; the skills auto-register.

No setup, no environment variables, no keys. PIP creates two small state files on first use (see [State](#state)).

## The skills

PIP is a set of skills. Trigger one by typing `/` and picking it (e.g. `/pip-learn`) or just by saying what you want — the matching skill fires on its own. They're chat messages, never the Python `pip` package installer.

| Skill | Say this | What it does |
|---|---|---|
| `/pip-plan` | "plan this with pip", "what do I need to learn here" | Splits your plan into parts and attaches the concepts you'll learn to each. No plan? It reads the repo + `git log` and infers one. |
| `/pip-learn` | "teach me the next concept" | Teaches one concept against your real code, then hands off to `pip-quiz` for a checkpoint that scores how well you explained it. |
| `/pip-quiz` | "quiz me on X", "quiz me on this project" | The single place all quizzing happens. Rigorous; raises your score on improvement, never lowers it; pinpoints weak facets and gives targeted practice. |
| `/pip-review` | "review this step" (auto after each part) | Catches concepts you used that the plan didn't anticipate, explains them with your own code, adds them to the tree, and gets them quizzed. |
| `/pip-revise` | "refresh me on X" | A quick refresher on a concept you already know — brief by default, expandable. Never lowers a grade. |
| `/pip-import` | "add my existing projects" | Backfills concepts from a repo **or a plain local folder** you've already built (see [the bulk-reader](#token-efficiency--the-bulk-reader-subagent)). |
| `/pip-mark` | "I already know X" | Asserts mastery without a checkpoint, so PIP won't teach it. The dashboard's "Mark as mastered" button feeds this. |
| `/pip-status` | "where am I", "save my progress" | Restates the tree and the next concept to learn; can print a portable progress snapshot you can paste anywhere. |
| `/pip-dashboard` | "open the dashboard", "show my stacks" | Generates and opens the visual dashboard from your latest progress. |

## Quizzing & grading

All quizzing is centralized in **`pip-quiz`** — the other skills call it rather than asking questions themselves, at one of four intensities: **checkpoint** (one question, from Learn), **sampling** (a few across many concepts, from Import), **focused** (a full multi-facet quiz on one concept), and **wrap-up** (across a whole project).

- **Real questions, real format.** Every question is asked through Claude's interactive popup — harder multiple-choice plus at least one open-ended "in your own words" prompt. Wrong multiple-choice picks are *diagnostic*: PIP works back from the specific misconception you chose to the right idea.
- **Scored out of 10** — mastered 9–10, passed 6–8, in-progress ≤5.
- **Improvement-first rescoring.** A later quiz can **raise** a score; a weaker showing **never lowers** the displayed score. Instead it records the exact weak facets as the concept's `gaps`, flags it for re-check in a later project, and offers targeted practice on just those facets.
- **No repeats, escalating difficulty.** Every question is logged per concept and never re-asked; a concept you haven't mastered gets harder questions each time it resurfaces.

## The concept model

- **Stacks & projects.** Concepts belong to one or more **stacks** (e.g. "Python · AI Engineering", ".NET · Backend"). A **project** has an execution scope — the concepts it actually builds.
- **Prerequisite closure.** A project's tree always pulls in the prerequisites of everything it builds, even ones the project doesn't itself build, so nothing is locked by a hidden prereq. Prereqs the project doesn't execute are quizzed lightly and capped at "modest understanding" until you master them in a project that uses them.
- **Cross-stack sharing, no duplicates.** A concept used by several stacks (e.g. dependency injection) is stored once and shown in each — canonical naming and dedup-by-meaning keep the graph clean.
- **Plan parts.** `pip-plan` splits your plan into ordered build phases and attaches concepts to each. The dashboard groups your learning plan by these parts, **harmonized** with prerequisite order so a concept's prerequisites never sit in a later part than the concept itself.
- **Learning is commutative.** A concept's score reflects how well you understand it, regardless of which project taught it.

## Token efficiency — the bulk-reader subagent

PIP keeps the expensive, strong model for **judgment** (concept identity, dedup, teaching, question design, scoring) and pushes **bulk reading** to a cheap, Haiku-class **subagent** spun up through the host. The subagent reads what it's told to and returns a **compact, structured summary** — `{concept, file:line, evidence}` lines, a short repo inventory, or a diff scan — never raw file dumps. The strong model then judges that summary.

This delegation runs wherever PIP would otherwise read a lot:

- **`pip-import`** — the heaviest read PIP does. The subagent triages a finished repo or folder's file tree and summarizes only the high-signal files into a candidate-concept list; the strong model dedups and places each concept by the resolution order, then offers a short sampling quiz to set real grades. The host never reads the whole project.
- **`pip-plan`** — when inferring a plan from a large repo.
- **`pip-review`** — scanning a large diff after a build step.
- **`pip-quiz`** — a wrap-up over a big codebase.

The result: PIP stays cheap on big projects, and the strong model spends its tokens on understanding, not on wading through files.

## State

Two plain-text stores, no database:

- **`.pip/progress.md`** — per-repo learning record at your repo root (created on first use; safe to commit).
- **`~/.pip/state.json`** — the cross-project store that powers the dashboard, plus the generated `~/.pip/dashboard.html`.

## The dashboard

A dark, self-contained, interactive map of your learning (no external dependencies):

- **Projects and Stacks** — two collapsible sidebar sections. A project shows the concepts you learned building it; a stack shows its **full curriculum** (everything needed to master it, including what you haven't started), with a mastery rollup bar.
- **Prerequisite concept tree** — colored ring nodes with status + grade, bezier edges, pan / zoom / fit. Colors: mastered (green), passed (amber), in-progress (sky blue), ready (gray), locked (red).
- **Node detail** — click any node for its status, aggregate grade + confidence, prerequisites, and **"Learned through"**: every project that taught it, with that project's grade and code pointer. Rows jump to that project's view.
- **Badges** — `×N` for a concept learned across N projects; `⇄` for a concept shared across stacks.
- **Learning plan panel** — a right pop-out nav (in project view) showing the project's roadmap grouped by **collapsible plan parts**, in prerequisite order, with a progress bar. Click a row to center that node.
- **Collapsible sidebars** — both the left nav and the right plan panel collapse, with canvas-edge toggles.
- **Mark as mastered** — assert mastery on a node you already know; the dashboard hands you a one-line `pip mark` message so it sticks across chats.
- **Auto-refresh** — reloads from disk every 5 minutes (toggleable) so progress appears without a manual refresh; your view is preserved across reloads.
- **Built-in How-To** — the sidebar opens on a guide to every skill and feature.

Regenerate it any time with `/pip-dashboard` (or run `scripts/render_dashboard.py`, a dependency-free stdlib renderer).

## Architecture — why it's better as a plugin

- **Repo-aware.** It builds the tree from code that exists, not from a description you type.
- **Zero infrastructure.** No MCP servers, no Postgres, no pgvector, no API keys — the host model is the teacher, your file/bash/git tools provide repo-awareness, and progress lives in plain files. Bulk reading is delegated to a cheap subagent for token efficiency.
- **Portable.** Drop it into any repo, in any language. It runs the same in a planning chat, in Claude Code, in a folder-mounted chat, or on a greenfield project — and reads the plan straight from your current conversation.

## The inviolable rule

**PIP teaches; it never writes your production code.** If a concept needs code written, PIP hands you an execution prompt to run in your build chat, then walks the result back with you. The point is that you can explain every line — not that PIP wrote it.

## Origin

PIP started as a hosted web app (FastAPI · Postgres · pgvector · React). This repository is the plugin rebuild. <!-- Original web app: add link here -->
