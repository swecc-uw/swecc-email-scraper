# SWECC Email Scraper

A Python CLI tool for analyzing email data in mbox format.

## Features

- 📧 Process mbox format email archives
- 🔧 Unix-style pipeline architecture for flexible processing
- 📊 Extendable framework for building analysis pipelines
- Coming soon: More analysis processors...

## Installation

### From PyPI

```bash
pip install swecc-email-scraper
```

### From Source

```bash
git clone https://github.com/swecc-uw/swecc-email-scraper.git
cd swecc-email-scraper
pip install -e ".[dev]"  # Install with development dependencies

# Run tests
pytest
```

## Quick Start

The tool uses Unix pipes to compose commands. Each command does one thing and can be combined with others:

1. Basic usage - get email stats with example processor:
```bash
swecc-email-scraper read mailbox.mbox \
  | swecc-email-scraper stats \
  | swecc-email-scraper format -f json > results.json
```

2. Basic Csv usage - get email stats with example processor:
```bash
swecc-email-scraper read mailbox.mbox \
  | swecc-email-scraper stats \
  | swecc-email-scraper format -f csv > results.csv
```

3. Basic Yaml usage - get email stats with example processor:
```bash
swecc-email-scraper read mailbox.mbox \
  | swecc-email-scraper stats \
  | swecc-email-scraper format -f yaml > results.yaml
```

4. List available processors:
```bash
swecc-email-scraper list-processors
```

5. List available output formats:
```bash
swecc-email-scraper list-formats
```

## Command Reference

### Read Command
Reads an mbox file and outputs email data as JSON:
```bash
swecc-email-scraper read input.mbox > emails.json
```

### Stats Command
Processes email data from stdin and outputs statistics:
```bash
cat emails.json | swecc-email-scraper stats > stats.json
```

### Format Command
1. Formats JSON data using the json formatter:
```bash
cat stats.json \
  | swecc-email-scraper format -f json \
  > formatted.json
```

2. Formats CSV (Checks for nested data: throws error if found) using the csv formatter:
```bash
cat stats.json \
  | swecc-email-scraper format -f csv \
  > formatted.csv
```

3. Formats CSV (Unchecked: converts nested data into string) using the csv formatter:
```bash
cat stats.json \
  | swecc-email-scraper format -f csv -u \
  > formatted.csv
```
4. Formats YAML data using the yaml formatter:
```bash
cat stats.json \
  | swecc-email-scraper format -f yaml \
  > formatted.yaml
```

## Pipeline Examples

1. Basic email statistics to terminal:
```bash
swecc-email-scraper read inbox.mbox \
  | swecc-email-scraper stats \
  | swecc-email-scraper format
```

2. Save analysis to a file:
```bash
swecc-email-scraper read inbox.mbox \
  | swecc-email-scraper stats \
  > analysis.json
```

3. Process with json formatting:
```bash
swecc-email-scraper read inbox.mbox \
  | swecc-email-scraper stats \
  | swecc-email-scraper format -f json \
  > analysis.json
```

4. Process with json formatting:
```bash
swecc-email-scraper read inbox.mbox \
  | swecc-email-scraper stats \
  | swecc-email-scraper format -f csv \
  > analysis.csv
```

5. Process with json formatting:
```bash
swecc-email-scraper read inbox.mbox \
  | swecc-email-scraper stats \
  | swecc-email-scraper format -f yaml \
  > analysis.yaml
```

6. Use with Unix tools:
```bash
# Filter emails before analysis
swecc-email-scraper read inbox.mbox \
  | jq 'map(select(.sender | contains("important")))' \
  | swecc-email-scraper stats
```

## Extending the Tool

The tool is designed to be easily extensible. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed information on:

- Creating custom processors
- Adding new output formats
- Contributing to the project
- Development setup and guidelines

## Architecture

The tool uses a Unix pipeline architecture where:

1. `read` command converts mbox files to JSON email data
2. Processor commands (like `stats`) transform or analyze the data
3. `format` command handles output formatting
4. Standard Unix pipes (`|`) connect the components

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Acknowledgments

Developed as part of SWECC Labs at the University of Washington.
