# PIP — global store, grades & dashboard

The dashboard is a cross-project view of everything the user has learned. It reads one global store and renders a self-contained HTML page with two ways to slice the data: **by project** (like the old webapp) and **by stack**.

## The global store — `~/.pip/state.json`

Lives in the user's home dir (not per-repo) so it spans every project. PIP maintains it; the dashboard only reads it.

```json
{
  "generatedAt": "2026-06-13",
  "user": "Example User",
  "stacks":   [ {"id": "python-ai", "name": "Python · AI Engineering", "blurb": "FastAPI · async · LLM"} ],
  "projects": [ {"id": "pip", "name": "PIP", "stacks": ["python-ai", "frontend"], "concepts": ["fastapi", "sse", "..."],
                 "parts": [ {"name": "Backend API", "concepts": ["fastapi", "..."]}, {"name": "Frontend", "concepts": ["..."]} ]} ],
  "concepts": [
    {
      "id": "async-loop", "name": "asyncio event loop", "stacks": ["python-ai"], "prereqs": ["..."],
      "learnedIn": [
        {"project": "pip",      "grade": "A",  "code": "app/main.py:5", "date": "2026-06-01"},
        {"project": "mcp-eval", "grade": "B+", "code": "server.py:20",  "date": "2026-05-21"}
      ]
    }
  ]
}
```

Field rules:
- **stacks** — a tech area the user is building mastery in (e.g., "Python · AI Engineering", ".NET · Backend", "Frontend · React", "DevOps · Deploy"). Reuse existing ids; only add a new stack for genuinely different tech. A concept may belong to **multiple stacks** — its `stacks` is an array, so a shared concept (e.g. dependency injection) is stored once and shown in each stack's tree, never duplicated.
- **projects** — each has `stacks` and a **`concepts` execution scope**: the concepts the project actually **builds** (what `pip plan` selects from the stack curriculum). The displayed project **tree** is this scope **closed under prerequisites** at render time — every prerequisite of a built concept is pulled in and shown as a node, even ones the project doesn't build, so prerequisites are always **visible** and nothing is locked by a hidden prereq. A prerequisite may appear in a project's tree without its dependents — never the reverse. Nodes in the tree but **outside `concepts`** are prerequisites the project doesn't build: they're quizzed lightly and capped at 5 (see Scoring rubric). `learnedIn` for a project is always a subset of its `concepts`.
- **parts** (optional, project-only) — the project plan split into ordered build phases, each `{name, concepts}`, in the order the user works them (this is exactly what `pip plan` produces when it attaches concepts to plan parts). The dashboard's right pop-out nav groups the **Learning plan** and **Concept queue** by these parts. List a part's *authored* concepts; prerequisites pulled in by closure are placed automatically. **Harmony rule:** part order must never contradict prerequisite order — the dashboard enforces it by pulling any prerequisite back to (no later than) the part of the concept that needs it, and within a part it sorts by prerequisite level. Author parts so a concept's prerequisites sit in the same or an earlier part. Omit `parts` and the plan/queue fall back to a single prerequisite-ordered roadmap.
- **concepts hold the FULL curriculum of their stack — not just what's done.** Each stack's tree must list *every concept needed to master that stack*, including ones the user has not started. An unlearned concept is simply a concept with **`learnedIn: []`** — it renders as `ready` (prereqs met) or `locked` (prereqs not met), so the tree shows the path *and what remains*. When planning, seed a stack with its standard concepts even if the user hasn't reached them yet.
- **learnedIn** is the provenance: one entry **per project the concept was learned through**, each with the **score** and the `code` pointer in that project. A concept with `learnedIn.length > 1` was learned in multiple projects — the dashboard badges it `×N` and lists them all.
- **asked** (optional) — a list of short summaries of every question PIP has put to the user for this concept. Never re-ask a logged question; always craft a fresh one. Persists across projects.
- **difficulty** (optional, default 1) — rises by one each time the concept resurfaces **without** having been mastered. PIP asks harder questions at higher difficulty. (Dashboard-internal; not rendered.)
- **gaps** (optional) — the specific facets a quiz found the user short on (e.g. "edge case: empty input", "trade-off vs the alternative"). A weak quiz records these; targeted `pip-learn`/`pip-revise` works exactly these, and a later project's re-check aims at them. Cleared as the user re-demonstrates them. (Dashboard-internal; not rendered.)
- **recheck** (optional bool) — set when a quiz came out below the displayed mastery. The displayed score is **never lowered**; instead a later project re-verifies the concept (targeting `gaps`, harder questions) before trusting it, and clears the flag once re-demonstrated. (Dashboard-internal; not rendered.)
- `grade` may be omitted/empty on a seeded entry — the node then shows `✓ learned` instead of a letter until a real checkpoint grades it.

## Updating — a completed concept hits BOTH the project and the stack

