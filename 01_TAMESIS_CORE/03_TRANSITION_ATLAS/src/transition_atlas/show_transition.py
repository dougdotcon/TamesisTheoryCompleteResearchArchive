from __future__ import annotations

import json
import sys

from .loader import load_transitions


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m transition_atlas.show_transition TRANSITION_ID")
    transition = load_transitions().get(sys.argv[1])
    if transition is None:
        raise SystemExit(f"unknown transition: {sys.argv[1]}")
    print(json.dumps(transition.model_dump(mode="json"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
