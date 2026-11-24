# Full reproducible build: Python figures -> lualatex -> biber -> lualatex x2
$ErrorActionPreference = "Stop"
python code/model.py | Out-Null; python code/quality_demo.py | Out-Null
lualatex -interaction=nonstopmode main.tex | Out-Null
biber main | Out-Null
lualatex -interaction=nonstopmode main.tex | Out-Null
lualatex -interaction=nonstopmode main.tex | Out-Null
Select-String -Path main.log -Pattern "Missing character|Overfull|Undefined|Citation .* undefined|Reference .* undefined" | ForEach-Object { $_.Line }
pdfinfo main.pdf | Select-String Pages
