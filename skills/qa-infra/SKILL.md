---
name: qa-infra
description: Checks project structure, reproducibility and repository contents.
---
# qa-infra
- Required files exist: `main.tex`, `memoria.cls`, `chapters/*.tex`, `PRD.md`, `PLAN.md`, `TODO.md`, `README.md`, `skills/`, `prompts/`, final PDF.
- Clean-clone build works with the documented command sequence.
- `.gitignore` excludes aux files but keeps the final PDF; no secrets; no files >10 MB.
- Both partners have commits; commit messages are meaningful; branch merged via pull. Status at `01d97bb` (2026-11-27): met. Commits: 24 by Katrina Reutova and 1 by Alexandra Pirogan (`ced6645`). Pushes: Katrina and `sspirogan` (GitHub). Pulls: Katrina (`git reflog`) and Alexandra (her confirmation, relayed by the user; git does not record pulls). Before `ced6645` all commits carried one git identity.
- The final PDF `Memoria-biu-sk26.pdf` must equal the latest `main.pdf` (`build.ps1` copies it); compare page counts before shipping (incident I-21).
- `build.ps1` must stop at the first failed Python, LuaLaTeX or Biber command (non-zero exit code) and must not copy the final PDF after a failure (incident I-22). Verify by failure injection in a throw-away clone, never in the project folder: put a syntax error in `code/model.py`, an undefined macro in a chapter, and a corrupt `bib/references.bib`; each run must exit non-zero with a "Build step ... failed" message and leave a sentinel file in place of `Memoria-biu-sk26.pdf` untouched, while a run without injection must replace it. Run every build from inside its own folder; `build.ps1` switches to its own folder itself.
