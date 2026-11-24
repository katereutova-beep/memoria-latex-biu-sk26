# Opens five Claude Code windows, one per agent role, all in this repository.
# Requires Claude Code >= 2.1.234 on Windows (cross-session messaging, see booklet chapter 11).
$repo = $PSScriptRoot
$roles = 'lead', 'writer', 'analyst', 'detector', 'fixer'
foreach ($r in $roles) {
    Start-Process powershell -ArgumentList '-NoExit', '-Command', "Set-Location '$repo'; claude --name $r"
    Start-Sleep -Seconds 2
}
Write-Host "Started: $($roles -join ', '). Give each window its role prompt from prompts/agent-roles.md."
