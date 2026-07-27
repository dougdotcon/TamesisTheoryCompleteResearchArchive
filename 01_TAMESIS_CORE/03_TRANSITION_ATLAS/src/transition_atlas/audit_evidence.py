from __future__ import annotations

import json
from pathlib import Path

from .loader import load_regimes, load_transitions
from .promotion import promotion_decision
from .provenance import write_sidecar
from .validator import validate


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    regimes = load_regimes(); transitions = load_transitions()
    findings = validate(regimes, transitions)
    decisions = [promotion_decision(t, t.epistemic_status) for t in transitions.values()]
    output = ROOT / "outputs" / "evidence_audit.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps({"findings": [f.__dict__ for f in findings], "promotion_decisions": decisions}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_sidecar(output, [], kind="evidence_audit")
    print(json.dumps({"errors": sum(f.severity == "error" for f in findings), "limitations": sum(f.severity == "limitation" for f in findings), "decisions": len(decisions)}, indent=2))
    if any(f.severity == "error" for f in findings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
