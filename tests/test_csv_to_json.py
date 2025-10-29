
import unittest
import os
import sys
import json
from pathlib import Path

# Add src directory to path to import csv_to_json
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from csv_to_json import parse_csv, convert_to_json

class TestCSVToJSON(unittest.TestCase):
    def setUp(self):
        # Create dummy CSV files for testing
        self.csv_data = {
            "simple.csv": "name,age,city\nJohn,25,New York\nJane,30,LA",
            "delimiter.csv": "name;age;city\nBob;35;Chicago\nAlice;28;SF",
            "types.csv": "name,score,active\nMax,100,true\nLeo,95.5,false",
            "empty.csv": "",
            "no_header.csv": "" # Empty file is a better test case
        }

        for filename, content in self.csv_data.items():
            with open(filename, 'w') as f:
                f.write(content)

    def tearDown(self):
        # Clean up dummy files
        for filename in self.csv_data.keys():
            if os.path.exists(filename):
                os.remove(filename)

    def test_parse_csv_simple(self):
        expected = [{'name': 'John', 'age': '25', 'city': 'New York'}, {'name': 'Jane', 'age': '30', 'city': 'LA'}]
        self.assertEqual(parse_csv('simple.csv'), expected)

    def test_delimiter_detection(self):
        expected = [{'name': 'Bob', 'age': '35', 'city': 'Chicago'}, {'name': 'Alice', 'age': '28', 'city': 'SF'}]
        self.assertEqual(parse_csv('delimiter.csv'), expected)

    def test_column_selection(self):
        expected = [{'name': 'John', 'city': 'New York'}, {'name': 'Jane', 'city': 'LA'}]
        self.assertEqual(parse_csv('simple.csv', columns=['name', 'city']), expected)

    def test_type_inference(self):
        csv_data = parse_csv('types.csv')
        json_output = convert_to_json(csv_data, infer_types=True, pretty=False)
        expected = [{"name": "Max", "score": 100, "active": True}, {"name": "Leo", "score": 95.5, "active": False}]
        self.assertEqual(json.loads(json_output), expected)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            parse_csv('non_existent_file.csv')

    def test_empty_csv(self):
        with self.assertRaises(ValueError):
            parse_csv('empty.csv')

if __name__ == '__main__':
    unittest.main()
