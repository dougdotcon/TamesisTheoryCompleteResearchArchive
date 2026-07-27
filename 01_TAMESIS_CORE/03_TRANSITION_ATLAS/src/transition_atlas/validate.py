from __future__ import annotations

import json

from .loader import load_evidence, load_protocols, load_regimes, load_transitions
from .validator import validate


def main() -> None:
    regimes = load_regimes(); transitions = load_transitions(); evidence = load_evidence(); protocols = load_protocols()
    findings = validate(regimes, transitions)
    payload = {"regimes": len(regimes), "transitions": len(transitions), "evidence": len(evidence), "protocols": len(protocols), "findings": [f.__dict__ for f in findings]}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    if any(f.severity == "error" for f in findings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
