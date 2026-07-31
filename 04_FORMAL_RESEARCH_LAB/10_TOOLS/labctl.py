#!/usr/bin/env python3
"""Continuity and validation tool for Tamesis Formal Research Lab."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
    from jsonschema import validate as jsonschema_validate
except ImportError as exc:  # pragma: no cover - reported by the CLI
    print(f"DEPENDENCY_ERROR: {exc}", file=sys.stderr)
    raise


TOOLS_DIR = Path(__file__).resolve().parent
LAB_ROOT = TOOLS_DIR.parent
REPO_ROOT = LAB_ROOT.parent
SCHEMA_DIR = LAB_ROOT / "00_GOVERNANCE" / "schemas"
ALLOWED_WORK_STATUS = {
    "UNSCOPED",
    "SCOPED",
    "READY",
    "IN_PROGRESS",
    "BLOCKED",
    "FAILED",
    "REFUTED",
    "PARTIAL_RESULT",
    "FROZEN_PARTIAL_RESULT",
    "VERIFIED",
    "EXTERNALLY_REVIEWED",
    "RETRACTED",
    "ARCHIVED",
}
EVIDENCE_LEVELS = set("HFCOPEITN")


def normalize_yaml(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: normalize_yaml(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_yaml(item) for item in value]
    return value


def read_yaml(path: Path) -> Any:
    return normalize_yaml(yaml.safe_load(path.read_text(encoding="utf-8")) or {})


def read_front_matter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"missing YAML front matter: {path}")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError(f"malformed YAML front matter: {path}")
    data = normalize_yaml(yaml.safe_load(match.group(1)) or {})
    if not isinstance(data, dict):
        raise ValueError(f"front matter is not a mapping: {path}")
    return data, match.group(2)


CANONICAL_COMMIT_PASS = "PASS"
CANONICAL_COMMIT_UNAVAILABLE = "CANONICAL_COMMIT_UNAVAILABLE"
CANONICAL_COMMIT_NOT_ANCESTOR = "CANONICAL_COMMIT_NOT_ANCESTOR"
CANONICAL_COMMIT_GIT_ERROR = "CANONICAL_COMMIT_GIT_ERROR"

SHALLOW_CLONE_HINT = (
    "complete the git history (git fetch --unshallow); a shallow clone that "
    "lacks the canonical commit is not a valid canonical environment"
)


def git_exit_code(args: list[str]) -> int:
    """Run a git command in REPO_ROOT and return only its exit code."""
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    ).returncode


def check_canonical_commit(
    canonical_commit: str | None,
    runner: Any = None,
) -> dict[str, Any]:
    """Non-destructive validation of LAB_STATE.canonical_commit.

    The commit must exist as a commit object and must be an ancestor of HEAD.
    Equality with HEAD is ACCEPTED: at the start of a session the canonical
    commit is normally the current HEAD. Strict ancestry is deliberately NOT
    implemented.

    `runner` takes a git argument list and returns an exit code; it is
    injected so the decision table can be unit tested without touching the
    repository.
    """
    run = git_exit_code if runner is None else runner
    if not canonical_commit:
        return {
            "status": CANONICAL_COMMIT_UNAVAILABLE,
            "canonical_commit": canonical_commit,
            "message": "LAB_STATE.canonical_commit is missing or empty",
        }

    exists = run(["git", "cat-file", "-e", f"{canonical_commit}^{{commit}}"])
    if exists != 0:
        return {
            "status": CANONICAL_COMMIT_UNAVAILABLE,
            "canonical_commit": canonical_commit,
            "exit_code": exists,
            "message": (
                f"canonical_commit {canonical_commit} is not available as a "
                f"commit object; {SHALLOW_CLONE_HINT}"
            ),
        }

    ancestry = run(["git", "merge-base", "--is-ancestor", canonical_commit, "HEAD"])
    if ancestry == 0:
        return {
            "status": CANONICAL_COMMIT_PASS,
            "canonical_commit": canonical_commit,
            "message": "canonical_commit exists and is an ancestor of HEAD (equality accepted)",
        }
    if ancestry == 1:
        return {
            "status": CANONICAL_COMMIT_NOT_ANCESTOR,
            "canonical_commit": canonical_commit,
            "exit_code": ancestry,
            "message": (
                f"canonical_commit {canonical_commit} exists but is not an "
                "ancestor of HEAD"
            ),
        }
    return {
        "status": CANONICAL_COMMIT_GIT_ERROR,
        "canonical_commit": canonical_commit,
        "exit_code": ancestry,
        "message": (
            f"git merge-base --is-ancestor failed with exit code {ancestry}; "
            "this is a git or environment error, NOT a non-ancestry verdict"
        ),
    }


def git_status() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def all_changes_are_in_lab(status_lines: list[str]) -> bool:
    for line in status_lines:
        path_text = line[3:].strip()
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        path_text = path_text.strip('"').replace("\\", "/")
        if not path_text.startswith("04_FORMAL_RESEARCH_LAB/"):
            return False
    return True


def validate_json_schema(data: Any, schema_name: str, label: str) -> list[str]:
    schema = json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))
    try:
        jsonschema_validate(instance=data, schema=schema)
    except Exception as exc:  # jsonschema.ValidationError without hard dependency in typing
        return [f"{label}: {exc.message if hasattr(exc, 'message') else exc}"]
    return []


def required_paths() -> list[Path]:
    return [
        LAB_ROOT / "README.md",
        LAB_ROOT / "LAB_STATE.md",
        LAB_ROOT / "CHANGELOG.md",
        LAB_ROOT / "AGENTS.md",
        LAB_ROOT / "00_GOVERNANCE" / "DOCUMENT_PRECEDENCE.md",
        LAB_ROOT / "00_GOVERNANCE" / "STATUS_POLICY.md",
        LAB_ROOT / "00_GOVERNANCE" / "CLAIM_LEDGER.yaml",
        LAB_ROOT / "00_GOVERNANCE" / "DECISION_LEDGER.yaml",
        LAB_ROOT / "00_GOVERNANCE" / "BIBLIOGRAPHY_LEDGER.yaml",
        LAB_ROOT / "00_GOVERNANCE" / "ARTIFACT_REGISTRY.yaml",
        LAB_ROOT / "01_PORTFOLIO" / "RESEARCH_QUEUE.yaml",
        LAB_ROOT / "05_FORMAL" / "lean" / "lakefile.toml",
        LAB_ROOT / "05_FORMAL" / "lean" / "lean-toolchain",
        LAB_ROOT / "05_FORMAL" / "specifications" / "LAB-BENCH-001.md",
        LAB_ROOT / "05_FORMAL" / "specifications" / "LAB-BENCH-001_STATUS.yaml",
        LAB_ROOT / "03_MILLENNIUM" / "00_POINCARE_BENCHMARK"
        / "POINCARE_VERIFICATION_BENCHMARK.md",
        LAB_ROOT / "06_COMPUTATION" / "python" / "pyproject.toml",
        LAB_ROOT / "10_TOOLS" / "labctl.py",
        LAB_ROOT / "90_LEGACY_MAP" / "LEGACY_INDEX.yaml",
        LAB_ROOT / "90_LEGACY_MAP" / "DUPLICATE_PAPERS.yaml",
    ]


def lean_check() -> dict[str, Any]:
    lean_root = LAB_ROOT / "05_FORMAL" / "lean"
    lean = shutil.which("lean")
    lake = shutil.which("lake")
    elan_home = os.environ.get("ELAN_HOME")
    if elan_home:
        toolchain_root = Path(elan_home) / "toolchains"
    else:
        home = os.environ.get("USERPROFILE") or os.environ.get("HOME")
        toolchain_root = (Path(home) if home else Path.home()) / ".elan" / "toolchains"
    installed_toolchains = [
        p for p in toolchain_root.iterdir()
        if p.is_dir() and not p.name.endswith(".lock")
    ] if toolchain_root.is_dir() else []
    stable_toolchains = [
        p for p in installed_toolchains
        if not p.name.endswith(".tmp") and ".tmp" not in p.name
    ]
    if not lean or not lake or not installed_toolchains:
        return {
            "status": "BLOCKED",
            "lean": lean,
            "lake": lake,
            "installed_toolchains": [p.name for p in installed_toolchains],
            "stable_toolchains": [p.name for p in stable_toolchains],
            "toolchain_stability": "PARTIAL" if installed_toolchains else "NOT_STARTED",
            "message": "Lean/lake toolchain unavailable; no build attempted.",
        }
    version = subprocess.run(
        [lean, "--version"], cwd=lean_root, text=True, capture_output=True, check=False,
        timeout=20,
    )
    stable = bool(stable_toolchains) and ".tmp" not in str(lean).lower()
    return {
        "status": "PASS" if stable else "NOT_RUN",
        "toolchain_stability": "PASS" if stable else "PARTIAL",
        "lean_path": lean,
        "lake_path": lake,
        "stable_toolchains": [p.name for p in stable_toolchains],
        "lean_version": version.stdout.strip(),
        "lean_version_exit": version.returncode,
        "lake_build_exit": None,
        "lake_build_stdout": "",
        "lake_build_stderr": "",
        "message": (
            "Structural validation confirms a stable, non-.tmp Lean toolchain resolved from PATH; "
            "it never invokes lake build. Compilation evidence comes from the immutable gate result."
        ),
    }


def validate() -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    for path in required_paths():
        if not path.exists():
            errors.append(f"missing required path: {path.relative_to(REPO_ROOT)}")

    state: dict[str, Any] = {}
    if (LAB_ROOT / "LAB_STATE.md").exists():
        try:
            state, _ = read_front_matter(LAB_ROOT / "LAB_STATE.md")
            errors.extend(validate_json_schema(state, "lab-state.schema.json", "LAB_STATE"))
        except Exception as exc:
            errors.append(str(exc))

    queue = read_yaml(LAB_ROOT / "01_PORTFOLIO" / "RESEARCH_QUEUE.yaml")
    items = queue.get("queue", [])
    item_ids = [item.get("work_item_id") for item in items]
    if len(item_ids) != len(set(item_ids)):
        errors.append("RESEARCH_QUEUE has duplicate work_item_id")
    item_set = set(item_ids)
    for item in items:
        errors.extend(
            validate_json_schema(item, "work-item.schema.json", item.get("work_item_id", "work-item"))
        )
        if item.get("status") not in ALLOWED_WORK_STATUS:
            errors.append(f"invalid work status: {item.get('work_item_id')}")
        for dependency in item.get("dependencies", []):
            if dependency not in item_set:
                errors.append(f"unknown dependency {dependency} in {item.get('work_item_id')}")
    active = state.get("active_work_item")
    if active and active not in item_set:
        errors.append(f"active_work_item not in queue: {active}")
    item_by_id = {item.get("work_item_id"): item for item in items}
    active_item = item_by_id.get(active)
    if active_item and state.get("work_status") != active_item.get("status"):
        errors.append("LAB_STATE work_status differs from active queue item")

    benchmark = item_by_id.get("LAB-BENCH-001", {})
    rh_nogo = item_by_id.get("RH-NOGO-001", {})
    semigroup = item_by_id.get("FOUND-SEMIGROUP-001", {})
    if active not in {"LAB-BENCH-001", "FOUND-SEMIGROUP-001", "RH-NOGO-001",
                      "FOUND-SEMIGROUP-002", "FOUND-FUNCTIONAL-GRAPH-001",
                      "FOUND-CYCLE-DETECTION-001"}:
        errors.append(
            "gate sequence requires LAB-BENCH-001, FOUND-SEMIGROUP-001, RH-NOGO-001, "
            "FOUND-SEMIGROUP-002, FOUND-FUNCTIONAL-GRAPH-001 or "
            "FOUND-CYCLE-DETECTION-001 as active_work_item"
        )
    if active == "FOUND-SEMIGROUP-001" and benchmark.get("status") != "VERIFIED":
        errors.append("FOUND-SEMIGROUP-001 cannot be active before LAB-BENCH-001 is VERIFIED")
    if active == "RH-NOGO-001" and semigroup.get("status") != "VERIFIED":
        errors.append("RH-NOGO-001 cannot be active before FOUND-SEMIGROUP-001 is VERIFIED")
    if active == "FOUND-SEMIGROUP-002" and semigroup.get("status") != "VERIFIED":
        errors.append("FOUND-SEMIGROUP-002 cannot be active before FOUND-SEMIGROUP-001 is VERIFIED")
    fs2 = item_by_id.get("FOUND-SEMIGROUP-002", {})
    if active == "FOUND-FUNCTIONAL-GRAPH-001" and fs2.get("status") != "VERIFIED":
        errors.append("FOUND-FUNCTIONAL-GRAPH-001 cannot be active before FOUND-SEMIGROUP-002 is VERIFIED")
    ffg = item_by_id.get("FOUND-FUNCTIONAL-GRAPH-001", {})
    if active == "FOUND-CYCLE-DETECTION-001" and ffg.get("status") != "VERIFIED":
        errors.append("FOUND-CYCLE-DETECTION-001 cannot be active before FOUND-FUNCTIONAL-GRAPH-001 is VERIFIED")
    if state.get("authorized_action") not in {
        "LAB_BENCHMARK_FORMALIZATION_PREPARATION_AUTHORIZED",
        "LAB_MATHLIB_SMOKE_RECOVERY_AUTHORIZED",
        "LAB_LEAN_MATHLIB_COMPATIBILITY_RECOVERY_AUTHORIZED",
        "LAB_WINDOWS_CACHE_LAUNCH_RECOVERY_AUTHORIZED",
        "LAB_CACHE_NETWORK_RECOVERY_AUTHORIZED",
        "LAB_BENCHMARK_EXECUTION_AUTHORIZED",
        "FOUNDATIONS_EXECUTION_AUTHORIZED",
        "RH_NOGO_SPECIFICATION_PREPARATION_AUTHORIZED",
        "RH_NOGO_ASYMPTOTIC_LEMMA_FORMALIZATION_AUTHORIZED",
        "RH_NOGO_PRIMARY_SOURCE_AUDIT_AUTHORIZED",
        "RH_NOGO_ADDITIONAL_SOURCE_RETRIEVAL_AUTHORIZED",
        "RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_AUTHORIZED",
        "RH_NOGO_COUNTING_BRIDGE_FORMALIZATION_AUTHORIZED",
        "RH_NOGO_GEOMETRIC_GAP_RESOLUTION_AUTHORIZED",
        "RH_NOGO_ABSTRACT_COMPOSITION_FORMALIZATION_AUTHORIZED",
        "RH_NOGO_RESEARCH_REVIEW_AUTHORIZED",
        "FOUND_SEMIGROUP_002_SPECIFICATION_PREPARATION_AUTHORIZED",
        "FOUND_SEMIGROUP_002_FORMALIZATION_AUTHORIZED",
        "FOUND_SEMIGROUP_002_RESULT_REVIEW_AUTHORIZED",
        "PORTFOLIO_REVIEW_REQUIRED",
        "PORTFOLIO_REVIEW_AUTHORIZED",
        "FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_PREPARATION_AUTHORIZED",
        "FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW_AUTHORIZED",
        "FOUND_FUNCTIONAL_GRAPH_001_FORMALIZATION_AUTHORIZED",
        "FOUND_FUNCTIONAL_GRAPH_001_RESULT_REVIEW_AUTHORIZED",
        "FOUND_CYCLE_DETECTION_001_SPECIFICATION_PREPARATION_AUTHORIZED",
        "RH_NOGO_ASYMPTOTIC_LEMMA_FORMALIZATION_AUTHORIZED",
    }:
        errors.append("authorized_action is inconsistent with the active infrastructure gate")
    benchmark_phases = benchmark.get("phase_status", {})
    if benchmark.get("status") == "VERIFIED" and (
        benchmark_phases.get("LAB_BENCHMARK_EXECUTION") != "PASS"
        or benchmark_phases.get("LAB_BENCHMARK_VERIFICATION") != "PASS"
    ):
        errors.append("LAB-BENCH-001 cannot be VERIFIED before execution and verification are PASS")
    if rh_nogo.get("status") not in {"SCOPED", "FROZEN_PARTIAL_RESULT"}:
        errors.append("RH-NOGO-001 must remain SCOPED or FROZEN_PARTIAL_RESULT")
    if rh_nogo.get("authorization_state") != "NOT_AUTHORIZED":
        errors.append("RH-NOGO-001 must remain NOT_AUTHORIZED")
    if rh_nogo.get("execution_state") != "NO_EXECUTION":
        errors.append("RH-NOGO-001 must remain NO_EXECUTION")

    benchmark_status = read_yaml(
        LAB_ROOT / "05_FORMAL" / "specifications" / "LAB-BENCH-001_STATUS.yaml"
    )
    phases = benchmark_status.get("phases", {})
    required_phases = {
        "LEAN_ENVIRONMENT_DISCOVERY",
        "LEAN_TOOLCHAIN_AVAILABILITY",
        "LEAN_SMOKE_BUILD",
        "LAB_BENCHMARK_PREPARATION",
        "LAB_BENCHMARK_EXECUTION",
        "LAB_BENCHMARK_VERIFICATION",
    }
    if set(phases) != required_phases:
        errors.append("LAB-BENCH-001 phase classification is incomplete")
    if phases.get("LAB_BENCHMARK_EXECUTION", {}).get("status") not in {"NOT_STARTED", "PASS"}:
        errors.append("LAB-BENCH-001 execution must be NOT_STARTED or PASS")
    if phases.get("LAB_BENCHMARK_VERIFICATION", {}).get("status") not in {"NOT_STARTED", "PASS"}:
        errors.append("LAB-BENCH-001 verification must be NOT_STARTED or PASS")
    if (
        phases.get("LAB_BENCHMARK_VERIFICATION", {}).get("status") == "PASS"
        and phases.get("LAB_BENCHMARK_EXECUTION", {}).get("status") != "PASS"
    ):
        errors.append("LAB-BENCH-001 verification cannot be PASS before execution")

    claims_doc = read_yaml(LAB_ROOT / "00_GOVERNANCE" / "CLAIM_LEDGER.yaml")
    claims = claims_doc.get("claims", [])
    claim_ids = [claim.get("claim_id") for claim in claims]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("CLAIM_LEDGER has duplicate claim_id")
    for claim in claims:
        errors.extend(
            validate_json_schema(claim, "claim.schema.json", claim.get("claim_id", "claim"))
        )
        if claim.get("evidence_level") not in EVIDENCE_LEVELS:
            errors.append(f"invalid evidence level: {claim.get('claim_id')}")
        if claim.get("work_status") in {"SOLVED", "CLOSED", "100_PERCENT", "CLAY_READY"}:
            errors.append(f"promotional status in claim ledger: {claim.get('claim_id')}")

    canonical_check = check_canonical_commit(state.get("canonical_commit"))
    if canonical_check["status"] != CANONICAL_COMMIT_PASS:
        errors.append(
            f"{canonical_check['status']}: {canonical_check['message']}"
        )

    status_lines = git_status()
    if not all_changes_are_in_lab(status_lines):
        errors.append("changes detected outside 04_FORMAL_RESEARCH_LAB")

    lean_files = [
        path
        for path in (LAB_ROOT / "05_FORMAL" / "lean").rglob("*.lean")
        if ".lake" not in path.parts
    ]
    forbidden_pattern = re.compile(r"\b(sorry|admit|axiom|unsafe)\b")
    forbidden_lean = [
        str(path.relative_to(REPO_ROOT))
        for path in lean_files
        if forbidden_pattern.search(path.read_text(encoding="utf-8"))
    ]
    if forbidden_lean:
        errors.append(f"forbidden Lean tokens in: {forbidden_lean}")

    lean_result = lean_check()
    if lean_result["status"] != "PASS":
        warnings.append("Lean smoke build was not run by structural validation; consult the gate result.")
    if lean_result.get("toolchain_stability") != "PASS":
        warnings.append("Lean toolchain is not installed at a stable, non-.tmp location.")

    manifest = json.loads(
        (LAB_ROOT / "05_FORMAL" / "lean" / "lake-manifest.json").read_text(encoding="utf-8")
    )
    mathlib_packages = [
        package for package in manifest.get("packages", [])
        if package.get("name", "").lower() == "mathlib"
    ]
    mathlib_revision = (
        mathlib_packages[0].get("rev")
        or mathlib_packages[0].get("commit")
        or "UNRESOLVED"
        if mathlib_packages
        else "UNRESOLVED"
    )
    if mathlib_revision == "UNRESOLVED":
        warnings.append("Mathlib revision is unresolved for LAB-BENCH-001.")

    return {
        "schema": "tamesis-lab0-result/1",
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "baseline_commit": state.get("canonical_commit"),
        "status": "PASS" if not errors and lean_result["status"] == "PASS" else (
            "LAB0_LEAN_ENVIRONMENT_FAILED" if not errors else "LAB0_VALIDATION_FAILED"
        ),
        "errors": errors,
        "canonical_commit_check": canonical_check,
        "warnings": warnings,
        "repository_changes": status_lines,
        "claim_count": len(claims),
        "work_item_count": len(items),
        "lean": lean_result,
        "benchmark_gate": {
            "authorized_action": state.get("authorized_action"),
            "active_work_item": active,
            "phases": phases,
            "rh_nogo": {
                "status": rh_nogo.get("status"),
                "authorization_state": rh_nogo.get("authorization_state"),
                "execution_state": rh_nogo.get("execution_state"),
            },
            "mathlib_revision": mathlib_revision,
        },
        "legacy_files_modified": 0 if all_changes_are_in_lab(status_lines) else None,
        "research_claims_promoted": 0,
        "new_mathematical_proofs_executed": 0,
    }


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, default=str))


def command_status() -> int:
    state, _ = read_front_matter(LAB_ROOT / "LAB_STATE.md")
    queue = read_yaml(LAB_ROOT / "01_PORTFOLIO" / "RESEARCH_QUEUE.yaml")
    active = next(
        (item for item in queue.get("queue", []) if item.get("work_item_id") == state.get("active_work_item")),
        None,
    )
    print_json({"state": state, "active_work_item": active})
    return 0


def command_next() -> int:
    state, _ = read_front_matter(LAB_ROOT / "LAB_STATE.md")
    print(state["next_single_action"])
    return 0


def command_claims() -> int:
    print_json(read_yaml(LAB_ROOT / "00_GOVERNANCE" / "CLAIM_LEDGER.yaml"))
    return 0


def command_gaps() -> int:
    gaps: list[dict[str, Any]] = []
    for path in sorted((LAB_ROOT / "03_MILLENNIUM").glob("*/GAP_REGISTER.yaml")):
        data = read_yaml(path)
        for gap in data.get("gaps", []):
            gaps.append({"source": str(path.relative_to(REPO_ROOT)), **gap})
    print_json({"gaps": gaps})
    return 0


def command_start_session(work_item: str) -> int:
    queue = read_yaml(LAB_ROOT / "01_PORTFOLIO" / "RESEARCH_QUEUE.yaml")
    if work_item not in {item.get("work_item_id") for item in queue.get("queue", [])}:
        print(f"unknown work item: {work_item}", file=sys.stderr)
        return 2
    now = datetime.now().astimezone()
    session_id = f"{now:%Y-%m-%d_%H%M}_{work_item}"
    year_dir = LAB_ROOT / "09_SESSIONS" / f"{now:%Y}"
    year_dir.mkdir(parents=True, exist_ok=True)
    path = year_dir / f"{session_id}.md"
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()
    content = f"""---
