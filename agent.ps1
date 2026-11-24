# Starts one named Claude Code agent session with its initial role prompt.
# Usage: .\agent.ps1 writer|analyst|detector|fixer|lead
param([Parameter(Mandatory)][ValidateSet('lead','writer','analyst','detector','fixer')][string]$Role)
Set-Location $PSScriptRoot
if ($Role -eq 'lead') {
    $prompt = "You are the lead agent of the Memoria project. Read prompts/agent-roles.md. Step 1: run ListAgents. Step 2: send PING to every other agent with SendMessage and ask each to reply PONG with its name. Step 3: when replies arrive, print a table of who reached whom and the verdict Full mesh N of N links work. Save the table to docs/mesh-check.md."
} else {
    $prompt = "You are the $Role agent of the Memoria project. Do nothing until another agent sends you PING. Then reply to the sender with SendMessage: PONG and your name $Role."
}
claude --name $Role $prompt