On every Learn-mode checkpoint, perform a single upsert that touches both axes:
1. **Stack axis** — ensure the concept exists once under its `stack` (create the stack if new), with its `prereqs`. This is what the *stack tree* shows.
2. **Project axis** — append (or update) a `learnedIn` entry `{project, grade, code, date}` for the **current project**. This is what the *project view* shows and what links the concept to that project.

So one checkpoint updates the stack curriculum (the concept is now `mastered` in that stack's tree) *and* the current project (the concept now appears under that project with its grade). Learning the same concept later in a different project adds a second `learnedIn` entry — the cross-project provenance.

**Import** (`pip import <repo>`) adds `learnedIn` entries the same way for projects built before PIP, but **ungraded** (`✓`) — provenance without a checkpoint grade. A grade appears only once the concept is actually checkpointed.

Then **regenerate the dashboard** (next section) so the change is visible.

## Live reflect — keeping the dashboard current

The dashboard is generated HTML with the store baked in (browsers can't read local JSON over `file://`). To reflect real work:

- After updating `~/.pip/state.json` at a checkpoint, **re-run the renderer** so `~/.pip/dashboard.html` is rebuilt:
  ```
  python3 ${CLAUDE_PLUGIN_ROOT}/skills/pip/scripts/render_dashboard.py
  ```
  The user just refreshes the open tab. (Add `--open` the first time to launch it.)
- Practically: complete a concept → PIP writes the store → PIP regenerates the dashboard → the node turns green and gains its grade on refresh.

## Scoring rubric (out of 10)

Score *how well the user explained the concept at checkpoint*, not whether the code runs. **Mastered 9–10 · passed 6–8 · 5 or less is still in progress.**

| Score | Meaning |
|---|---|
| 9–10 | Explained the *why*, traced edge cases, could defend it to a skeptic — mastered. |
| 6–8 | Correct and usable, but some reasoning was filled in on prompts — passed, not yet mastered. |
| 5 | A prerequisite the project doesn't build, quizzed lightly — a modest understanding (capped here; never score these above 5). |
| <5 | Couldn't explain it; re-teach. Stays in progress. |

Be precise — use the whole range, not only 9s and 10s. A `learnedIn` entry stores **`score` (0–10)**. **A prerequisite outside the project's execution scope is capped at 5** — it's needed to understand what it leads to, but a modest understanding is enough until a project actually builds on it.

## Status derivation (computed, not stored)

- **mastered** (green) — aggregate score ≥ 9, **or self-marked** (`selfMastered: true`, or the user's dashboard mark).
- **passed** (amber) — aggregate score 6–8 (or learned-but-ungraded, e.g. imported).
- **in-progress** (sky blue) — score 5 or less (includes lightly-quizzed prerequisites the project doesn't build).
- **ready** (gray) — `learnedIn: []` but every in-stack prereq is *done* (passed or better).
- **locked** (red) — `learnedIn: []` and a prereq isn't done.

Node icon: ✓ mastered · the score (e.g. `7`) for passed/in-progress · – ready · ⌧ locked. Sub-label shows `score/10`.

**Self-mark.** A concept the user marks mastered (in the dashboard, or via `pip mark`) counts as mastered regardless of score, and PIP won't teach it. The dashboard remembers browser marks in `localStorage` and shows a sync line; the authoritative mark is `selfMastered: true` in the store, set when the user tells PIP — so it holds across every chat. Marking is blocked on `locked` concepts.

## Rendering

`scripts/render_dashboard.py` injects the store into `assets/dashboard.html` (self-contained — inline CSS/JS, no deps, no network) and writes `~/.pip/dashboard.html`. Flags: `--state PATH` (default `~/.pip/state.json`), `--out PATH`, `--open`. With no store, the template's embedded example data renders so the page is never blank. `assets/state.seed.json` is a starting store the user can copy to `~/.pip/state.json`.

## Dashboard layout

Dark canvas (#080809) with a faint starfield — the old PIP webapp aesthetic.

- **Sidebar = two collapsible sections:**
  - **Projects** (like the webapp) — every project; click one to see the concepts you **learned or can learn** through it (its scope of the stack curricula) — green where done, gray/locked where still available.
  - **Stacks** — every stack with a mastery rollup bar; click one to see its **full concept tree** (everything needed to master it, done and not-done).
- **Center:** a prerequisite **concept tree** for the selected project or stack — colored ring nodes (status + grade), bezier prerequisite edges, pan / wheel-zoom / fit. A `×N` badge marks concepts learned across multiple projects. A header tag shows whether you're viewing a `project` or a `stack`.
- **Bottom detail panel** (slides up on node click): status, aggregate grade + confidence, and **"Learned through"** — every project that taught the concept with its grade/code/date (rows are clickable → jump to that project's view), a cross-project note when N > 1, and clickable prerequisites.
- **Header:** totals (projects · stacks · mastered/total · cross-project) and concept search.

Improvements over the webapp: both project and stack lenses, grades on every node (the webapp cut grades from v1), explicit multi-project provenance, full-curriculum stack trees (you see what's left, not only what's done), and stack-level mastery rollups.
