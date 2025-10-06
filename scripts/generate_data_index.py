import re
import json
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_FILE = Path("data-index.json")


def natural_sort_key(s: str):
    """
    Generate a key for natural sorting:
    Splits the string into numeric and non-numeric parts.
    Numeric parts are converted to int, text parts to lowercase.
    """
    parts = re.split(r"(\d+)", s)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def build_data_index():
    """
    Build a dictionary mapping subdirectory names to sorted file lists.
    """
    return {
        subdir.name: sorted(
            (f.name for f in subdir.iterdir() if f.is_file()), key=natural_sort_key
        )
        for subdir in sorted(DATA_DIR.iterdir(), key=lambda d: natural_sort_key(d.name))
        if subdir.is_dir()
    }


if __name__ == "__main__":
    data_index = build_data_index()
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(data_index, f, separators=(",", ":"))

    print(f"Data index written to {OUTPUT_FILE}")
