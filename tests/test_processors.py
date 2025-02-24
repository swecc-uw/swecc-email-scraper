import mailbox
from datetime import datetime, timedelta
from email.message import EmailMessage
from email.utils import format_datetime

import pytest

from email_scraper.processors import EmailData, Pipeline
from email_scraper.processors.example import ExampleProcessor


@pytest.fixture
def sample_dates():
    """create two dates for testing, one day apart."""
    base_date = datetime.now().replace(microsecond=0)
    next_date = base_date + timedelta(days=1)
    return base_date, next_date


@pytest.fixture
def sample_emails(sample_dates):
    """create sample emaildata objects for testing."""
    date1, date2 = sample_dates

    msg1 = EmailMessage()
    msg1.add_header("from", "sender1@example.com")
    msg1.add_header("subject", "Test Subject 1")
    msg1.add_header("date", format_datetime(date1))

    msg2 = EmailMessage()
    msg2.add_header("from", "sender2@example.com")
    msg2.add_header("subject", "Test Subject 2")
    msg2.add_header("date", format_datetime(date2))

    return [EmailData.from_message(msg1), EmailData.from_message(msg2)]


@pytest.fixture
def sample_mbox(tmp_path, sample_dates):
    """create a temporary mbox file with test data."""
    date1, date2 = sample_dates
    mbox_path = tmp_path / "test.mbox"
    mbox = mailbox.mbox(str(mbox_path))

    msg1 = EmailMessage()
    msg1.add_header("from", "sender1@example.com")
    msg1.add_header("subject", "Test Subject 1")
    msg1.add_header("date", format_datetime(date1))

    msg2 = EmailMessage()
    msg2.add_header("from", "sender2@example.com")
    msg2.add_header("subject", "Test Subject 2")
    msg2.add_header("date", format_datetime(date2))

    mbox.add(msg1)
    mbox.add(msg2)
    mbox.close()

    return mbox_path


def test_statistics_processor(sample_emails, sample_dates):
    """test the statistics processor."""
    date1, date2 = sample_dates
    processor = ExampleProcessor()
    results = processor.process(sample_emails)

    assert results["total_messages"] == 2
    assert results["unique_senders"] == 2
    assert len(results["top_senders"]) == 2
    assert results["top_senders"]["sender1@example.com"] == 1
    assert results["top_senders"]["sender2@example.com"] == 1

    assert results["date_range"]["start"] == date1.isoformat()
    assert results["date_range"]["end"] == date2.isoformat()


def test_pipeline_processing(sample_mbox):
    """test the complete processing pipeline."""
    pipeline = Pipeline([ExampleProcessor()])
    results = pipeline.process(sample_mbox)

    assert "example" in results
    stats = results["example"]
    assert stats["total_messages"] == 2
    assert stats["unique_senders"] == 2
    assert len(stats["top_senders"]) == 2

    assert stats["date_range"]["start"] is not None
    assert stats["date_range"]["end"] is not None

    start_date = datetime.fromisoformat(stats["date_range"]["start"])
    end_date = datetime.fromisoformat(stats["date_range"]["end"])
    assert end_date > start_date
    assert (end_date - start_date) == timedelta(days=1)


def test_email_data_creation(sample_dates):
    """test emaildata creation and date parsing."""
    date1, _ = sample_dates
    formatted_date = format_datetime(date1)

    msg = EmailMessage()
    msg.add_header("from", "test@example.com")
    msg.add_header("subject", "Test Subject")
    msg.add_header("date", formatted_date)
    msg.set_content("Test content")

    email_data = EmailData.from_message(msg)

    assert email_data.sender == "test@example.com"
    assert email_data.subject == "Test Subject"
    assert email_data.date == formatted_date
    assert "Test content" in email_data.content

    assert email_data.parsed_date is not None
    assert isinstance(email_data.parsed_date, datetime)
    assert email_data.parsed_date.replace(microsecond=0) == date1.replace(microsecond=0)
