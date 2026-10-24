from rich import style
import json
import ast
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

from annexa_scanner.visitors import AISDKVisitor

app = typer.Typer(help="Annexa Code Scanner for AI Components")
console = Console()

def scan_directory(target_path: Path) -> set[str]:
    visitor = AISDKVisitor()

    for py_file in target_path.rglob("*.py"):
        if ".venv" in py_file.parts or py_file.parts[0].startswith("."):
            continue

        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            visitor.visit(tree)
        except(SyntaxError, UnicodeDecodeError):
            continue

    return visitor.found_sdks

def generate_cyclonedx(sdks: set[str]) -> str:
    components = [
        {"type": "library", "name": sdk, "description": "AI Component detected via AST"}
        for sdk in sorted(sdks)
    ]

    bom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": "urn:uuid:annexa-scan-001",
        "version": 1,
        "components": components,
    }

    return json.dumps(bom, indent=2)

@app.command()
def scan(
        path: Path = typer.Argument(..., help="Directory to scan"),
        format: str = typer.Option("table", "--format", "-f" ,help="Output format: table or json")
) -> None:
    if not path.exists() or not path.is_dir():
        console.print(f"[red]Error: Path '{path}' is not a valid directory.[/red]")
        raise typer.Exit(code=1)

    with console.status(f"Scanning [cyan]{path}[/cyan] using AST parsing..."):
        detected_sdks = scan_directory(path)


    if format == "json":
        print(generate_cyclonedx(detected_sdks))
    else:
        table = Table(title="AI Components detected (AI-BOM)")
        table.add_column("Component", style="cyan", no_wrap=True)
        table.add_column("Type", style="green", justify="left")

        if not detected_sdks:
            table.add_row("No AI SDKs detected", "-")
        else:
            for sdk in sorted(detected_sdks):
                table.add_row(sdk, "Library")

        console.print(table)
        console.print(f"\n[dim]Run with --format json to generate a CycloneDX 1.6 AI-BOM.[/dim]")

if __name__ == "__main__":
    app()

