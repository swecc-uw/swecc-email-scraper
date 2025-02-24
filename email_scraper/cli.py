from pathlib import Path
from typing import List, Union

import click
from rich.console import Console
from rich.progress import Progress

from . import __version__
from .formatters import FORMATTERS
from .formatters.json import JsonFormatter
from .processors import PROCESSORS, Pipeline
from .processors.example import ExampleProcessor

# register built-in processors and formatters
PROCESSORS["statistics"] = ExampleProcessor
FORMATTERS["json"] = JsonFormatter

console = Console()


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """SWECC Email Scraper - Process and analyze email data in mbox format."""
    pass


@main.command()
@click.argument("mbox_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--processors",
    "-p",
    multiple=True,
    default=["statistics"],
    type=click.Choice(list(PROCESSORS.keys())),
    help="Processors to run (can specify multiple times)",
)
@click.option(
    "--format",
    "-f",
    "format_name",
    default="json",
    type=click.Choice(list(FORMATTERS.keys())),
    help="Output format",
)
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Path to save the output")
def process(mbox_path: Path, processors: list[str], format_name: str, output: Path | None) -> None:
    """Process an mbox file using selected processors.

    MBOX_PATH: Path to the mbox file to process
    """
    try:
        # Create pipeline with selected processors
        pipeline = Pipeline([PROCESSORS[name]() for name in processors])

        # Process the emails
        with Progress() as progress:
            task = progress.add_task("Processing emails...", total=100)
            results = pipeline.process(mbox_path)
            progress.update(task, completed=100)

        # Format and output results
        formatter = FORMATTERS[format_name]()
        formatted = formatter.format(results)

        if output:
            formatter.save(results, output)
            console.print(f"[green]Results saved to {output}[/green]")
        else:
            console.print(formatted)

    except Exception as e:
        console.print(f"[red]Error: {e!s}[/red]")
        raise click.Abort() from e


@main.command()
def list_processors() -> None:
    """List available email processors."""
    console.print("\n[bold]Available Processors:[/bold]\n")

    for name, processor_cls in PROCESSORS.items():
        console.print(f"[green]{name}[/green]: {processor_cls.description}")


@main.command()
def list_formats() -> None:
    """List available output formats."""
    console.print("\n[bold]Available Output Formats:[/bold]\n")

    for name, formatter_cls in FORMATTERS.items():
        console.print(f"[green]{name}[/green]: {formatter_cls.description}")


def process_mbox(
    mbox_path: Union[str, Path],
    processors: List[str],
    output_format: str = "text",
) -> None:
    """Process an mbox file with the specified processors."""
    path = Path(mbox_path) if isinstance(mbox_path, str) else mbox_path
    if not path.exists():
        raise click.BadParameter(f"Mbox file not found: {mbox_path}")


if __name__ == "__main__":
    main()
