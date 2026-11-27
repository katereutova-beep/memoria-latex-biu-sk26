# Full reproducible build: lint -> Python figures -> lualatex -> biber -> lualatex x2 -> copy the final PDF.
# Every step must succeed. A non-zero exit code of any Python, LuaLaTeX or Biber command stops the build
# before the final PDF is copied (incident I-22). Run from any folder: the script switches to the repository root.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$started = Get-Date

function Invoke-Step {
    param([Parameter(Mandatory)][string]$Name, [Parameter(Mandatory)][scriptblock]$Command)
    $global:LASTEXITCODE = 0
    & $Command
    $code = $LASTEXITCODE
    if ($code -ne 0) {
        if (Test-Path main.log) { Write-Host "--- last lines of main.log"; Get-Content main.log -Tail 12 }
        throw "Build step '$Name' failed with exit code $code. The final PDF was not copied."
    }
}

Invoke-Step "model.py" { python code/model.py | Out-Null }
Invoke-Step "quality_demo.py" { python code/quality_demo.py | Out-Null }
Invoke-Step "lint_bidi (sources and generated figures)" { python code/lint_bidi.py }
Invoke-Step "lualatex pass 1" { lualatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null }
Invoke-Step "biber" { biber main | Out-Null }
Invoke-Step "lualatex pass 2" { lualatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null }
Invoke-Step "lualatex pass 3" { lualatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null }

# Guards that do not depend on exit codes: a fresh PDF, and no LaTeX error line in the final log.
if (-not (Test-Path main.pdf) -or (Get-Item main.pdf).LastWriteTime -lt $started) {
    throw "main.pdf was not produced by this build. The final PDF was not copied."
}
if (Select-String -Path main.log -Pattern '^!' -Quiet) {
    throw "main.log contains a LaTeX error line. The final PDF was not copied."
}

Select-String -Path main.log -Pattern "Missing character|Overfull|Undefined|Citation .* undefined|Reference .* undefined" | ForEach-Object { $_.Line }
Invoke-Step "pdfinfo" { pdfinfo main.pdf | Select-String Pages }
Copy-Item main.pdf Memoria-biu-sk26.pdf -Force   # the committed final PDF is always the latest successful build (incidents I-21, I-22)
