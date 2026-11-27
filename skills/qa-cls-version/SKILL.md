---
name: qa-cls-version
description: Checks that the memoria.cls version matches the expected version and that CLS changes are logged.
---
# qa-cls-version
- `\memoriaversion` in `memoria.cls` equals the version in `docs/cls-changelog.md`.
- Every CLS change bumps the version and adds a changelog line (what, why, which defect).
- `main.tex` loads the class with no local overrides of class macros (overrides hide defects).
- `main.tex` carries no formatting commands of its own. The compact table of contents is a `\tableofcontents` wrapper in the class (1.3.4, incident I-25).