session_id: {session_id}
started_at: {now.isoformat()}
ended_at: null
agent: labctl
git_commit_before: {commit}
git_commit_after: null
active_work_item: {work_item}
authorized_action: NOT_SET
result_status: IN_PROGRESS
files_created: []
files_modified: []
commands_executed: []
tests_executed: []
claims_changed: []
gaps_opened: []
gaps_closed: []
next_single_action: "Registrar o objetivo autorizado antes de executar."
---

## Objetivo autorizado
UNSET

## Estado inicial
UNSET

## Trabalho executado
UNSET

## Evidências
UNSET

## Falhas
UNSET

## Decisões
UNSET

## O que não foi feito
UNSET

## Próxima ação única
Registrar o objetivo autorizado antes de executar.

## Handoff
Sessão aberta; não executar sem autorização.
"""
    path.write_text(content, encoding="utf-8")
    print(path.relative_to(REPO_ROOT))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="labctl")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("next")
    sub.add_parser("claims")
    sub.add_parser("gaps")
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("--write-result", action="store_true")
    start_parser = sub.add_parser("start-session")
    start_parser.add_argument("work_item")
    sub.add_parser("close-session").add_argument("result_status")
    args = parser.parse_args(argv)

    if args.command == "status":
        return command_status()
    if args.command == "next":
        return command_next()
    if args.command == "claims":
        return command_claims()
    if args.command == "gaps":
        return command_gaps()
    if args.command == "start-session":
        return command_start_session(args.work_item)
    if args.command == "close-session":
        print("close-session requires editing the immutable session record through a reviewed change.")
        return 0
    result = validate()
    if args.write_result:
        (LAB_ROOT / "lab0-result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8"
        )
    print_json(result)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
