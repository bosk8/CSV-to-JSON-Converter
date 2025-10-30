# CSV to JSON Converter

A lightweight, dependency-free Python CLI tool to convert CSV files to formatted JSON.

## Features

- **Simple CLI Interface**: Easy-to-use command-line interface
- **Flexible Output**: Output to file or stdout
- **Configurable Formatting**: Pretty-printed or compact JSON output
- **Robust Error Handling**: Clear error messages for common issues
- **File Size Validation**: Built-in 10MB file size limit
- **Dependency-Free**: Uses only Python standard library
- **Comprehensive Testing**: Full test suite with 16+ test cases
- **CI/CD Integration**: Automated quality checks and testing

## Installation

No installation required! Just ensure you have Python 3.6+ installed.

```bash
# Clone the repository
git clone https://github.com/bosk8/CSV-to-JSON-Converter.git
cd CSV-to-JSON-Converter
```

### Development Setup

If you want to contribute or run tests, you can set up a development environment:

```bash
# Create a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install pytest pylint black ruff mypy

# Or install from requirements (if available)
pip install -r requirements-dev.txt
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
- `-h, --help`: Show help message

### Examples

```bash
# Basic conversion
python src/csv_to_json.py -i data.csv

# Save to file with pretty formatting
python src/csv_to_json.py -i data.csv -o result.json

# Compact output to file
python src/csv_to_json.py -i data.csv -o result.json --no-pretty
```

## Input Format

The tool expects CSV files with:
- Headers in the first row
- Comma-separated values
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

## Testing

The project includes a comprehensive test suite. Run tests using:

```bash
# Using pytest (recommended)
pytest tests/ -v

# Using unittest (fallback)
python -m unittest discover -s tests -v
```

### Test Coverage

The test suite includes:
- CSV parsing validation
- JSON conversion (pretty and compact)
- Error handling (file not found, empty files, invalid formats)
- CLI interface testing
- Edge cases (large files, inconsistent columns, unicode characters)

## Development

### Code Quality

This project uses several tools for code quality:

- **Black**: Code formatting (line length: 100)
- **Ruff**: Fast Python linter
- **Pylint**: Static code analysis
- **MyPy**: Type checking (optional, lenient mode)

### Running Quality Checks

```bash
# Format code with Black
black src/ tests/

# Check formatting (dry run)
black --check src/ tests/

# Run Ruff linter
ruff check src/ tests/

# Run Pylint
pylint src/csv_to_json.py

# Run MyPy type checker
mypy src/csv_to_json.py --ignore-missing-imports
```

### Pre-commit Hooks (Optional)

You can set up pre-commit hooks to automatically run checks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install
```

## Error Handling

The tool provides clear error messages for common issues:

- **File not found**: `Error: CSV file not found.`
- **Empty file**: `Error: No data found in CSV.`
- **File too large**: `Error: CSV file too large. Maximum size is 10MB.`
- **Invalid CSV format**: `Error: Invalid CSV format.`
- **Inconsistent columns**: `Error: Row X has inconsistent column count. Missing fields: ...`

## Limitations

- Maximum file size: 10MB
- All values are treated as strings (no type conversion)
- Requires headers in the first row
- Uses comma as the delimiter

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Project Structure

```
CSV-to-JSON-Converter/
├── src/
│   └── csv_to_json.py      # Main application code
├── tests/
│   ├── __init__.py
│   ├── test_csv_to_json.py  # Test suite
│   └── test_data/           # Test fixtures
│       ├── sample.csv
│       └── empty.csv
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD configuration
├── .gitignore               # Git ignore rules
├── pyproject.toml          # Project configuration
├── LICENSE                 # MIT License
└── README.md               # This file
```

## CI/CD

The project uses GitHub Actions for continuous integration:

- **Lint Job**: Runs code quality checks (Black, Ruff, Pylint, MyPy) across Python 3.6-3.13
- **Test Job**: Runs test suite across Python 3.6-3.13
- **Build Job**: Validates package build process

All checks must pass before merging pull requests.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Run tests** to ensure everything works (`pytest tests/ -v`)
5. **Run code quality checks** (`black --check .`, `ruff check .`)
6. **Commit your changes** with clear, descriptive messages
7. **Push to your branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

### Code Style

- Follow PEP 8 guidelines
- Use Black for formatting (line length: 100)
- Write docstrings for all functions and classes
- Add tests for new functionality
- Keep functions focused and small

### Commit Messages

Use clear, descriptive commit messages:
- `fix: description` - Bug fixes
- `feat: description` - New features
- `docs: description` - Documentation changes
- `test: description` - Test additions/changes
- `refactor: description` - Code refactoring
- `chore: description` - Maintenance tasks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

## Changelog

### Version 1.0.0
- Initial release
- Basic CSV to JSON conversion
- CLI interface
- Comprehensive test suite
- CI/CD integration
- Code quality tooling
