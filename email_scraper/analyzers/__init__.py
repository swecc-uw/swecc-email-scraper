from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Type


class BaseAnalyzer(ABC):
    """Base class for all email analyzers.

    This class defines the interface that all analyzers must implement.
    Analyzers are responsible for extracting information from email data.
    """

    name: str = "base"  # override in subclasses
    description: str = "Base analyzer"  # override in subclasses

    def __init__(self, mbox_path: Path):
        """Initialize the analyzer.

        Args:
            mbox_path: Path to the mbox file to analyze
        """
        self.mbox_path = mbox_path

    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """Analyze the mbox file and return results.

        Returns:
            Dictionary containing analysis results
        """
        pass

    @classmethod
    def get_name(cls) -> str:
        """Get the name of this analyzer."""
        return cls.name


# registry of analyzers
ANALYZERS: Dict[str, Type[BaseAnalyzer]] = {}
