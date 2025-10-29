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


def main():
    """Main entry point for the CSV to JSON converter."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        # Parse CSV file
        columns = args.columns.split(',') if args.columns else None
        csv_data = parse_csv(args.input, args.delimiter, columns)
        
        # Convert to JSON (pretty formatting unless --no-pretty is specified)
        pretty_format = not args.no_pretty
        json_output = convert_to_json(csv_data, pretty_format, args.infer_types)
        
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


def create_argument_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Convert CSV files to JSON format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python csv_to_json.py -i input.csv
  python csv_to_json.py -i input.csv -o output.json
  python csv_to_json.py -i input.csv --no-pretty
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input CSV file path'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output JSON file path (default: stdout)'
    )
    
    parser.add_argument(
        '--no-pretty',
        action='store_true',
        help='Disable pretty JSON formatting (output compact JSON)'
    )
    
    parser.add_argument(
        '-d', '--delimiter',
        help='CSV delimiter (default: auto-detect)'
    )

    parser.add_argument(
        '-c', '--columns',
        help='Comma-separated list of columns to include'
    )

    parser.add_argument(
        '--infer-types',
        action='store_true',
        help='Automatically infer data types (e.g., numbers, booleans)'
    )

    return parser


def detect_delimiter(file_path):
    """
    Detect CSV delimiter by sniffing the first few lines.

    Args:
        file_path (Path): Path to the CSV file

    Returns:
        str: Detected delimiter
    """
    with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
        try:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            return dialect.delimiter
        except csv.Error:
            # Default to comma if detection fails
            return ','


def parse_csv(file_path, delimiter=None, columns=None):
    """
    Parse CSV file and return list of dictionaries.
    
    Args:
        file_path (str): Path to the CSV file
        delimiter (str, optional): CSV delimiter. Auto-detected if not provided.
        columns (list, optional): List of column names to include.
        
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
    
    # Detect delimiter if not provided
    if delimiter is None:
        delimiter = detect_delimiter(input_path)

    csv_data = []
    
    try:
        with open(input_path, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            
            # Check if we have headers
            if not reader.fieldnames:
                raise ValueError("No data found in CSV.")
            
            # Read all rows
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                # Skip completely empty rows
                if not any(value.strip() for value in row.values() if value):
                    continue
                
                # Validate row has same number of fields as headers
                if len(row) != len(reader.fieldnames):
                    raise ValueError(f"Row {row_num} has inconsistent column count.")
                
                # Filter columns if specified
                if columns:
                    # Validate column names
                    invalid_columns = set(columns) - set(reader.fieldnames)
                    if invalid_columns:
                        raise ValueError(f"Invalid column(s): {', '.join(invalid_columns)}")

                    # Create a new dict with only the selected columns
                    filtered_row = {col: row[col] for col in columns if col in row}
                    csv_data.append(filtered_row)
                else:
                    csv_data.append(row)
        
        # Check if we have any data
        if not csv_data:
            raise ValueError("No data found in CSV.")
        
        return csv_data
        
    except csv.Error as e:
        raise csv.Error("Invalid CSV format.") from e


def _infer_type(value):
    """
    Infers the type of a string value.

    Args:
        value (str): The string value to inspect.

    Returns:
        int, float, bool, or str: The inferred type.
    """
    if not isinstance(value, str):
        return value

    # Try integer
    if value.isdigit():
        return int(value)

    # Try float
    try:
        return float(value)
    except ValueError:
        pass

    # Try boolean
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'

    return value


def convert_to_json(csv_data, pretty=True, infer_types=False):
    """
    Convert CSV data to JSON string.
    
    Args:
        csv_data (list): List of dictionaries representing CSV rows
        pretty (bool): Whether to format JSON with indentation
        infer_types (bool): Whether to automatically infer data types
        
    Returns:
        str: JSON string representation of the CSV data
        
    Raises:
        TypeError: If data contains non-serializable types
    """
    if infer_types:
        csv_data = [{k: _infer_type(v) for k, v in row.items()} for row in csv_data]

    try:
        if pretty:
            return json.dumps(csv_data, indent=4, ensure_ascii=False)
        else:
            return json.dumps(csv_data, ensure_ascii=False)
    except TypeError as e:
        raise TypeError("Invalid data type in CSV.") from e


def output_json(json_string, output_path=None):
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
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_string)
        else:
            print(json_string)
    except IOError as e:
        raise IOError(f"Unable to write to output file: {e}") from e


if __name__ == '__main__':
    main()
