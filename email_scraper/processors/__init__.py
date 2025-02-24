import mailbox
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from email.message import Message
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type


@dataclass
class EmailData:
    """parsed email data."""

    sender: str
    subject: str
    date: str
    content: str
    headers: Dict[str, str]
    raw_message: Message | None = None

    @property
    def parsed_date(self) -> Optional[datetime]:
        """Get the parsed datetime object from the date string.

        Returns:
            datetime object if date can be parsed, None otherwise
        """
        if not self.date:
            return None
        try:
            return parsedate_to_datetime(self.date)
        except (TypeError, ValueError):
            return None

    @classmethod
    def from_message(cls, message: Message) -> "EmailData":
        """Create EmailData from an email.message.Message.

        Args:
            message: Email message to parse

        Returns:
            EmailData object containing parsed message data
        """
        date = message.get("date", "")
        if isinstance(date, bytes):
            date = date.decode("utf-8")

        content = message.get_payload()
        text_content = ""

        if isinstance(content, list):
            # handle multipart messages by concatenating text parts
            parts = [part.get_payload() for part in content if isinstance(part, Message)]
            text_content = "\n".join(str(part) for part in parts)
        elif isinstance(content, bytes):
            text_content = content.decode("utf-8")
        else:
            text_content = str(content)

        return cls(
            sender=message.get("from", ""),
            subject=message.get("subject", ""),
            date=date,
            content=text_content,
            headers={k: str(v) for k, v in message.items()},
            raw_message=message,
        )


class EmailProcessor(ABC):
    """Base class for email processors.

    Each processor is responsible for a specific transformation or analysis
    of email data. Processors can be chained together to form a pipeline.
    """

    name: str  # must be overridden in subclasses
    description: str  # must be overridden in subclasses

    @abstractmethod
    def process(self, emails: List[EmailData]) -> Dict[str, Any]:
        """Process a list of emails and return results.

        Args:
            emails: List of EmailData objects to process

        Returns:
            Dictionary containing processing results
        """
        pass


class Pipeline:
    """Email processing pipeline.

    Combines multiple processors and executes them in sequence.
    Results from each processor are merged into the final output.
    """

    def __init__(self, processors: List[EmailProcessor]):
        """Initialize the pipeline with a list of processors."""
        self.processors = processors

    def process(self, mbox_path: Path) -> Dict[str, Any]:
        """Process an mbox file through all processors.

        Args:
            mbox_path: Path to the mbox file to process

        Returns:
            Combined results from all processors
        """
        mbox = mailbox.mbox(str(mbox_path))
        emails = [EmailData.from_message(msg) for msg in mbox]

        results = {}
        for processor in self.processors:
            results[processor.name] = processor.process(emails)

        return results

    def load_emails(self, mbox_path: Path) -> List[EmailData]:
        """Load emails from an mbox file.

        Args:
            mbox_path: Path to the mbox file to load

        Returns:
            List of EmailData objects
        """
        mbox = mailbox.mbox(str(mbox_path))
        return [EmailData.from_message(msg) for msg in mbox]


PROCESSORS: Dict[str, Type[EmailProcessor]] = {}
