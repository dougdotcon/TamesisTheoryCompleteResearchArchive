#!/usr/bin/env python3
"""FOUND-SEMIGROUP-001 — auditoria computacional finita.

Verificação cruzada exaustiva do modelo cíclico de três regimes e três
transições, mais fixtures negativas que mostram que as propriedades não são
automáticas. COMPUTATIONAL_FINITE_CROSS_CHECK_ONLY: nada aqui promove um
resultado a teorema; a verificação formal é feita em Lean.
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

REGIMES = ["alpha", "beta", "gamma"]
SHIFTS = ["identity", "forward", "forward2"]

# Ação: apply[s][r] — determinística e total.
APPLY = {
    "identity": {"alpha": "alpha", "beta": "beta", "gamma": "gamma"},
    "forward": {"alpha": "beta", "beta": "gamma", "gamma": "alpha"},
    "forward2": {"alpha": "gamma", "beta": "alpha", "gamma": "beta"},
}


def comp(a: str, b: str) -> str:
    """Composição: `comp(a, b)` aplica `b` primeiro e depois `a` — a mesma
    convenção de `Shift3.comp` e da lei `mul_smul` da Mathlib."""
    table = {
        ("identity", "identity"): "identity",
        ("identity", "forward"): "forward",
        ("identity", "forward2"): "forward2",
        ("forward", "identity"): "forward",
        ("forward", "forward"): "forward2",
        ("forward", "forward2"): "identity",
        ("forward2", "identity"): "forward2",
        ("forward2", "forward"): "identity",
        ("forward2", "forward2"): "forward",
    }
    return table[(a, b)]


def check_closure() -> tuple[bool, list]:
    bad = [
        {"a": a, "b": b, "result": comp(a, b)}
        for a, b in product(SHIFTS, SHIFTS)
        if comp(a, b) not in SHIFTS
    ]
    return not bad, bad


def check_associativity() -> tuple[bool, list]:
    bad = [
        {"a": a, "b": b, "c": c}
        for a, b, c in product(SHIFTS, SHIFTS, SHIFTS)
        if comp(comp(a, b), c) != comp(a, comp(b, c))
    ]
    return not bad, bad


def check_left_identity() -> tuple[bool, list]:
    bad = [{"a": a} for a in SHIFTS if comp("identity", a) != a]
    return not bad, bad


def check_right_identity() -> tuple[bool, list]:
    bad = [{"a": a} for a in SHIFTS if comp(a, "identity") != a]
    return not bad, bad


def check_action_compatibility() -> tuple[bool, list]:
    bad = [
        {"a": a, "b": b, "r": r}
        for a, b, r in product(SHIFTS, SHIFTS, REGIMES)
        if APPLY[comp(a, b)][r] != APPLY[a][APPLY[b][r]]
    ]
    return not bad, bad


def check_faithful(action=None, shifts=None) -> tuple[bool, list]:
    action = action if action is not None else APPLY
    shifts = shifts if shifts is not None else SHIFTS
    bad = [
        {"a": a, "b": b}
        for a in shifts
        for b in shifts
        if a != b and all(action[a][r] == action[b][r] for r in REGIMES)
    ]
    return not bad, bad


def check_transitivity(action=None, shifts=None) -> tuple[bool, list]:
    action = action if action is not None else APPLY
    shifts = shifts if shifts is not None else SHIFTS
    bad = [
        {"from": x, "to": y}
        for x, y in product(REGIMES, REGIMES)
        if not any(action[s][x] == y for s in shifts)
    ]
    return not bad, bad


def negative_fixtures() -> dict:
    """Fixtures que mostram que as propriedades NÃO são automáticas.
    Aqui espera-se encontrar contraexemplos; encontrá-los é o resultado
    correto destas verificações."""
    out: dict = {}

    # 1. Operação finita não associativa: subtração truncada em {0,1,2}.
    trunc_sub = lambda a, b: max(a - b, 0)  # noqa: E731
    non_assoc = [
        {"a": a, "b": b, "c": c,
         "left": trunc_sub(trunc_sub(a, b), c),
         "right": trunc_sub(a, trunc_sub(b, c))}
        for a, b, c in product(range(3), repeat=3)
        if trunc_sub(trunc_sub(a, b), c) != trunc_sub(a, trunc_sub(b, c))
    ]
    out["non_associative_operation"] = {
        "description": "subtração truncada em {0,1,2}",
        "counterexamples_found": len(non_assoc),
        "first_counterexample": non_assoc[0] if non_assoc else None,
        "expected_failure_observed": bool(non_assoc),
    }

    # 2. Ação incompatível com a composição: forward2 forçada a agir como
    # identidade, mantendo a tabela de composição original.
    broken_apply = {**APPLY, "forward2": {r: r for r in REGIMES}}
    incompat = [
        {"a": a, "b": b, "r": r}
        for a, b, r in product(SHIFTS, SHIFTS, REGIMES)
        if broken_apply[comp(a, b)][r] != broken_apply[a][broken_apply[b][r]]
    ]
    out["incompatible_action"] = {
        "description": "forward2 agindo como identidade sob a mesma composição",
        "counterexamples_found": len(incompat),
        "first_counterexample": incompat[0] if incompat else None,
        "expected_failure_observed": bool(incompat),
    }

    # 3. Sistema de transições não transitivo: somente {identity}.
    ok_trans, non_trans = check_transitivity(shifts=["identity"])
    out["non_transitive_system"] = {
        "description": "subsistema contendo apenas a transição identity",
        "unreachable_pairs": len(non_trans),
        "first_counterexample": non_trans[0] if non_trans else None,
        "expected_failure_observed": not ok_trans,
    }

    # 4. Representação não fiel: identity e forward2 mapeadas para a mesma
    # função (identidade em todos os regimes).
    unfaithful_action = {
        "identity": {r: r for r in REGIMES},
        "forward": APPLY["forward"],
        "forward2": {r: r for r in REGIMES},
    }
    ok_faith, collisions = check_faithful(action=unfaithful_action)
    out["unfaithful_representation"] = {
        "description": "identity e forward2 com a mesma ação",
        "colliding_pairs": len(collisions),
        "first_counterexample": collisions[0] if collisions else None,
        "expected_failure_observed": not ok_faith,
    }

    return out


def main() -> int:
    checks = {}
    all_ok = True
    for name, fn in [
        ("closure", check_closure),
        ("associativity", check_associativity),
        ("left_identity", check_left_identity),
        ("right_identity", check_right_identity),
        ("action_compatibility", check_action_compatibility),
        ("faithful_action", check_faithful),
        ("transitivity", check_transitivity),
    ]:
        ok, bad = fn()
        checks[name] = {"status": "PASS" if ok else "FAIL",
                        "counterexamples": bad}
        all_ok = all_ok and ok

    result = {
        "schema": "tamesis-computational-audit/1",
        "work_item": "FOUND-SEMIGROUP-001",
        "classification": "COMPUTATIONAL_FINITE_CROSS_CHECK_ONLY",
        "note": "Verificação cruzada finita; não promove resultado a teorema.",
        "composition_convention": "comp(a, b) aplica b primeiro e depois a",
        "model_size": {"regimes": len(REGIMES), "transitions": len(SHIFTS)},
        "checks": checks,
        "counterexamples_found": sum(
            len(c["counterexamples"]) for c in checks.values()
        ),
        "negative_fixtures": negative_fixtures(),
        "status": "PASS" if all_ok else "FAIL",
    }

    results_dir = Path(__file__).resolve().parents[2] / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    out_path = results_dir / "FOUND-SEMIGROUP-001-computational-audit.json"
    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"audit_status={result['status']}")
    print(f"result_written={out_path}")
    negatives = result["negative_fixtures"]
    negatives_ok = all(v["expected_failure_observed"] for v in negatives.values())
    print(f"negative_fixtures_behaved_as_expected={negatives_ok}")
    return 0 if all_ok and negatives_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
