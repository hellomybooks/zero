# Agent Instructions

This repository is a long-form fiction project, not a software codebase. Your job is to preserve continuity without turning the story into project-management prose.

## Cold-start protocol

Do **not** scan the whole repository on first entry.

Read in this order:

1. `STATUS.md`
2. `凡存在者-项目/02-Canon/CANON-唯一真源-v1.0.md`
3. only the files required by the current task

If the task is to develop a new, plot-independent story in the same universe of ideas, read `CORE-SEED.md` instead of inheriting the current plot.

## Minimal context by task

### Continue or draft a chapter

Read only:

1. `STATUS.md`
2. Canon
3. the current volume README / control document
4. the current chapter card
5. the previous manuscript chapter
6. only the continuity files needed for the characters, knowledge, injuries, relationships, objects, and foreshadowing involved

Do not read the full archive unless a source dispute requires it.

### Edit an outline

Read:

1. `STATUS.md`
2. Canon
3. series / volume design material
4. relevant character and relationship arcs
5. unresolved continuity or foreshadowing records

### Audit a Canon conflict

Read:

1. Canon
2. Canon authority rules
3. the conflicting prose / outline
4. original historical source material only if current evidence is insufficient

## Authority order

Use the repository's Canon authority rules. In short:

1. locked Canon
2. accepted Story Bible / current structured setting
3. current outline / chapter cards
4. manuscript facts
5. review notes and audits
6. historical source material / old chats / retired drafts

A lower layer must not silently overwrite a higher layer.

When a new idea changes a locked truth, major twist, identity, world rule, or future dependency, record it explicitly as a Canon change rather than hiding the change inside prose.

## Creative invariants

- Canon is a boundary, not a railroad.
- Character truth outranks a clever technical metaphor.
- Do not rush characters toward emotional completion.
- Do not rush the world to explain itself.
- Let wrong models remain useful for a long time.
- A correct description does not guarantee a good outcome.
- A useful classification is not an essence.
- Power growth should usually come from a better question, a better representation, and a better intervention—not merely more energy.
- Every powerful ability needs failure modes, misreadings, psychological temptation, and social consequences.
- Keep ordinary life. Food, embarrassment, chores, injury, jealousy, boredom, promises, debt, and small kindness make later losses matter.
- Restraint is a baseline, not a ceiling. When a true emotional or evolution payoff arrives, it may be large, painful, spectacular, and memorable.

## Important long-range protection

Do not prematurely complete these states:

- Ren genuinely accepting that he does not know
- Zero no longer needing others to define what he is
- Lumi resolving identity through a label
- Sain genuinely accepting imperfection
- Elia learning when not to repair
- Nox fully owning a choice under uncertainty

Early scenes may contain shadows, failed versions, temporary insight, regression, or contradiction.

## Technical-language boundary

The fantasy must work for a reader who knows nothing about OpenCV, computer vision, or software engineering.

Modern CV concepts may exist as a translation layer for Ren or as design logic for the author. They are **not** the source code of the universe.

Do not reduce the setting to:

- "the universe is a matrix"
- "OpenCV is magic source code"
- "everything is a simulation"
- "classification is always evil"
- "all boundaries should be removed"
- "copies are less real"

## Archive rule

`notes/` and `凡存在者-项目/01-原始资料/` are historical evidence layers.

Default behavior: **do not read them during normal writing.**

Use them only for source recovery, disputed Canon, version archaeology, or an explicit audit task.

## Review rule

After any significant prose or structural change, ask:

1. What happened to a person before it happened to a concept?
2. Did anyone make a choice they may regret?
3. Did a character say a correct sentence they have not yet earned?
4. Did the chapter prematurely spend a future revelation or emotional payoff?
5. If all technical metaphors were removed, would the human conflict still work?

## Mechanical validation

The current repository includes a validation tool under:

`凡存在者-项目/tools/validate_project.py`

Run it after structural edits when the environment allows. It validates structure and source boundaries; it does not judge literary quality.

## Git / review discipline

- Prefer small, reviewable changes.
- Do not rewrite prose while performing a repository-architecture migration unless the prose change is independently justified.
- Preserve historical evidence.
- Use Issues for external review findings and unresolved supervision items.
- When fixing an Issue, preserve the historical discussion rather than deleting the evidence.
