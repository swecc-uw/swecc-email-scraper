from typing import Any, Dict

import yaml
from rich.console import Console

from . import OutputFormatter

console = Console(stderr=True)  # use stderr for status messages


class YamlFormatter(OutputFormatter):
    """Formats results as CSV."""

    name = "yaml"
    description = "Format results as YAML"
    file_extension = "yaml"

    def format(self, results: Dict[str, Any], **kwargs: Dict[str, Any]) -> str:
        """Format results as a CSV string.

        Args:
            results: Dictionary of results to format

        Returns:
            CSV-formatted string
        """
        return yaml.dump(results, indent=2)
