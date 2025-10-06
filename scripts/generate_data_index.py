import json
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_FILE = Path("data-index.json")


def build_data_index():
    return {
        subdir.name: sorted(f.name for f in subdir.iterdir() if f.is_file())
        for subdir in sorted(DATA_DIR.iterdir(), key=lambda d: d.name)
        if subdir.is_dir()
    }


if __name__ == "__main__":
    data_index = build_data_index()
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(data_index, f, separators=(",", ":"))

    print(f"Data index written to {OUTPUT_FILE}")
