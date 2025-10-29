# CSV to JSON Converter

A lightweight, dependency-free Python CLI tool to convert CSV files to formatted JSON.

## Features

- **Simple CLI Interface**: Easy-to-use command-line interface
- **Flexible Output**: Output to file or stdout
- **Configurable Formatting**: Pretty-printed or compact JSON output
- **Robust Error Handling**: Clear error messages for common issues
- **File Size Validation**: Built-in 10MB file size limit
- **Dependency-Free**: Uses only Python standard library
- **Dynamic Delimiter Support**: Auto-detects common delimiters or accepts a custom one.
- **Selective Column Conversion**: Choose which columns to include in the output.
- **Automatic Type Inference**: Automatically converts numbers and booleans to their correct types.


## Installation

No installation required! Just ensure you have Python 3.6+ installed.

```bash
# Clone the repository
git clone https://github.com/bosk8/CSV-to-JSON-Converter.git
cd CSV-to-JSON-Converter
```

## Usage

### Basic Usage

```bash
# Convert CSV to JSON (output to stdout)
python src/csv_to_json.py -i input.csv

# Convert CSV to JSON (output to file)
python src/csv_to_json.py -i input.csv -o output.json

# Compact JSON output (no pretty formatting)
python src/csv_to_json.py -i input.csv --no-pretty
```

### Command Line Options

- `-i, --input`: Input CSV file path (required)
- `-o, --output`: Output JSON file path (optional, defaults to stdout)
- `--no-pretty`: Disable pretty JSON formatting (output compact JSON)
- `-d, --delimiter`: CSV delimiter (optional, defaults to auto-detect)
- `-c, --columns`: Comma-separated list of columns to include (optional)
- `--infer-types`: Automatically infer data types (e.g., numbers, booleans)
- `-h, --help`: Show help message

### Examples

```bash
# Basic conversion
python src/csv_to_json.py -i data.csv

# Save to file with pretty formatting
python src/csv_to_json.py -i data.csv -o result.json

# Compact output to file
python src/csv_to_json.py -i data.csv -o result.json --no-pretty

# Use a specific delimiter
python src/csv_to_json.py -i data.tsv -d "\\t"

# Select specific columns
python src/csv_to_json.py -i data.csv -c "name,city"

# Infer data types
python src/csv_to_json.py -i data.csv --infer-types
```

## Input Format

The tool expects CSV files with:
- Headers in the first row
- Comma-separated values (or other delimiter)
- UTF-8 encoding (recommended)

### Example CSV Input
```csv
name,age,city
John,25,New York
Jane,30,Los Angeles
Bob,35,Chicago
```

### Example JSON Output
```json
[
    {
        "name": "John",
        "age": "25",
        "city": "New York"
    },
    {
        "name": "Jane",
        "age": "30",
        "city": "Los Angeles"
    },
    {
        "name": "Bob",
        "age": "35",
        "city": "Chicago"
    }
]
```

## Error Handling

The tool provides clear error messages for common issues:

- **File not found**: `Error: CSV file not found.`
- **Empty file**: `Error: No data found in CSV.`
- **File too large**: `Error: CSV file too large. Maximum size is 10MB.`
- **Invalid CSV format**: `Error: Invalid CSV format.`
- **Inconsistent columns**: `Error: Row X has inconsistent column count.`

## Limitations

- Maximum file size: 10MB
- Requires headers in the first row

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
