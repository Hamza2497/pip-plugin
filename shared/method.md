# PIP — method reference

Load this when planning a concept tree or designing a checkpoint. It is the detail behind the SKILL.md loop.

## Concept extraction — ideas, not actions

A **concept** is something a person must *understand*; an **action** is something they *do*. Teach only concepts.

| Action (do NOT make this a concept) | Concept (DO extract this) |
|---|---|
| Run `alembic upgrade head` | How Alembic tracks the migration head and computes the upgrade path |
| Add `async` to the function | Why this call is I/O-bound and what the event loop does while it awaits |
| `pip install pgvector` | How cosine similarity over embeddings ranks "nearest" concepts |
| Wrap it in `try/except` | Which failures are recoverable here and why catching broadly hides bugs |
| Call `git rebase -i` | What a rebase rewrites and why that changes commit identity |

Extraction rules:
- **1–4 concepts per area/step.** More than 4 means the area is really several areas — split it.
- Prefer the concept the user is **most likely to be asked about in an interview** for this code.
- A concept must be **specific to how it shows up in this codebase**, not a textbook definition. Anchor it to the recorded code pointer.
- If two candidate concepts collapse into one idea, merge them.

## Concept identity — canonical naming & no duplicates

The global store **is** the concept registry. Before creating a concept, **search the store for one that already means the same thing and reuse it** (same `id`, same name) instead of minting a near-duplicate. Match by **meaning, not string** — "asyncio event loop", "async/await", and "the event loop" are one concept, not three.

