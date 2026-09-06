# index.ps1: Wissensspeicher von Grund auf aufbauen oder nach Korpusaenderung erneuern.
#
# Laeuft auf jedem Rechner gleich; das Geraet (CUDA, Vulkan, CPU) waehlt QMD selbst.
# Erwartet: Node 22+, Python 3 mit PyYAML, uv, "npm install" in diesem Ordner erledigt
# (der postinstall-Schritt wendet patches/apply.mjs an).
#
# Schritte:
#   0. uv sync: eigene Python-Umgebung des Teilprojekts (.venv, kein Download)
#   1. Sicht view/ aus corpus/ bauen (Hardlinks, drei Rechteklassen)
#   2. .qmd/index.yml aus index.template.yml mit den Pfaden dieses Rechners schreiben
#   3. qmd init, qmd trust (Freigabe des eigenen Modells), qmd pull (GGUF laden)
#   4. qmd update (Dokumente indizieren), qmd embed -f (Vektoren, ohne Zeitlimit),
#      danach die Projektantraege in die Collection antraege (ingest/import.py antraege)
#   5. Testsuite eval/run_tests.py
#
# Aufruf:  .\index.ps1                GPU, wenn vorhanden, sonst CPU
#          .\index.ps1 -Cpu           CPU erzwingen
#          .\index.ps1 -SkipEmbed     nur Sicht, Konfiguration, Modelle, Index
#          .\index.ps1 -SkipTests     ohne Testsuite
#
# Dauer des Einbettens (992 Chunks): RTX 2080 rund 3,5 Minuten. Auf reiner CPU
# ist node-llama-cpp unter Windows sehr langsam (siehe README, Hardware);
# deshalb kein Zeitlimit (--timeout 0), der Lauf darf Stunden dauern.

param(
    [switch] $Cpu,
    [switch] $SkipEmbed,
    [switch] $SkipTests
)

$ErrorActionPreference = "Stop"
. "$PSScriptRoot\env.ps1" -Cpu:$Cpu
Set-Location $PSScriptRoot

function Step($text) { Write-Host "`n== $text" -ForegroundColor Cyan }

Step "0/5 Python-Umgebung des Teilprojekts (uv sync)"
uv sync --no-python-downloads
if ($LASTEXITCODE -ne 0) { throw "uv sync fehlgeschlagen" }

Step "1/5 Sicht view/ aus corpus/ bauen"
python ingest\build_view.py --klassen
if ($LASTEXITCODE -ne 0) { throw "build_view.py fehlgeschlagen" }

Step "2/5 .qmd\index.yml aus index.template.yml schreiben"
$yml = (Get-Content -Raw -Encoding UTF8 "$PSScriptRoot\index.template.yml").Replace("{{QMD_ROOT}}", $PSScriptRoot)
New-Item -ItemType Directory -Force -Path "$PSScriptRoot\.qmd" | Out-Null
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$PSScriptRoot\.qmd\index.yml", $yml, $utf8NoBom)
Get-Content "$PSScriptRoot\.qmd\index.yml" | Select-String "^\s+(path|embed):"

Step "3/5 qmd init, trust, pull"
Invoke-Qmd init
Invoke-Qmd trust
Invoke-Qmd pull

Step "4/5 qmd update und embed"
Invoke-Qmd update
if (-not $SkipEmbed) {
    Invoke-Qmd embed -f --timeout 0
    uv run python ingest\import.py antraege
    if ($LASTEXITCODE -ne 0) { throw "import.py antraege fehlgeschlagen" }
}
Invoke-Qmd status

if (-not $SkipTests) {
    Step "5/5 Testsuite"
    $testArgs = @()
    if ($Cpu) { $testArgs += "--cpu" }
    python eval\run_tests.py @testArgs
    if ($LASTEXITCODE -ne 0) { throw "Testsuite nicht bestanden" }
}

Write-Host "`nFertig." -ForegroundColor Green
