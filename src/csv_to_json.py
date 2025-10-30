#!/usr/bin/env python3
"""
CSV to JSON Converter CLI Tool

A lightweight, dependency-free Python CLI tool to convert CSV files to formatted JSON.
Uses only Python standard libraries for maximum compatibility.
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def main() -> None:
    """Main entry point for the CSV to JSON converter."""
    parser = create_argument_parser()
    args = parser.parse_args()

    try:
        # Parse CSV file
        csv_data = parse_csv(args.input)

        # Convert to JSON (pretty formatting unless --no-pretty is specified)
        pretty_format = not args.no_pretty
        json_output = convert_to_json(csv_data, pretty_format)

        # Output JSON
        output_json(json_output, args.output)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except csv.Error as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except TypeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Convert CSV files to JSON format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python csv_to_json.py -i input.csv
  python csv_to_json.py -i input.csv -o output.json
  python csv_to_json.py -i input.csv --no-pretty
        """,
    )

    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")

    parser.add_argument(
        "-o", "--output", help="Output JSON file path (default: stdout)"
    )

    parser.add_argument(
        "--no-pretty",
        action="store_true",
        help="Disable pretty JSON formatting (output compact JSON)",
    )

    return parser


def parse_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse CSV file and return list of dictionaries.

    Args:
        file_path (str): Path to the CSV file

    Returns:
        list: List of dictionaries where each dict represents a CSV row

    Raises:
        FileNotFoundError: If the input file doesn't exist
        csv.Error: If the CSV format is invalid
        ValueError: If the CSV is empty or has no headers
    """
    input_path = Path(file_path)

    # Check if file exists
    if not input_path.exists():
        raise FileNotFoundError("CSV file not found.")

    # Check file size (10MB limit for MVP)
    if input_path.stat().st_size > 10 * 1024 * 1024:  # 10MB
        raise ValueError("CSV file too large. Maximum size is 10MB.")

    csv_data: List[Dict[str, Any]] = []

    try:
        with open(input_path, "r", encoding="utf-8", newline="") as csvfile:
            reader = csv.reader(csvfile)

            # Get header
            try:
                header = next(reader)
            except StopIteration:
                raise ValueError("No data found in CSV.")

            # Read all rows
            for row_num, row in enumerate(
                reader, start=2
            ):  # Start at 2 (after header)
                # Skip completely empty rows
                if not any(field.strip() for field in row):
                    continue

                # Validate row has same number of fields as headers
                if len(row) != len(header):
                    raise ValueError(f"Row {row_num} has inconsistent column count.")

                csv_data.append(dict(zip(header, row)))

        # Check if we have any data
        if not csv_data:
            raise ValueError("No data found in CSV.")

        return csv_data

    except csv.Error as e:
        raise csv.Error("Invalid CSV format.") from e


def convert_to_json(csv_data: List[Dict[str, Any]], pretty: bool = True) -> str:
    """
    Convert CSV data to JSON string.

    Args:
        csv_data (list): List of dictionaries representing CSV rows
        pretty (bool): Whether to format JSON with indentation

    Returns:
        str: JSON string representation of the CSV data

    Raises:
        TypeError: If data contains non-serializable types
    """
    try:
        if pretty:
            return json.dumps(csv_data, indent=4, ensure_ascii=False)
        else:
            return json.dumps(csv_data, ensure_ascii=False)
    except TypeError as e:
        raise TypeError("Invalid data type in CSV.") from e


def output_json(json_string: str, output_path: Optional[str] = None) -> None:
    """
    Output JSON to file or stdout.

    Args:
        json_string (str): JSON string to output
        output_path (str, optional): Path to output file. If None, outputs to stdout.

    Raises:
        IOError: If unable to write to output file
    """
    try:
        if output_path:
            output_file = Path(output_path)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(json_string)
        else:
            print(json_string)
    except IOError as e:
        raise IOError(f"Unable to write to output file: {e}") from e


if __name__ == "__main__":
    main()
