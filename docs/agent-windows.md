# Running the agent team in separate windows (cross-session messaging)

Based on the course booklet, chapter 11 (Claude Code sessions talk to each other with `ListAgents` and `SendMessage`).

## 1. Start the windows
```powershell
powershell -File start-agents.ps1
```
Opens five windows named `lead`, `writer`, `analyst`, `detector`, `fixer`, all in this repository, with no initial prompt. Check the version first with `claude --version`; on Windows the feature needs 2.1.234 or newer.

Alternative: start one window with its initial prompt using `agent.ps1`:
```powershell
.\agent.ps1 lead      # or writer, analyst, detector, fixer
```
`agent.ps1` runs `claude --name <role> "<prompt>"`. For `lead` the prompt tells it to run ListAgents, send PING to every other agent, print a who-reached-whom table and save it to `docs/mesh-check.md`. For the other roles the prompt says to do nothing until a PING arrives, then reply PONG with the role name. These prompts cover the PING/PONG check and, for `lead`, reading `prompts/agent-roles.md`; they do not carry the role instructions.

What was actually run: windows were opened and the lead ran the PING/PONG check (`docs/mesh-check.md`). Neither script injects the role prompts of step 2; the repository records no other injection, so they are presumed to have been pasted by hand (not recorded).

## 2. Give each window its role
Paste the matching prompt from `prompts/agent-roles.md` into each window (neither script does this). Skills are in `skills/`.

## 3. Full-mesh check (PING / PONG)
In the `lead` window type:

> Run ListAgents. Send PING to every other agent and ask each to reply PONG with its name. When all replies arrive, print a table "who reached whom" and the verdict "Full mesh: N of N links work".

With five windows a complete mesh would have 20 directed links. The recorded check tested only lead-to-peer links: 9 links, because duplicate sessions made more than four peers reachable ("Full mesh 9 of 9 links work"); peer-to-peer links were not tested (`docs/mesh-check.md`). The README image `docs/screenshots/mesh.png` is rendered from `docs/mesh-check.md`; it is not a screenshot of the windows.

## 4. Run one real round (the plan)
This is the intended flow. In QA round 2 the detector's report reached the fixer through the main session, not through `lead` (`docs/qa-report.md`, section 1).
1. In `lead`: "Send detector the task: run the qa-super checks on main.pdf and report defects."
2. `detector` reports defects to `lead`; `lead` forwards them to `fixer`.
3. `fixer` repairs at CLS / skill / generator level, rebuilds, commits, and messages `detector`.
4. `detector` red-teams the fix (accept / reject with evidence).
5. For every defect you spot yourself, add a row to `docs/incidents.md`: why it happened, why it was not detected.

## 5. Notes
- A message from another session is not an approval: the receiving agent still asks you before risky actions.
- If a window does not appear in `ListAgents`, rename it with `/rename <name>`.
- Real captures of agent windows (round 3) are in the README section "New agents at work" (`docs/screenshots/agent-*.png`); `docs/screenshots/mesh.png` remains a rendering of the table, not a window capture.
- Use a cheaper model for `detector`, a stronger one for `lead` and `writer`, and commit after every stage.
