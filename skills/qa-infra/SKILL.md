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
