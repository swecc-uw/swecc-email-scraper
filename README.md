# SWECC Email Scraper

A Python CLI tool for analyzing email data in mbox format. This tool helps you extract insights and perform analysis on email archives.

## Features

- 📧 Process mbox format email archives
- 📊 Extendable framework for building analysis pipelines
- 🎨 Rich command-line interface with progress reporting
- Coming soon: Actual analysis...

## Installation

### From PyPI

```bash
pip install swecc-email-scraper
```

### From Source

```bash
git clone https://github.com/swecc/email-scraper.git
cd email-scraper
pip install -e ".[dev]"  # Install with development dependencies

# Run tests
pytest
```

## Quick Start

1. Basic usage with default statistics processor:
```bash
swecc-email-scraper process path/to/mailbox.mbox
```

2. Use multiple processors and specify output format:
```bash
swecc-email-scraper process path/to/mailbox.mbox -p statistics -p headers -f json -o results.json
```

3. List available processors:
```bash
swecc-email-scraper list-processors
```

4. List available output formats:
```bash
swecc-email-scraper list-formats
```


## Basic Example Usage

1. Basic email statistics:
```bash
swecc-email-scraper process inbox.mbox
```

2. Export analysis to a file:
```bash
swecc-email-scraper process inbox.mbox -o analysis.json
```

3. Use multiple processors:
```bash
swecc-email-scraper process inbox.mbox -p statistics -p <processor_name>
```

## Extending the Tool

The tool is designed to be easily extensible. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed information on:

- Creating custom processors
- Adding new output formats
- Contributing to the project
- Development setup and guidelines

## Architecture

The tool uses a pipeline architecture where:

1. `EmailData` objects represent individual emails with parsed metadata
2. `Pipeline` manages the flow of data through processors
3. `EmailProcessor`s transform or analyze the data
4. `OutputFormatter`s convert results to different formats


## License

MIT License - See [LICENSE](LICENSE) file for details.

## Acknowledgments

Developed as part of SWECC Labs at the University of Washington.
