"""
Unit tests for CSV to JSON Converter.

Tests cover all major functionality including:
- CSV parsing
- JSON conversion
- Error handling
- CLI interface
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import csv_to_json


class TestParseCSV(unittest.TestCase):
    """Test CSV parsing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.sample_csv = self.test_data_dir / "sample.csv"

    def test_parse_valid_csv(self):
        """Test parsing a valid CSV file."""
        data = csv_to_json.parse_csv(str(self.sample_csv))
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["name"], "John")
        self.assertEqual(data[0]["age"], "25")
        self.assertEqual(data[0]["city"], "New York")

    def test_parse_csv_file_not_found(self):
        """Test parsing a non-existent file."""
        with self.assertRaises(FileNotFoundError):
            csv_to_json.parse_csv("nonexistent.csv")

    def test_parse_csv_empty_file(self):
        """Test parsing an empty CSV file (headers only)."""
        empty_csv = self.test_data_dir / "empty.csv"
        with self.assertRaises(ValueError) as context:
            csv_to_json.parse_csv(str(empty_csv))
        self.assertIn("No data found", str(context.exception))

    def test_parse_csv_too_large(self):
        """Test parsing a file that exceeds size limit."""
        # Create a temporary file larger than 10MB
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Write header
            f.write("name,age,city\n")
            # Write enough data to exceed 10MB
            large_row = "A" * 1000 + ",25,Test\n"
            for _ in range(11 * 1024):  # 11MB worth of data
                f.write(large_row)
            temp_path = f.name

        try:
            with self.assertRaises(ValueError) as context:
                csv_to_json.parse_csv(temp_path)
            self.assertIn("too large", str(context.exception).lower())
        finally:
            Path(temp_path).unlink()

    def test_parse_csv_inconsistent_columns(self):
        """Test parsing CSV with inconsistent column counts."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,age,city\n")
            f.write("John,25\n")  # Missing city column
            temp_path = f.name

        try:
            with self.assertRaises(ValueError) as context:
                csv_to_json.parse_csv(temp_path)
            self.assertIn("inconsistent column count", str(context.exception).lower())
        finally:
            Path(temp_path).unlink()


class TestConvertToJSON(unittest.TestCase):
    """Test JSON conversion functionality."""

    def test_convert_to_json_pretty(self):
        """Test converting to pretty-printed JSON."""
        data = [{"name": "John", "age": "25"}]
        result = csv_to_json.convert_to_json(data, pretty=True)
        self.assertIn("\n", result)
        self.assertIn("    ", result)  # Contains indentation
        parsed = json.loads(result)
        self.assertEqual(parsed, data)

    def test_convert_to_json_compact(self):
        """Test converting to compact JSON."""
        data = [{"name": "John", "age": "25"}]
        result = csv_to_json.convert_to_json(data, pretty=False)
        self.assertNotIn("\n", result)
        parsed = json.loads(result)
        self.assertEqual(parsed, data)

    def test_convert_to_json_with_unicode(self):
        """Test converting JSON with unicode characters."""
        data = [{"name": "José", "city": "São Paulo"}]
        result = csv_to_json.convert_to_json(data, pretty=True)
        self.assertIn("José", result)
        self.assertIn("São Paulo", result)
        parsed = json.loads(result)
        self.assertEqual(parsed, data)


class TestOutputJSON(unittest.TestCase):
    """Test JSON output functionality."""

    def test_output_to_stdout(self):
        """Test outputting JSON to stdout."""
        json_string = '{"test": "data"}'
        with patch('builtins.print') as mock_print:
            csv_to_json.output_json(json_string, output_path=None)
            mock_print.assert_called_once_with(json_string)

    def test_output_to_file(self):
        """Test outputting JSON to a file."""
        json_string = '{"test": "data"}'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            csv_to_json.output_json(json_string, output_path=temp_path)
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertEqual(content, json_string)
        finally:
            Path(temp_path).unlink()

    def test_output_to_invalid_path(self):
        """Test outputting to an invalid file path."""
        json_string = '{"test": "data"}'
        invalid_path = "/nonexistent/directory/file.json"
        with self.assertRaises(IOError):
            csv_to_json.output_json(json_string, output_path=invalid_path)


class TestCLI(unittest.TestCase):
    """Test command-line interface."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.sample_csv = self.test_data_dir / "sample.csv"

    def test_cli_with_input_only(self):
        """Test CLI with input file only (stdout output)."""
        with patch('builtins.print') as mock_print:
            with patch('sys.argv', ['csv_to_json.py', '-i', str(self.sample_csv)]):
                csv_to_json.main()
                mock_print.assert_called_once()
                output = mock_print.call_args[0][0]
                parsed = json.loads(output)
                self.assertEqual(len(parsed), 3)

    def test_cli_with_output_file(self):
        """Test CLI with input and output files."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            with patch('sys.argv', ['csv_to_json.py', '-i', str(self.sample_csv), '-o', temp_path]):
                csv_to_json.main()
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            self.assertEqual(len(content), 3)
        finally:
            Path(temp_path).unlink()

    def test_cli_no_pretty(self):
        """Test CLI with --no-pretty flag."""
        with patch('builtins.print') as mock_print:
            with patch('sys.argv', ['csv_to_json.py', '-i', str(self.sample_csv), '--no-pretty']):
                csv_to_json.main()
                output = mock_print.call_args[0][0]
                self.assertNotIn("\n", output)

    def test_cli_missing_input(self):
        """Test CLI with missing required input argument."""
        with patch('sys.argv', ['csv_to_json.py']):
            with self.assertRaises(SystemExit):
                csv_to_json.main()

    def test_cli_file_not_found(self):
        """Test CLI with non-existent input file."""
        with patch('sys.argv', ['csv_to_json.py', '-i', 'nonexistent.csv']):
            with patch('sys.exit') as mock_exit:
                csv_to_json.main()
                mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()

