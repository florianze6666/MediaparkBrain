# Gemeinsame Umgebung fuer alle qmd-Skripte dieses Teilprojekts.
#
# Zweck: QMD legt Modelle und Konfiguration sonst global unter
# %USERPROFILE%\.cache\qmd bzw. %USERPROFILE%\.config\qmd ab. Beides wuerde die
# Abschottungs-Zusage aus .plans/qmd_standalone_plan.md brechen. Hier wird alles
# auf diesen Ordner umgebogen, damit der Rueckbau ein einziger Loeschbefehl bleibt.
#
# Aufruf aus anderen Skripten:  . "$PSScriptRoot\env.ps1"
# Von Hand:                     . .\env.ps1          (GPU, wenn vorhanden)
#                               . .\env.ps1 -Cpu     (CPU erzwingen, z. B. zum Testen)
#
# Hardware: QMD (node-llama-cpp) waehlt das Geraet selbst: CUDA, sonst Vulkan,
# sonst CPU. Ein Rechner ohne GPU braucht keine andere Konfiguration, nur mehr
# Zeit (siehe README, Abschnitt Hardware). -Cpu setzt QMD_FORCE_CPU und
# erzwingt den CPU-Pfad auch auf einem GPU-Rechner.

param(
    [switch] $Cpu
)

$ErrorActionPreference = "Stop"

$QmdRoot = $PSScriptRoot

# MODEL_CACHE_DIR in dist/llm.js: <XDG_CACHE_HOME>\qmd\models
$env:XDG_CACHE_HOME = Join-Path $QmdRoot ".cache"

# getConfigDir() in dist/collections.js wertet QMD_CONFIG_DIR zuerst aus.
# Die projektlokale .qmd\index.yml haelt zusaetzlich die Index-Datenbank hier
# im Ordner. index.ps1 schreibt sie aus der Vorlage index.template.yml.
$env:QMD_CONFIG_DIR = Join-Path $QmdRoot ".qmd"

# Embedding-Modell, falls .qmd\index.yml noch nicht existiert ("qmd init"
# uebernimmt den Wert). Steht die Datei, gilt deren models.embed. Beide
# Stellen muessen dasselbe Modell nennen; index.ps1 sorgt dafuer.
$env:QMD_EMBED_MODEL = "hf:NeoRoth/nemotron-3-embed-1b-gguf/nemotron-3-embed-1b-q8_0.gguf"

if ($Cpu) {
    $env:QMD_FORCE_CPU = "1"
} else {
    Remove-Item Env:QMD_FORCE_CPU -ErrorAction SilentlyContinue
}

# Reine Vorsichtsmassnahme: nichts von diesem Teilprojekt darf in das
# Wiki-Projekt schreiben. Der Korpus wird ausschliesslich lesend verwendet.
$CorpusDir = Resolve-Path (Join-Path $QmdRoot "..\corpus")

# Lokales qmd, kein globales npm-Paket.
$QmdExe = Join-Path $QmdRoot "node_modules\.bin\qmd.ps1"

function Invoke-Qmd {
    param([Parameter(ValueFromRemainingArguments = $true)] $Args)
    & $QmdExe @Args
}

$Device = if ($Cpu) { "CPU erzwungen (QMD_FORCE_CPU=1)" } else { "automatisch (CUDA > Vulkan > CPU)" }
Write-Host "qmd-Umgebung aktiv" -ForegroundColor DarkGray
Write-Host "  Modelle : $env:XDG_CACHE_HOME\qmd\models" -ForegroundColor DarkGray
Write-Host "  Konfig  : $env:QMD_CONFIG_DIR" -ForegroundColor DarkGray
Write-Host "  Korpus  : $CorpusDir (nur lesend)" -ForegroundColor DarkGray
Write-Host "  Geraet  : $Device" -ForegroundColor DarkGray
