import json
import sys
from pathlib import Path

import click
from rich.console import Console

from . import __version__
from .formatters import FORMATTERS
from .formatters.json import JsonFormatter
from .processors import PROCESSORS, EmailData, Pipeline
from .processors.example import ExampleProcessor

# register built-in processors and formatters
PROCESSORS["statistics"] = ExampleProcessor
FORMATTERS["json"] = JsonFormatter

console = Console(stderr=True)  # use stderr for status messages


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """SWECC Email Scraper - Process and analyze email data in mbox format.

    Commands can be piped together using standard Unix pipes. For example:

    email-scraper read input.mbox | email-scraper stats | email-scraper format -f json > output.json
    """
    pass


@main.command()
@click.argument("mbox_path", type=click.Path(exists=True, path_type=str))
def read(mbox_path: str) -> None:
    """Read emails from an mbox file and output as JSON.

    Outputs a JSON array of email objects to stdout, which can be piped to other commands.
    """
    try:
        pipeline = Pipeline([])
        emails = pipeline.load_emails(Path(mbox_path))

        email_dicts = [
            {
                "sender": e.sender,
                "subject": e.subject,
                "date": e.date,
                "content": e.content,
                "headers": e.headers,
            }
            for e in emails
        ]

        json.dump(email_dicts, sys.stdout)
    except Exception as e:
        console.print(f"[red]Error reading mbox: {e}[/red]")
        raise click.Abort() from e


@main.command()
def stats() -> None:
    """Process emails from stdin and output statistics.

    Reads JSON email data from stdin (piped from 'read' command),
    processes it using the statistics processor, and outputs results as JSON to stdout.
    """
    try:
        data = json.load(sys.stdin)

        emails = [
            EmailData(
                sender=e["sender"],
                subject=e["subject"],
                date=e["date"],
                content=e["content"],
                headers=e["headers"],
            )
            for e in data
        ]

        processor = ExampleProcessor()
        results = processor.process(emails)

        json.dump(results, sys.stdout)
    except Exception as e:
        console.print(f"[red]Error processing emails: {e}[/red]")
        raise click.Abort() from e


@main.command()
@click.option(
    "-f",
    "--format",
    "format_name",
    type=click.Choice(list(FORMATTERS.keys())),
    default="json",
    help="Output format",
)
def format(format_name: str) -> None:
    """Format JSON data from stdin using the specified formatter.

    Reads JSON data from stdin and formats it according to the specified format.
    """
    try:
        data = json.load(sys.stdin)

        formatter = FORMATTERS[format_name]()
        formatted = formatter.format(data)

        print(formatted)
    except Exception as e:
        console.print(f"[red]Error formatting data: {e}[/red]")
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


if __name__ == "__main__":
    main()