Naming rules, applied every time a concept is named:
- Name the **idea** as a noun phrase — never a tool, library, command, or action. "Dependency injection", not `services.AddScoped`; "cosine-similarity nearest-neighbour search", not "pgvector".
- One canonical name per concept; prefer the name already in the store over a new synonym. Keep a short `aliases` list on the concept so future scans resolve to it.
- Consistent granularity — roughly one interview-answerable idea per concept; don't split one idea into overlapping nodes or merge two distinct ideas into one.
- Stable `id` = kebab-case of the canonical name; never mint a second id for the same idea.
- Language/stack-specific variants are separate only when the underlying idea genuinely differs (e.g. C# `async`/`await` vs Python's event loop). If the idea is the same, it's one concept.

When unsure whether two are the same concept, they probably are — merge.

**Cross-stack is the same registry.** The dedup check spans *all* stacks, not just the current one — "FastAPI dependency injection" and "ASP.NET Core DI" are the same idea (dependency injection) and must be **one** concept, not one per stack. A shared concept carries a **`stacks` array** and is stored once, appearing in every stack tree it belongs to. Split by stack only when the mechanics genuinely differ (e.g. Python's event loop vs C#'s `Task`-based async).

### Placing a concept — resolution order

Any concept that needs a home (most often one that emerges during Review) resolves to a real node in the stack curricula — never an ad-hoc addition. In order:

1. **Current stack** — already in this stack's curriculum (matched *by meaning*)? Use that node.
2. **Other stacks** — present in another stack's curriculum? It's the **same** concept: add the current stack to its `stacks` array (now shared) and reuse it. Never duplicate it.
3. **Nowhere** — only then consider a **new** node, and **scrutinise first**: run dedup-by-meaning across the whole registry (it may already exist under a different name), and confirm it's a standard, defensible concept for the stack — a real idea, not a tool, command, or one-off. If in doubt, don't add it.

The bias is **conservative**: reuse and share before you create. Don't grow stacks left and right.

## Stack curricula — the full path to mastery

A stack tree should show **everything needed to master that stack**, not only what the user has touched. When a stack first appears (or on request), **generate its reference curriculum** — the standard concepts a strong engineer in that stack is expected to know — as concepts with prereqs and `learnedIn: []`. The user's learned concepts then match onto that curriculum by meaning (see canonical naming) and turn green; the gray/locked nodes are the road ahead. Keep the curriculum honest and conventional for the stack — comprehensive, but no niche trivia padding. A stack tree that contains only what the user has already built is incomplete by definition.

## Repo-awareness — the scan sequence

When planning from a real repo, gather evidence before decomposing:

1. **Identity:** `Read` README + dependency manifest(s) + entry point(s). Determine language, framework, what the app does.
2. **Shape:** `Glob` the source tree; `Read` the files that carry real logic (routes/handlers, models, services, the agent/loop, auth, migrations). Skip generated/boilerplate.
3. **History:** `Bash` →
   - `git log --oneline -n 30` — the order things were built.
   - `git log -p -n <k> -- <path>` — how a specific tricky piece evolved, when needed.
   - `git log --stat -n 10` — which files change together (coupling signal).
4. **Map:** for each concept, record the file:line and/or commit where it lives. Every lesson then points at real code.

Derive the tree from this evidence. Only fall back to asking the user when the repo genuinely can't answer (e.g., intent behind an undocumented design choice).

## Prerequisite ordering — cycle-free by construction

Prerequisites form a DAG that gets walked in order. LLMs occasionally emit a cycle (A needs B, B needs A), which makes ordering impossible. Prevent it structurally instead of detecting it after:

- Give every concept a **rank** = the order it was first created (earlier areas/commits rank lower). Ties broken deterministically by name.
- **Store a prerequisite edge only when `rank(prereq) < rank(concept)`** — every edge points "backward" along one total order, so the graph can never contain a cycle.
- When an edge would violate that (points forward), **drop it and log it** in the dropped-edge log. Do **not** reverse it — reversing injects a prerequisite claim that may be pedagogically false. The two concepts stay ordered by rank, so the learning order is still meaningful; only the unreliable directional claim is dropped.
- Order the tree with this rank as the tiebreak so independent concepts come out in a stable, sensible sequence.

This is a deterministic, domain-weighted feedback-arc-set heuristic: the "weight" is agreement with build order, and prevention-first means cycles never enter the stored tree.

## Checkpoint questions — force reasoning, not recall

A good checkpoint cannot be answered by repeating the lesson. Patterns that work:

- **"Why this and not that?"** — "Why is this call `await`ed but the one above it isn't?"
- **"What breaks if…?"** — "What would happen if two requests hit this endpoint at the same time with the same key?"
- **"Where would you change it?"** — "If you needed this to also support X, which line changes and why?"
- **"Explain it to a skeptic"** — "A reviewer says this `try/except` is too broad. Are they right? Defend or concede."
- **Trace it** — "Walk the value from the request to the database and back; where could it become `None`?"

Avoid yes/no questions and definition-recall ("What is a decorator?"). One question per checkpoint.

**Delivery — always the question popup.** Ask every checkpoint/quiz through Claude's question popup (`AskUserQuestion`), mixing two kinds:
- **Multiple-choice** — make it *hard*: 3–4 options whose wrong answers are *close*, subtle misconceptions a half-understanding learner would actually choose (never obviously-wrong facts). Each distractor maps to a specific misunderstanding so a wrong pick is diagnostic.
- **In your own words** — ask with no real answer choices and let the user write their explanation in the free-text input; judge the writing. Use these when articulation matters more than recognition.

On a wrong multiple-choice pick, **read which option they chose**, infer the misconception it encodes, and walk them from *that* point to the right answer before re-checking — don't re-explain generically. Fall back to a plain typed question only if the host can't show the popup.

## Evaluation rubric

| Answer quality | Action |
|---|---|
| Correct + reasoned (explains *why*, not just *what*) | Mark `checkpointed`; add to mastery list; advance. |
| Right conclusion, shaky reasoning | Name the gap, give the missing link, re-ask a narrower question. |
| Wrong | Correct directly and constructively; teach the missing idea; re-check before advancing. |
| Pattern-matched / recited | Push with a "why" or "what breaks" follow-up; don't pass on recall alone. |

Honest scoring is the product. A concept marked `checkpointed` is a promise the user can defend it in an interview.

Also assign a **score out of 10** at each checkpoint — **mastered 9–10, passed 6–8** (5 or less is still in progress) — and record it in the global store; see `dashboard.md`. A prerequisite the project doesn't actually build is quizzed lightly and **capped at 5** (a modest understanding) until a later project executes it. The score is per-project, so a concept learned in two projects carries two scores and an aggregate the dashboard displays.

## `.pip/progress.md` schema

```markdown
# PIP Progress — <project name>

_Source: <repo path or "described project">. Last updated: <YYYY-MM-DD>._

## Concept tree

### <Area / step 1>
- [x] **<concept>** — `built` · prereqs: none · code: `src/app/db.py:42` / commit `a1b2c3d`
- [~] **<concept>** — `teaching` · prereqs: <concept> · code: `src/app/routes.py:88`
- [ ] **<concept>** — `new` · prereqs: <concept> · code: `src/app/agent.py:12`
- [ ] **<concept>** — `known` (deduped) · code: `src/app/main.py:5`

### <Area / step 2>
- [ ] **<concept>** — `new` · prereqs: <area-1 concept>

## Mastery list (deduped — known across all projects)
- <concept> — from <project/area>
- <concept> — from <project/area>

## Dropped prerequisite edges (log)
- <prereq> → <concept>  (dropped: would point forward in build order)
```

Checkbox convention: `[ ]` not done · `[~]` in progress · `[x]` done. The checkbox is cosmetic; the backticked status word is authoritative.

## Plan input & part attachment

`pip plan` accepts the plan three ways, in priority: a **plan file** the user points at, a **plan pasted** in the message, or — failing both — a plan inferred from the repo. Whatever the source, split it into **parts** (the build steps) and attach 1–4 concepts to each part. `.pip/progress.md` is grouped by part, and teaching follows the plan: finish a part → checkpoint its concepts → move to the next. This is what makes PIP "ride along" — the concepts are pinned to the part of the plan you're building.

## Importing existing projects

`pip import <repo>` backfills history so the dashboard reflects work done before PIP. Scan the repo, list the concepts it demonstrates, and for each add a `learnedIn` entry under the right stack with a `code` pointer — **ungraded** (`✓`), because nothing was checkpointed. Never fabricate a score for imported work; a score is earned only at a real checkpoint or quiz. Offer to checkpoint imported concepts to convert `✓` into a score.

Optionally run a **short mastery quiz** at import to set real grades instead of `✓`: sample the project's key concepts, and when the user passes a concept, **pass its prerequisites transitively** — using X correctly implies the Y it depends on. Unquizzed, uninferred concepts stay `✓`. The quiz is a fast confidence check, not a full checkpoint.

## Two-chat handoff (optional)

PIP teaches; it does not write the user's production code. When a concept requires code, hand off an execution prompt for the user's build chat (Claude Code or similar), then walk the returned output back before marking the concept `built`. Keep PIP as the place the concept tree and progress live; the build chat is disposable.
