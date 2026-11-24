---
name: qa-infra
description: Checks project structure, reproducibility and repository contents.
---
# qa-infra
- Required files exist: `main.tex`, `memoria.cls`, `chapters/*.tex`, `PRD.md`, `PLAN.md`, `TODO.md`, `README.md`, `skills/`, `prompts/`, final PDF.
- Clean-clone build works with the documented command sequence.
- `.gitignore` excludes aux files but keeps the final PDF; no secrets; no files >10 MB.
- Both partners have commits; commit messages are meaningful; branch merged via pull.
