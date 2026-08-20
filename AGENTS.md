# Agent Instructions

This repository is a long-form fiction project, not a software codebase. Preserve continuity without turning the story into project-management prose.

## Cold start

Do not scan the whole repository on first entry. Read:

1. `STATUS.md`
2. `CANON.md`, then the formal Canon only when the task needs it
3. only the files required by the current task

For a plot-independent story in the same conceptual universe, read `CORE-SEED.md` and do not inherit the current plot by default.

## Authority order

1. locked Canon
2. accepted structured setting
3. current outline and chapter cards
4. manuscript facts
5. review notes and audits
6. historical source material

A lower layer must not silently overwrite a higher layer. Any change to a locked truth, major twist, identity, world rule, or future dependency requires an explicit Canon Change record.

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

Run `python3 凡存在者-项目/tools/validate_project.py` after structural edits. It checks project wiring and source boundaries; it does not judge literary quality.

## Archive and Git

Treat `notes/` and `凡存在者-项目/01-原始资料/` as historical evidence. Read them only for source recovery or an explicit audit. Preserve historical discussion when fixing an Issue. Keep changes small, inspect the worktree, stage only confirmed paths, and never rewrite prose as a side effect of an architecture migration.
