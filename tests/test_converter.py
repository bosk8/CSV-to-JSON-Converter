import pytest
from src.converter import parse_csv, convert_to_json
import json


# Fixtures for creating temporary files
@pytest.fixture
def create_csv_file(tmp_path):
    def _create_csv_file(content):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(content)
        return str(csv_file)

    return _create_csv_file


# Basic success case: valid CSV to pretty JSON
def test_parse_csv_success(create_csv_file):
    content = "name,age\nAlice,30\nBob,25"
    csv_file = create_csv_file(content)
    expected = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
    assert parse_csv(csv_file) == expected


# Compact JSON output
def test_convert_to_json_compact(create_csv_file):
    content = "name,age\nAlice,30\nBob,25"
    csv_file = create_csv_file(content)
    data = parse_csv(csv_file)
    expected = json.dumps(
        [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
    )
    assert convert_to_json(data, pretty=False) == expected


# File not found error
def test_parse_csv_file_not_found():
    with pytest.raises(FileNotFoundError, match="CSV file not found."):
        parse_csv("non_existent_file.csv")


# Empty CSV file
def test_parse_csv_empty_file(create_csv_file):
    csv_file = create_csv_file("")
    with pytest.raises(ValueError, match="No data found in CSV."):
        parse_csv(csv_file)


# CSV with only headers
def test_parse_csv_only_headers(create_csv_file):
    csv_file = create_csv_file("name,age")
    with pytest.raises(ValueError, match="No data found in CSV."):
        parse_csv(csv_file)
