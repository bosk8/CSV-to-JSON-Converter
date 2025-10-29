# CSV to JSON Converter

[![Python CI](https://github.com/bosk8/CSV-to-JSON-Converter/actions/workflows/ci.yml/badge.svg)](https://github.com/bosk8/CSV-to-JSON-Converter/actions/workflows/ci.yml)

A lightweight, dependency-free Python CLI tool to convert CSV files to formatted JSON.

## Features

- **Simple CLI Interface**: Easy-to-use command-line interface
- **Flexible Output**: Output to file or stdout
- **Configurable Formatting**: Pretty-printed or compact JSON output
- **Robust Error Handling**: Clear error messages for common issues
- **File Size Validation**: Built-in 10MB file size limit
- **Dependency-Free Core**: The core conversion logic uses only the Python standard library.

## Installation

The tool itself requires no installation. Just ensure you have Python 3.8+ installed.

```bash
# Clone the repository
git clone https://github.com/bosk8/CSV-to-JSON-Converter.git
cd CSV-to-JSON-Converter
```

## Usage

### Basic Usage

```bash
# Convert CSV to JSON (output to stdout)
python src/cli.py -i input.csv

# Convert CSV to JSON (output to file)
python src/cli.py -i input.csv -o output.json

# Compact JSON output (no pretty formatting)
python src/cli.py -i input.csv --no-pretty
```

### Command Line Options

- `-i, --input`: Input CSV file path (required)
- `-o, --output`: Output JSON file path (optional, defaults to stdout)
- `--no-pretty`: Disable pretty JSON formatting (output compact JSON)
- `-h, --help`: Show help message

## Development

To contribute to this project, you'll need to set up a development environment.

### Setup

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install pytest flake8 black mypy
```

### Running Tests

To run the test suite:

```bash
# Make sure the virtual environment is activated
PYTHONPATH=. pytest
```

### Linting and Formatting

This project uses `black` for formatting and `flake8` for linting.

```bash
# Format the code
black .

# Check for linting issues
flake8 .
```

### Static Analysis

This project uses `mypy` for static type checking.

```bash
mypy src/
```

## Continuous Integration

This repository uses GitHub Actions to automate testing, linting, and type checking for every push and pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please ensure that your changes pass all tests and linting checks before submitting a pull request.
