from typing import List, Dict, Any, Optional
import csv
import json
from pathlib import Path

def parse_csv(file_path: str) -> List[Dict[str, Any]]:
    input_path = Path(file_path)
    if not input_path.exists():
        raise FileNotFoundError("CSV file not found.")
    if input_path.stat().st_size > 10 * 1024 * 1024:
        raise ValueError("CSV file too large. Maximum size is 10MB.")
    csv_data: List[Dict[str, Any]] = []
    try:
        with open(input_path, "r", encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            if not reader.fieldnames:
                raise ValueError("No data found in CSV.")
            for row_num, row in enumerate(reader, start=2):
                if not any(value.strip() for value in row.values() if value):
                    continue
                if len(row) != len(reader.fieldnames):
                    raise ValueError(f"Row {row_num} has inconsistent column count.")
                csv_data.append(row)
        if not csv_data:
            raise ValueError("No data found in CSV.")
        return csv_data
    except csv.Error as e:
        raise csv.Error("Invalid CSV format.") from e

def convert_to_json(csv_data: List[Dict[str, Any]], pretty: bool = True) -> str:
    try:
        if pretty:
            return json.dumps(csv_data, indent=4, ensure_ascii=False)
        else:
            return json.dumps(csv_data, ensure_ascii=False)
    except TypeError as e:
        raise TypeError("Invalid data type in CSV.") from e
