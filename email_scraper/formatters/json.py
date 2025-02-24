import json
from typing import Any, Dict

from . import OutputFormatter


class JsonFormatter(OutputFormatter):
    """Formats results as JSON."""

    name = "json"
    description = "Format results as JSON"
    file_extension = "json"

    def format(self, results: Dict[str, Any]) -> str:
        """Format results as a JSON string.

        Args:
            results: Dictionary of results to format

        Returns:
            JSON-formatted string
        """
        return json.dumps(results, indent=2)
