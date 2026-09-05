"""CLI: python -m mpb <befehl>. Dieselben Services wie die API."""
def main() -> None:  # wird in cli/main.py implementiert
    from mpb.cli.main import main as _main
    _main()
