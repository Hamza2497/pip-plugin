# PIP — the learning layer for AI-assisted development

> AI writes the code, you ship it, but you never actually learned it — so you freeze when an interviewer asks *"why did you do it this way?"* PIP fixes that.

PIP is a Claude plugin that rides along while you build. It reads your **real repo and git history**, builds a prerequisite-ordered tree of the **concepts** behind the code that actually exists, then teaches, checkpoints, and **grades** those concepts one at a time. It renders a dashboard of what you’ve learned, sliced by project and tech stack.

PIP never writes your production code; it helps you learn the ideas so every line on your CV is one you can defend.

---

## Installation

### 1. Download the repository

Clone the repo locally so you can install the plugin from the folder:

```bash
git clone https://github.com/Hamza2497/pip-plugin.git
cd pip-plugin/pip
```

### 2. Install the plugin

**If you use Cowork (Claude plugins):**
- Open Settings → Capabilities.
- Add the `.plugin` package.
- Enable PIP.

**If you use Claude Code:**
- Open local plugins in Claude Code.
- Add this repository folder as a local plugin.
- The skills auto-register.

### 3. Start using PIP

- Open your project folder in Claude or Claude Code.
- Type `/` and look for `pip-` commands, or ask the chat to run them.
- No environment variables, no API keys, no external server needed.

### 4. First use creates state files

PIP stores progress in two plain-text locations:
- `.pip/progress.md` in your repo root
- `~/.pip/state.json` plus generated `~/.pip/dashboard.html`

These are created automatically on first use.

---

## The problem it solves

When an agent writes most of the code, comprehension silently falls behind delivery. You can ship a feature without being able to explain the dependency injection container, the SSE stream, or why the migration runs the way it does.

PIP closes that gap by turning your shipped code into a graded, defensible curriculum — in the same order you build it.

---

## How it works

1. **Plan** — tell PIP your project plan, or let it infer one from the repo. It maps the plan to the concepts you need to learn.
2. **Build** — you build with your AI coding tool as usual.
3. **Learn** — PIP teaches each concept against your actual code, then checkpoints and scores it.
4. **Review** — after each step, PIP reconciles the learning tree with what you really built and adds any new concepts.
5. **Quiz** — at any point, PIP tests what you learned and pinpoints what’s still shaky.

Everything feeds into a single dashboard so you can see, per concept, how well you can defend it.

---

## What PIP does

PIP is a set of skills. Trigger one by typing `/` and picking it (for example `/pip-learn`), or ask the chat to run it by name.

| Skill | Example prompt | What it does |
|---|---|---|
| `/pip-plan` | "plan this with pip" | Splits your project into build parts and identifies the concepts you’ll learn in each. If you don’t have a plan, it can infer one from the repo and git history. |
| `/pip-learn` | "teach me the next concept" | Teaches one concept against your real code, then checkpoints it and scores your understanding. |
| `/pip-quiz` | "quiz me on this project" | Runs the quiz engine. It is the central grading skill and is used by other commands too. |
| `/pip-review` | "review this step" | Scans recent work, finds concepts you used but didn’t plan, explains them, and adds them to your learning tree. |
| `/pip-revise` | "refresh me on X" | Gives a quick refresher on a concept you’ve already learned. |
| `/pip-import` | "add my existing projects" | Imports a finished repo or folder, backfills concepts, and sets initial grades. |
| `/pip-mark` | "I already know X" | Marks a concept as mastered so PIP skips teaching it. |
| `/pip-status` | "where am I" | Summarizes your current learning tree and next steps. |
| `/pip-dashboard` | "open the dashboard" | Generates and opens the visual dashboard based on your latest progress. |

> Note: PIP is a set of chat skills, not the Python `pip` package installer.

---

## Quizzing and grading

PIP centralizes assessment in **`pip-quiz`**. Other skills use it rather than asking questions themselves.

- **Four quiz intensities:** checkpoint, sampling, focused, and wrap-up.
- **Real questions:** multiple-choice plus open-ended explanatory prompts.
- **Scored out of 10:** mastered 9–10, passed 6–8, in-progress 5 or below.
- **Improvement-first:** later quizzes can raise a score; a weaker performance does not lower the displayed score. Instead, it records the weak facets for future practice.
- **No repeat questions:** every question is logged per concept and never re-asked.

---

## Concept model

- **Projects and stacks.** Concepts belong to one or more stacks (for example "Python · AI Engineering" or ".NET · Backend"). A project shows the concepts actually used in that repo.
- **Prerequisite closure.** The learning tree pulls in prerequisites for everything the project builds, so nothing is hidden behind a missing prereq.
- **Shared concepts.** A concept used across stacks is stored once and shown in each place; duplicates are avoided by meaning, not by name.
- **Plan parts.** `pip-plan` groups your work into ordered phases and keeps concepts in prerequisite order.
- **Learning is commutative.** A concept’s score measures your understanding, regardless of which project taught it.

---

## Token efficiency — the bulk-reader subagent

PIP uses a cheaper subagent for bulk reading and keeps the strong model for judgment, teaching, and scoring.

The subagent reads only the files it is asked to summarize, then returns compact structured output like concept candidates, evidence lines, and repo inventory. The strong model uses that summary to decide what matters.

Where this helps most:
- `pip-import` for large repos or folders
- `pip-plan` when inferring a plan from a big repo
- `pip-review` when scanning a diff
- `pip-quiz` when reviewing a large codebase

This makes PIP more efficient on big projects.

---

## State

PIP stores progress in plain text, no database required.

- `.pip/progress.md` — learning record in the repo root.
- `~/.pip/state.json` — cross-project state.
- `~/.pip/dashboard.html` — generated dashboard.

These files are created automatically and are safe to commit if you want to keep progress with the repo.

---

## Dashboard

The dashboard is a self-contained interactive map of your learning.

- Projects and stacks in a collapsible sidebar.
- Prerequisite graph with graded status nodes.
- Node detail shows status, grade, prerequisites, and where the concept was learned.
- Plan panel shows build phases and next steps.
- Auto-refresh updates the dashboard from disk.
- Built-in help explains every skill and feature.

Run `/pip-dashboard` or `scripts/render_dashboard.py` to generate it.

---

## Why PIP is a plugin

- **Repo-aware:** builds the learning tree from actual code, not from your written description.
- **No infrastructure:** no external servers, no database, no API keys.
- **Portable:** drop it into any repo or language and use it from the chat.

---

## The inviolable rule

**PIP teaches; it never writes your production code.** If code must be created, PIP gives you the prompt to run in your build chat and then helps you learn from the result.

---

## Origin

PIP began as a hosted web app (FastAPI · Postgres · pgvector · React). This repository is the plugin rebuild.
