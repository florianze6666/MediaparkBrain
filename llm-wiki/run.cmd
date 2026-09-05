@echo off
REM Startet das LLM-Wiki unter http://127.0.0.1:8000
REM Batch-Datei statt run.ps1, weil die PowerShell-Ausfuehrungsrichtlinie
REM (Set-ExecutionPolicy) .ps1-Skripte auf vielen Rechnern blockiert.
cd /d "%~dp0"

where uv >nul 2>nul
if errorlevel 1 (
  echo [Fehler] uv wurde nicht gefunden.
  echo          Installieren mit:  winget install astral-sh.uv
  echo          Danach ein neues Terminal oeffnen.
  pause
  exit /b 1
)

if not exist ".env" (
  echo [Hinweis] Keine .env vorhanden - es gibt nur Wiki-Ausschnitte, keine LLM-Antworten.
  echo           Anlegen mit:  copy .env.example .env    und ANTHROPIC_API_KEY eintragen.
  echo.
)

echo Starte das LLM-Wiki auf http://127.0.0.1:8000  (Beenden mit Strg+C)
uv run uvicorn app.main:app --reload --port 8000
