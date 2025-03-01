import json

import pytest

from email_scraper.formatters.json import JsonFormatter
from email_scraper.formatters.csv import CsvFormatter

@pytest.fixture
def sample_results():
    """create sample processing results for testing formatters."""
    return {
        "statistics": {
            "total_messages": 2,
            "unique_senders": 2,
            "top_senders": {"sender1@example.com": 1, "sender2@example.com": 1},
            "date_range": {
                "start": "2023-01-01T10:00:00+00:00",
                "end": "2023-01-02T11:00:00+00:00",
            },
            "top_subjects": {"Test Subject 1": 1, "Test Subject 2": 1},
        }
    }

def test_json_formatter(sample_results):
    """test json formatter output."""
    formatter = JsonFormatter()
    output = formatter.format(sample_results)

    parsed = json.loads(output)
    assert parsed == sample_results


def test_json_formatter_save(sample_results, tmp_path):
    """test saving json formatter output to file."""
    formatter = JsonFormatter()
    output_path = tmp_path / "test_output.json"

    formatter.save(sample_results, output_path)

    assert output_path.exists()
    with open(output_path) as f:
        saved_data = json.load(f)
    assert saved_data == sample_results

def test_csv_formatter(sample_results):
    """test csv formatter output."""
    formatter = CsvFormatter()
    output = formatter.format(sample_results)

    parsed = json.loads(output)
    assert parsed == sample_results