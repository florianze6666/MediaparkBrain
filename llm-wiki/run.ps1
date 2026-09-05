# Startet das LLM-Wiki. Die venv liegt bewusst ausserhalb von OneDrive
# (C:\Users\<user>\.uv-envs\llm-wiki), da OneDrive-Sync viele kleine
# venv-Dateien sperrt und uv/pip dann mit "Zugriff verweigert" abbricht.
$env:UV_PROJECT_ENVIRONMENT = "$HOME\.uv-envs\llm-wiki"
$uv = (Get-Command uv -ErrorAction SilentlyContinue).Source
if (-not $uv) { $uv = "$env:LOCALAPPDATA\Microsoft\WinGet\Links\uv.exe" }
& $uv run uvicorn app.main:app --reload --port 8000
