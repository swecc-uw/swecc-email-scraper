import csv
import io
import json
from typing import Any

import click
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

def flatten_dict(sample_results):
    new_dict = {}
    for key,value in sample_results.items():
        if isinstance(value,dict) and value:
            new_dict[key] = next(iter(value.values()))
        else:
            new_dict[key] = value
    return new_dict

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

def test_csv_formatter_unchecked(sample_results):
    """test csv formatter(uncheked) output."""
    formatter = CsvFormatter()
    parsed = formatter.format(sample_results,True)
    col = list(sample_results.keys())
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=col) 
    writer.writeheader()
    writer.writerow(sample_results)
    assert parsed == output.getvalue()

def test_csv_formatter_checked_invalid(sample_results):
    """test csv formatter(cheked) for nested input."""
    formatter = CsvFormatter()
    with pytest.raises(click.Abort):
        formatter.format(sample_results,False)

def test_csv_formatter_checked_valid(sample_results):
    """test csv formatter(cheked) for un-nested input."""
    formatter = CsvFormatter()
    flat_results = flatten_dict(sample_results)
    parsed = formatter.format(flat_results,True)
    col = list(flat_results.keys())
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=col) 
    writer.writeheader()
    writer.writerow(flat_results)
    assert parsed == output.getvalue()