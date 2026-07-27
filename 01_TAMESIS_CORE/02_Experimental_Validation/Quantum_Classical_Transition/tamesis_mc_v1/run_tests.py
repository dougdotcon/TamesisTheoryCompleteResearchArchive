from __future__ import annotations

import subprocess

from config import reject_runtime_overrides


def main() -> None:
    reject_runtime_overrides()
    subprocess.run(["python", "-m", "pytest", "-q"], check=True)


if __name__ == "__main__":
    main()
