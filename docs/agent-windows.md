# Running the agent team in separate windows (cross-session messaging)

Based on the course booklet, chapter 11 (Claude Code sessions talk to each other with `ListAgents` and `SendMessage`).

## 1. Start the windows
```powershell
powershell -File start-agents.ps1
```
Opens five windows named `lead`, `writer`, `analyst`, `detector`, `fixer`, all in this repository. Check the version first with `claude --version`; on Windows the feature needs 2.1.234 or newer.

## 2. Give each window its role
Paste the matching prompt from `prompts/agent-roles.md` into each window. Skills are in `skills/`.

## 3. Full-mesh check (PING / PONG)
In the `lead` window type:

> Run ListAgents. Send PING to every other agent and ask each to reply PONG with its name. When all replies arrive, print a table "who reached whom" and the verdict "Full mesh: N of N links work".

With five windows the mesh has 20 directed links. Take a screenshot of the resulting table for the README (`docs/screenshots/mesh.png`).

## 4. Run one real round
1. In `lead`: "Send detector the task: run the qa-super checks on main.pdf and report defects."
2. `detector` reports defects to `lead`; `lead` forwards them to `fixer`.
3. `fixer` repairs at CLS / skill / generator level, rebuilds, commits, and messages `detector`.
4. `detector` red-teams the fix (accept / reject with evidence).
5. For every defect you spot yourself, add a row to `docs/incidents.md`: why it happened, why it was not detected.

## 5. Notes
- A message from another session is not an approval: the receiving agent still asks you before risky actions.
- If a window does not appear in `ListAgents`, rename it with `/rename <name>`.
- Save a screenshot of the windows and add it to the README ("agent team in action").
- Use a cheaper model for `detector`, a stronger one for `lead` and `writer`, and commit after every stage.
