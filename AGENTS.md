# Agent Instructions

This repository is a long-form fiction project, not a software codebase. Preserve continuity without turning the story into project-management prose.

## Cold start

Do **not** scan the whole repository on first entry.

Read in this order:

1. `STATUS.md`
2. `CANON.md`
3. only the minimum files required by the current task

For the existing novel, `CORE-SEED.md` is optional and normally unnecessary. It is for plot-independent parallel-story experiments, not for continuing the current Ren / Zero storyline.

## Minimum context by task

### Writing or revising prose

Read only what the scene needs:

1. `STATUS.md`
2. `CANON.md`, and the formal Canon when the scene touches a locked truth
3. the current volume README / controller
4. the current chapter card
5. the previous manuscript chapter, plus the next card only when continuity requires it
6. only the relevant continuity / character-state files

Do not read the entire archive, all previous volumes, or all audits by default.

### Changing outline or long-range structure

Read the formal Canon, the current volume design, the relevant character arcs, and the continuity / foreshadowing records that the change can affect. A major identity, world rule, twist, or future dependency requires an explicit Canon Change record.

### Investigating a conflict or historical source

Follow the formal source/conflict rules in [`凡存在者-项目/02-Canon/权威层级.md`](./凡存在者-项目/02-Canon/权威层级.md) and the Canon Change process. Only then enter `notes/` or `凡存在者-项目/01-原始资料/` as evidence.

## Authority and conflict handling

Do not invent a second authority hierarchy in this file.

- `CANON.md` is the root orientation page.
- The only formal Canon is the file linked from it.
- Source conflicts, historical evidence order, and Canon-change rules are governed by [`凡存在者-项目/02-Canon/权威层级.md`](./凡存在者-项目/02-Canon/权威层级.md).
- Structured setting, outline, chapter cards, manuscript, and review records are task context; they cannot silently overwrite a locked Canon truth.

## Creative invariants

- Canon is a boundary, not a railroad.
- Character truth outranks a clever technical metaphor.
- Do not rush emotional completion or explain the world too early.
- Let useful wrong models succeed long enough to matter.
- Correct description does not guarantee a good outcome.
- Every power needs failure modes, misreadings, psychological temptation, and social consequences.
- Keep ordinary life, embarrassment, debt, injury, jealousy, food, chores, and small kindness.
- Restraint is a baseline, not a ceiling; earned transformations may become spectacular.
- OpenCV and computer vision are a translation layer, never the source code of the universe.

Do not prematurely complete Ren accepting that he does not know, Zero no longer needing definition, Lumi resolving identity, Sain accepting imperfection, Elia learning when not to repair, or Nox fully owning a choice under uncertainty.

## Review protocol

After a significant prose or structural change, ask:

1. What happened to a person before it happened to a concept?
2. Did anyone make a choice they may regret?
3. Did a character say a correct sentence they have not earned?
4. Did the change spend a future revelation or emotional payoff early?
5. If technical metaphors were removed, would the human conflict still work?

For high-risk Canon/prose boundaries, use the stricter rule established by the Chapter 36 review: compare **authority requirement → prose's most natural reading → strictest conflict judgment**. "It can be explained away" is not automatically a pass.

Run `python3 凡存在者-项目/tools/validate_project.py` after structural edits. It checks project wiring and source boundaries; it does not judge literary quality.

## Archive and Git

Treat `notes/` and `凡存在者-项目/01-原始资料/` as historical evidence. Read them only for source recovery or an explicit audit.

Preserve historical discussion when fixing an Issue. Keep changes small and scoped. Never rewrite prose as a side effect of an architecture migration.
