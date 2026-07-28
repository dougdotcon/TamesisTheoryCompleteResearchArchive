import json
from pathlib import Path

from labctl import validate


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = validate()
    (root / "dashboard.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(root / "dashboard.json")
