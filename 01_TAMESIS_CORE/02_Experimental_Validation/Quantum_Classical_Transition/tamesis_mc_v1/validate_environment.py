from __future__ import annotations

import importlib.metadata as metadata
from pathlib import Path

from config import reject_runtime_overrides


LOCK = Path(__file__).resolve().parent / "requirements-lock.txt"


def main() -> None:
    reject_runtime_overrides()
    errors = []
    for line in LOCK.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        package, expected = line.split("==", 1)
        try:
            actual = metadata.version(package)
        except metadata.PackageNotFoundError:
            errors.append(f"missing dependency: {package}=={expected}")
            continue
        if actual != expected:
            errors.append(f"dependency drift: {package} expected {expected}, found {actual}")
    if errors:
        raise SystemExit("environment lock validation failed:\n- " + "\n- ".join(errors))
    print(f"environment lock verified: {LOCK.name}")


if __name__ == "__main__":
    main()
