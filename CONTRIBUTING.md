# Contributing to SWECC Email Scraper

Thank you for your interest in contributing to SWECC Email Scraper! This document provides comprehensive guidelines and instructions for contributing to the project.

## Table of Contents

- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Adding New Components](#adding-new-components)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Release Process](#release-process)

## Development Setup

1. Fork and clone the repository:

```bash
git clone https://github.com/<your-username>/swecc-email-scraper.git
cd swecc-email-scraper
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

3. Install development dependencies:

```bash
# install the package in editable mode with all dev dependencies
pip install -e ".[dev]"

# install pre-commit hooks
pre-commit install
```

4. Verify the installation:

```bash
# run the pre-commit checks
pre-commit run --all-files

# run tests
pytest
```

## Development Workflow

1. Create a new branch for your feature:

```bash
git checkout -b feature-name
```

2. Make your changes

3. Run quality checks locally:

```bash
# format code
black email_scraper

# run linting
ruff check email_scraper

# run type checking
mypy email_scraper

# run tests
pytest
```

4. Commit your changes:

```bash
git add .
git commit -m "Description of changes"
```

5. Push changes and create a pull request:

```bash
git push -u origin feature-name
```

## Code Style Guidelines

We use several tools to maintain code quality:

- **Black**: For code formatting
- **Ruff**: For linting and import sorting
- **MyPy**: For type checking

### Python Standards

1. Use type hints for all function arguments and return values:

```python
from typing import List, Dict, Any

def process_data(input_data: List[str]) -> Dict[str, Any]:
    ...
```

2. Write clear docstrings using Google style:

```python
def process_data(input_data: List[str]) -> Dict[str, Any]:
    """Process the input data and return results.

    Args:
        input_data: List of strings to process

    Returns:
        Dictionary containing processing results

    Raises:
        ValueError: If input_data is empty
    """
    ...
```

3. Follow PEP 8 guidelines (enforced by ruff)

## Adding New Components

### Adding a New Processor

1. Create a new file in `email_scraper/processors/`:

```python
from typing import Dict, Any, List
from email_scraper.processors import EmailProcessor, EmailData

class MyCustomProcessor(EmailProcessor):
    """Custom processor for specific analysis."""

    name = "my-processor"
    description = "Description of what my processor does"

    def process(self, emails: List[EmailData]) -> Dict[str, Any]:
        """Process emails and return results.

        Args:
            emails: List of emails to process

        Returns:
            Dictionary containing processing results
        """
        results = {}
        # Implementation here
        return results

# Register your processor
PROCESSORS[MyCustomProcessor.name] = MyCustomProcessor
```

2. Add tests in `tests/test_processors.py`

### Adding a New Formatter

1. Create a new file in `email_scraper/formatters/`:

```python
from typing import Dict, Any
from email_scraper.formatters import OutputFormatter

class MyCustomFormatter(OutputFormatter):
    """Custom output formatter."""

    name = "my-format"
    description = "Description of my output format"
    file_extension = "txt"

    def format(self, results: Dict[str, Any]) -> str:
        """Format results as a string.

        Args:
            results: Dictionary of results to format

        Returns:
            Formatted string
        """
        # Implementation here
        return formatted_string

# Register your formatter
FORMATTERS[MyCustomFormatter.name] = MyCustomFormatter
```

2. Add tests in `tests/test_formatters.py`

## Testing Guidelines

1. Write tests for all new functionality:

```python
import pytest
from email_scraper.processors import MyCustomProcessor

def test_my_processor():
    processor = MyCustomProcessor()
    result = processor.process([...])
    assert result["key"] == expected_value
```

2. Use fixtures for common test data:

```python
@pytest.fixture
def sample_emails():
    """Create sample EmailData objects for testing."""
    ...
```

3. Write clear and focused tests that verify specific functionality

## Documentation Guidelines

1. Update docstrings for all new code
2. Update README.md for user-facing changes
3. Update CONTRIBUTING.md for development-related changes
4. Add examples for new features

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. CI/CD will automatically publish to PyPI

## Best Practices

1. Keep processors focused on a single responsibility
2. Use type hints consistently
3. Write comprehensive tests
4. Document your code thoroughly
5. Follow the existing code style
6. Keep the code modular and maintainable

## Getting Help

- Create an issue for bugs or feature requests
- Join our discussions for questions
- Read our documentation

Thank you for contributing to SWECC Email Scraper!

## Pull Request Process

1. Update the README.md with details of significant changes
2. Update the version number in `pyproject.toml` following [semantic versioning](https://semver.org/)
3. Create a pull request with a clear description of the changes
4. Ensure all CI checks pass

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Questions?

Feel free to open an issue for any questions or concerns.
