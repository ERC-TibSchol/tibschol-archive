import json
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_FILE = Path("data-index.json")


def build_data_index():
    data_index = {}
    for subdir in DATA_DIR.iterdir():
        if subdir.is_dir():
            files = [f.name for f in subdir.iterdir() if f.is_file()]
            data_index[subdir.name] = files
    return data_index


if __name__ == "__main__":
    data_index = build_data_index()
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(data_index, f, separators=(",", ":"))

    print(f"Data index written to {OUTPUT_FILE}")
