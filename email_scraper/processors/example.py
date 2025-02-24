from collections import Counter
from datetime import datetime
from typing import Any, Dict, List

from . import EmailData, EmailProcessor


class ExampleProcessor(EmailProcessor):
    """Example processor that generates basic email statistics."""

    name = "example"
    description = "Example processor that generates basic email statistics."

    def process(self, emails: List[EmailData]) -> Dict[str, Any]:
        """Process emails and generate example statistics.

        Args:
            emails: List of emails to analyze

        Returns:
            Dictionary containing email statistics including:
            - total_messages: Total number of emails
            - unique_senders: Number of unique senders
            - top_senders: Most frequent senders with counts
            - date_range: Start and end dates of the email range
            - top_subjects: Most frequent subject lines with counts
        """
        senders: Counter[str] = Counter()
        dates: list[datetime] = []
        subjects: Counter[str] = Counter()

        for email in emails:
            if email.sender:
                senders[email.sender] += 1

            if parsed_date := email.parsed_date:
                dates.append(parsed_date)

            if email.subject:
                subjects[email.subject] += 1

        date_range: dict[str, Any] = {
            "start": None,
            "end": None,
        }
        if dates:
            date_range["start"] = min(dates).isoformat()
            date_range["end"] = max(dates).isoformat()

        return {
            "total_messages": len(emails),
            "unique_senders": len(senders),
            "top_senders": dict(senders.most_common(10)),
            "date_range": date_range,
            "top_subjects": dict(subjects.most_common(10)),
        }
