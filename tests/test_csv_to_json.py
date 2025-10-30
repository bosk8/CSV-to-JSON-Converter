import json
import pytest
from csv_to_json import parse_csv, convert_to_json, output_json


# Fixtures for creating temporary files
@pytest.fixture
def temp_csv_file(tmp_path):
    csv_content = "name,age,city\nJohn,25,New York\nJane,30,Los Angeles"
    csv_file = tmp_path / "input.csv"
    csv_file.write_text(csv_content)
    return csv_file


@pytest.fixture
def temp_empty_csv_file(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")
    return csv_file


@pytest.fixture
def temp_header_only_csv_file(tmp_path):
    csv_file = tmp_path / "header_only.csv"
    csv_file.write_text("name,age,city")
    return csv_file


@pytest.fixture
def temp_inconsistent_csv_file(tmp_path):
    csv_content = "name,age,city\nJohn,25\nJane,30,Los Angeles"
    csv_file = tmp_path / "inconsistent.csv"
    csv_file.write_text(csv_content)
    return csv_file


@pytest.fixture
def temp_large_csv_file(tmp_path):
    # Create a file larger than 10MB
    large_content = "a" * (11 * 1024 * 1024)
    csv_file = tmp_path / "large.csv"
    csv_file.write_text(large_content)
    return csv_file


# Tests for parse_csv function
def test_parse_csv_success(temp_csv_file):
    expected_data = [
        {"name": "John", "age": "25", "city": "New York"},
        {"name": "Jane", "age": "30", "city": "Los Angeles"},
    ]
    assert parse_csv(str(temp_csv_file)) == expected_data


def test_parse_csv_file_not_found():
    with pytest.raises(FileNotFoundError, match="CSV file not found."):
        parse_csv("non_existent_file.csv")


def test_parse_csv_empty_file(temp_empty_csv_file):
    with pytest.raises(ValueError, match="No data found in CSV."):
        parse_csv(str(temp_empty_csv_file))


def test_parse_csv_header_only(temp_header_only_csv_file):
    with pytest.raises(ValueError, match="No data found in CSV."):
        parse_csv(str(temp_header_only_csv_file))


def test_parse_csv_inconsistent_columns(temp_inconsistent_csv_file):
    with pytest.raises(ValueError, match="Row 2 has inconsistent column count."):
        parse_csv(str(temp_inconsistent_csv_file))


def test_parse_csv_file_too_large(temp_large_csv_file):
    with pytest.raises(ValueError, match="CSV file too large. Maximum size is 10MB."):
        parse_csv(str(temp_large_csv_file))


# Tests for convert_to_json function
def test_convert_to_json_pretty():
    csv_data = [{"name": "John", "age": "25"}]
    expected_json = json.dumps(csv_data, indent=4)
    assert convert_to_json(csv_data, pretty=True) == expected_json


def test_convert_to_json_compact():
    csv_data = [{"name": "John", "age": "25"}]
    expected_json = json.dumps(csv_data)
    assert convert_to_json(csv_data, pretty=False) == expected_json


# Tests for output_json function
def test_output_json_to_file(tmp_path):
    json_string = '{"key": "value"}'
    output_file = tmp_path / "output.json"
    output_json(json_string, str(output_file))
    assert output_file.read_text() == json_string


def test_output_json_to_stdout(capsys):
    json_string = '{"key": "value"}'
    output_json(json_string)
    captured = capsys.readouterr()
    assert captured.out.strip() == json_string
