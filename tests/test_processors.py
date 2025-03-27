import mailbox
from datetime import datetime, timedelta
from email.message import EmailMessage
from email.utils import format_datetime

import pytest

from email_scraper.processors import EmailData, Pipeline
from email_scraper.processors.classifier import EmailClassifier
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


@pytest.fixture
def sample_classify_emails():
    """
    emails to test all 5 types of keywords one by one as
    well as one email for something that requires human review
    """

    comfirmation_email = EmailMessage()
    comfirmation_email.add_header("from", "recruiter@company.com")
    comfirmation_email.add_header("to", "applicant@example.com")
    comfirmation_email.add_header("subject", "Thank you for applying!")
    comfirmation_email.add_header("date", format_datetime(datetime.now()))
    comfirmation_email.set_content(
        "Please note that your application to company XYZ has been accepted."
    )

    oa_email = EmailMessage()
    oa_email.add_header("from", "recruiter@company.com")
    oa_email.add_header("to", "applicant@example.com")
    oa_email.add_header("subject", "Online Assesment")
    oa_email.add_header("date", format_datetime(datetime.now()))
    oa_email.set_content("Dear Applicant\n\n A HackerRank has been sent out to you.")

    interview_email = EmailMessage()
    interview_email.add_header("from", "recruiter@company.com")
    interview_email.add_header("to", "applicant@example.com")
    interview_email.add_header("subject", "Your application to Intern Position")
    interview_email.add_header("date", format_datetime(datetime.now()))
    interview_email.set_content(
        "Dear Applicant\n\n Please reply with available times to schedule a call to discuss you experiences."
    )

    rejection_email = EmailMessage()
    rejection_email.add_header("from", "recruiter@company.com")
    rejection_email.add_header("to", "applicant@example.com")
    rejection_email.add_header("subject", "Your application to Intern Position")
    rejection_email.add_header("date", format_datetime(datetime.now()))
    rejection_email.set_content(
        "Dear Applicant\n\n Unfortunately, we are unable to offer you a position."
    )

    offer_email = EmailMessage()
    offer_email.add_header("from", "recruiter@company.com")
    offer_email.add_header("to", "applicant@example.com")
    offer_email.add_header("subject", "Job Offer at XYZ")
    offer_email.add_header("date", format_datetime(datetime.now()))
    offer_email.set_content(
        "Dear Applicant\n\n Congratulations! We are able to offer a position for you! "
    )

    other_email = EmailMessage()
    other_email.add_header("from", "recruiter@company.com")
    other_email.add_header("to", "applicant@example.com")
    other_email.add_header("subject", "Job Offer at XYZ")
    other_email.add_header("date", format_datetime(datetime.now()))
    other_email.set_content(
        "Dear Person\n\n After the previous interview, we were impressed but unfortunately we are unable to offer you a positon at company XYZ.  "
    )

    return [
        EmailData.from_message(comfirmation_email),
        EmailData.from_message(oa_email),
        EmailData.from_message(interview_email),
        EmailData.from_message(rejection_email),
        EmailData.from_message(offer_email),
        EmailData.from_message(other_email),
    ]


def test_classify_processor(sample_classify_emails):
    """Test the email classification processor."""
    processor = EmailClassifier()
    results = processor.process(sample_classify_emails)

    assert "classifications" in results
    classifications = results["classifications"]
    assert len(classifications) == 6

    # Test each email classification by index
    # Confirmation email
    assert classifications[0]["category"] == "Application confirmation"
    assert any(
        kw in classifications[0]["matched_keywords"]
        for kw in [
            "thank you for applying",
            "application received",
            "we have received your application",
        ]
    )
    assert classifications[0]["confidence"] > 0.5

    # OA/Hackerrank email
    assert classifications[1]["category"] == "OA invitation"
    assert "hackerrank" in classifications[1]["matched_keywords"]
    assert classifications[1]["confidence"] > 0.5

    # Interview email
    assert classifications[2]["category"] == "Interview request"
    assert any(
        kw in classifications[2]["matched_keywords"]
        for kw in [
            "interview",
            "schedule a call",
            "speak with you",
            "chat about your application",
        ]
    )
    assert classifications[2]["confidence"] > 0.5

    # Rejection email
    assert classifications[3]["category"] == "Rejection"
    assert "unfortunately" in classifications[3]["matched_keywords"]
    assert classifications[3]["confidence"] > 0.5

    # Offer email
    assert classifications[4]["category"] == "Offer"
    assert "congratulations" in classifications[4]["matched_keywords"]
    assert classifications[4]["confidence"] > 0.5

    # Mixed signals email
    assert classifications[5]["category"] == "Human Review Needed"
    assert classifications[5]["confidence"] <= 0.5
    assert len(classifications[5]["matched_keywords"]) >= 2
    assert "unfortunately" in classifications[5]["matched_keywords"]
    assert any(
        kw in classifications[5]["matched_keywords"]
        for kw in [
            "interview",
            "schedule a call",
            "speak with you",
            "chat about your application",
        ]
    )
