from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Type


class OutputFormatter(ABC):
    """Base class for output formatters.

    Formatters are responsible for converting processing results
    into different output formats (JSON, CSV, HTML, etc.).
    """

    name: str  # override in subclasses
    description: str  # description of what the formatter does
    file_extension: str  # default file extension for this format

    @abstractmethod
    def format(self, results: Dict[str, Any]) -> str:
        """Format processing results as a string.

        Args:
            results: Dictionary of processing results to format

        Returns:
            Formatted string representation
        """
        pass

    def save(self, results: Dict[str, Any], output_path: Path) -> None:
        """Save formatted results to a file.

        Args:
            results: Dictionary of processing results to format
            output_path: Path where to save the formatted output
        """
        formatted = self.format(results)
        with open(output_path, "w") as f:
            f.write(formatted)


# registry of formatters
FORMATTERS: Dict[str, Type[OutputFormatter]] = {}
