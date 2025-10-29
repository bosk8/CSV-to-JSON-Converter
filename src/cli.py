#!/usr/bin/env python3
"""
CSV to JSON Converter CLI Tool
"""

import argparse
import sys
from pathlib import Path
from converter import parse_csv, convert_to_json
from typing import Optional

def main() -> None:
    """Main entry point for the CSV to JSON converter."""
    parser = create_argument_parser()
    args = parser.parse_args()

    try:
        csv_data = parse_csv(args.input)
        pretty_format = not args.no_pretty
        json_output = convert_to_json(csv_data, pretty_format)
        output_json(json_output, args.output)
    except (FileNotFoundError, ValueError, TypeError, IOError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(description="Convert CSV files to JSON format")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-o", "--output", help="Output JSON file path (default: stdout)")
    parser.add_argument("--no-pretty", action="store_true", help="Disable pretty JSON formatting")
    return parser

def output_json(json_string: str, output_path: Optional[str] = None) -> None:
    """Output JSON to file or stdout."""
    try:
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(json_string)
        else:
            print(json_string)
    except IOError as e:
        raise IOError(f"Unable to write to output file: {e}") from e

if __name__ == "__main__":
    main()
