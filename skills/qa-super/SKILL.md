---
name: qa-super
description: Orchestrator of all QA families for the Memoria LaTeX project. Runs the full build, dispatches the specialist skills, merges findings into one report and enforces the iron rule (never fix text directly).
---
# qa-super
1. Run `lualatex main.tex; biber main; lualatex main.tex; lualatex main.tex` (clean build).
2. Invoke in order: `qa-infra`, `qa-cls-version`, `qa-typeset`, `qa-BiDi`, `qa-table`, `qa-code`, `qa-img`.
3. Collect findings as `{id, skill, severity: blocker|major|minor, location, evidence, suspected_root_cause}`.
4. Hand the list to `detector` for confirmation (red team), then to `fixer`.
5. Iron rule: a fix must change the Skill or the CLS (or the generator code), then rebuild. A text-only patch is rejected.
6. Loop until zero blockers and zero majors; write the result to `docs/qa-report.md`.
Exit criterion: the same clean build twice, identical page count, no new findings.
