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
from typing import Any, NamedTuple

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
    """Front matter de um Markdown, REJEITANDO chaves duplicadas.

    `yaml.safe_load` sozinho aplica "ultimo valor vence", que a governanca
    do laboratorio proibe explicitamente. Carregar o bloco sem antes
    verificar duplicatas faria o parser escolher silenciosamente um dos
    valores — inclusive num campo como `authorized_action`.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"missing YAML front matter: {path}")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError(f"malformed YAML front matter: {path}")
    duplicates = detect_duplicate_front_matter_keys(path)
    if duplicates:
        raise ValueError(
            f"{DUPLICATE_YAML_KEY}: {path}: " + "; ".join(d.as_error() for d in duplicates)
        )
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


YAML_SCAN_EXCLUDED_DIRS = {".lake", "__pycache__", ".venv", "node_modules", ".git"}
DUPLICATE_YAML_KEY = "DUPLICATE_YAML_KEY"


class DuplicateYamlKey(NamedTuple):
    """Uma chave definida mais de uma vez dentro do mesmo mapa YAML."""

    file: str
    document_index: int
    mapping_path: str
    key: str
    first_line: int
    duplicate_line: int
    first_value: str
    duplicate_value: str
    classification: str

    def as_error(self) -> str:
        return (
            f"{DUPLICATE_YAML_KEY}: {self.file}:{self.duplicate_line} "
            f"path={self.mapping_path} key={self.key} "
            f"first_defined_at={self.first_line} "
            f"classification={self.classification}"
        )


def _yaml_node_label(node: Any) -> str:
    if isinstance(node, yaml.ScalarNode):
        return node.value
    if isinstance(node, yaml.SequenceNode):
        return f"<seq len={len(node.value)}>"
    if isinstance(node, yaml.MappingNode):
        return f"<map keys={len(node.value)}>"
    return "<node>"


def _yaml_path_label(path: list[Any]) -> str:
    out = ""
    for part in path:
        if isinstance(part, int):
            out += f"[{part}]"
        else:
            out += ("." if out else "") + str(part)
    return out or "<root>"


def _walk_yaml_node(node: Any, path: list[Any], file: str, doc_index: int,
                    found: list[DuplicateYamlKey]) -> None:
    """Percorre a ARVORE SINTATICA. O objeto ja colapsado pelo parser nao
    serve: nele a duplicata desapareceu."""
    if isinstance(node, yaml.MappingNode):
        seen: dict[str, tuple[Any, Any]] = {}
        for key_node, value_node in node.value:
            key = key_node.value if isinstance(key_node, yaml.ScalarNode) else _yaml_node_label(key_node)
            if key in seen:
                first_key_node, first_value_node = seen[key]
                first_value = _yaml_node_label(first_value_node)
                duplicate_value = _yaml_node_label(value_node)
                found.append(DuplicateYamlKey(
                    file=file,
                    document_index=doc_index,
                    mapping_path=_yaml_path_label(path),
                    key=key,
                    first_line=first_key_node.start_mark.line + 1,
                    duplicate_line=key_node.start_mark.line + 1,
                    first_value=first_value,
                    duplicate_value=duplicate_value,
                    classification=("IDENTICAL_DUPLICATE"
                                    if first_value == duplicate_value
                                    else "DIVERGENT_DUPLICATE"),
                ))
            else:
                seen[key] = (key_node, value_node)
            _walk_yaml_node(value_node, path + [key], file, doc_index, found)
    elif isinstance(node, yaml.SequenceNode):
        for index, child in enumerate(node.value):
            _walk_yaml_node(child, path + [index], file, doc_index, found)


def detect_duplicate_yaml_keys(path: Path) -> list[DuplicateYamlKey]:
    """Chaves duplicadas de um arquivo YAML, em qualquer profundidade.

    Duplicatas com valores idênticos também são reportadas: a política do
    laboratório não aceita "último valor vence" como semântica.
    """
    found: list[DuplicateYamlKey] = []
    try:
        label = str(path.relative_to(REPO_ROOT))
    except ValueError:
        label = str(path)
    documents = yaml.compose_all(path.read_text(encoding="utf-8"))
    for index, document in enumerate(documents):
        if document is None:
            continue
        _walk_yaml_node(document, [], label, index, found)
    return found


MALFORMED_FRONT_MATTER = "MALFORMED_FRONT_MATTER"

FRONT_MATTER_PATTERN = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", re.DOTALL)

# A linha de abertura "---" ocupa a primeira linha do arquivo, de modo que a
# primeira linha do bloco YAML e a linha 2. O detector conta a partir de 1
# dentro do bloco, e por isso o deslocamento para o arquivo eh exatamente 1.
FRONT_MATTER_LINE_OFFSET = 1


def extract_front_matter(text: str) -> str | None:
    """Bloco YAML de um documento Markdown, ou None se nao houver.

    Devolve None quando o arquivo nao comeca com "---". Levanta ValueError
    quando comeca com "---" e o delimitador de fechamento nao esta numa
    linha propria: nesse caso o front matter existe mas esta malformado, e
    silenciar isso seria aceitar um documento sem estrutura univoca.
    """
    if not text.startswith("---"):
        return None
    match = FRONT_MATTER_PATTERN.match(text)
    if not match:
        raise ValueError(
            "front matter opened with --- but the closing delimiter is not on a line of its own"
        )
    return match.group(1)


def detect_duplicate_front_matter_keys(path: Path) -> list[DuplicateYamlKey]:
    """Chaves duplicadas dentro do front matter YAML de um Markdown.

    Reutiliza o MESMO percurso da arvore sintatica usado nos arquivos .yaml.
    O defeito historico era de ESCOPO, nao de algoritmo: a deteccao sempre
    funcionou, mas a selecao de arquivos filtrava por extensao.
    """
    try:
        label = str(path.relative_to(REPO_ROOT))
    except ValueError:
        label = str(path)
    body = extract_front_matter(path.read_text(encoding="utf-8"))
    if body is None:
        return []
    found: list[DuplicateYamlKey] = []
    for index, document in enumerate(yaml.compose_all(body)):
        if document is None:
            continue
        raw: list[DuplicateYamlKey] = []
        _walk_yaml_node(document, [], label, index, raw)
        found.extend(
            item._replace(
                first_line=item.first_line + FRONT_MATTER_LINE_OFFSET,
                duplicate_line=item.duplicate_line + FRONT_MATTER_LINE_OFFSET,
            )
            for item in raw
        )
    return found


def markdown_files_under(root: Path) -> list[Path]:
    files = []
    for candidate in sorted(root.rglob("*.md")):
        if any(part in YAML_SCAN_EXCLUDED_DIRS for part in candidate.parts):
            continue
        files.append(candidate)
    return files


def yaml_files_under(root: Path) -> list[Path]:
    files = []
    for candidate in sorted(root.rglob("*")):
        if candidate.suffix.lower() not in (".yaml", ".yml"):
            continue
        if any(part in YAML_SCAN_EXCLUDED_DIRS for part in candidate.parts):
            continue
        files.append(candidate)
    return files


def scan_duplicate_yaml_keys(root: Path | None = None) -> dict[str, Any]:
    """Varredura integral: arquivos .yaml/.yml E o front matter YAML dos
    documentos Markdown.

    O escopo do front matter foi acrescentado depois de se medir que a
    varredura anterior cobria 57 arquivos e ZERO Markdown, deixando de fora
    332 documentos com front matter — inclusive LAB_STATE.md, o arquivo mais
    critico da governanca. Declarar aquela varredura como integral era
    afirmar mais do que ela media.
    """
    root = root or LAB_ROOT
    duplicates: list[DuplicateYamlKey] = []
    unparsable: list[str] = []
    malformed: list[str] = []

    files = yaml_files_under(root)
    for path in files:
        try:
            duplicates.extend(detect_duplicate_yaml_keys(path))
        except yaml.YAMLError as exc:
            unparsable.append(f"{path}: {exc}")

    markdown_files = markdown_files_under(root)
    markdown_with_front_matter = 0
    for path in markdown_files:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            unparsable.append(f"{path}: {exc}")
            continue
        if not text.startswith("---"):
            continue
        markdown_with_front_matter += 1
        try:
            duplicates.extend(detect_duplicate_front_matter_keys(path))
        except ValueError as exc:
            malformed.append(f"{path}: {exc}")
        except yaml.YAMLError as exc:
            unparsable.append(f"{path}: {exc}")

    return {
        "files_scanned": len(files) + markdown_with_front_matter,
        "yaml_files_scanned": len(files),
        "markdown_files_seen": len(markdown_files),
        "markdown_front_matter_scanned": markdown_with_front_matter,
        "duplicate_count": len(duplicates),
        "files_with_duplicates": len({d.file for d in duplicates}),
        "identical_duplicates": sum(
            1 for d in duplicates if d.classification == "IDENTICAL_DUPLICATE"),
        "divergent_duplicates": sum(
            1 for d in duplicates if d.classification == "DIVERGENT_DUPLICATE"),
        "unparsable_files": unparsable,
        "malformed_front_matter": malformed,
        "duplicates": [d._asdict() for d in duplicates],
        "errors": [d.as_error() for d in duplicates]
        + [f"UNPARSABLE_YAML: {u}" for u in unparsable]
        + [f"{MALFORMED_FRONT_MATTER}: {m}" for m in malformed],
    }


DECISION_CITATION_PATTERN = re.compile(r"\bDEC-(\d{3})\b")

DECISION_TEXT_SUFFIXES = (".md", ".yaml", ".yml", ".json")


def decision_ids_registered() -> set[str]:
    """Identificadores com entrada propria no ledger de decisoes."""
    doc = read_yaml(LAB_ROOT / "00_GOVERNANCE" / "DECISION_LEDGER.yaml")
    return {
        str(entry.get("decision_id"))
        for entry in doc.get("decisions", [])
        if entry.get("decision_id")
    }


def scan_decision_citations(root: Path | None = None) -> dict[str, Any]:
    """Toda citacao DEC-NNN sob o laboratorio precisa de entrada no ledger.

    Motivo: DEC-015..DEC-022 foram citados no CHANGELOG como autoridade de
    edicoes literais no proprio labctl.py sem nunca terem entrada. Uma
    autoridade que so existe em narrativa nao e autoridade.

    A verificacao detecta citacao SEM entrada. Ela nao detecta citacao com
    entrada ERRADA: a colisao de DEC-014 foi resolvida por um campo
    explicito, nao por esta varredura.
    """
    base = root if root is not None else LAB_ROOT
    registered = decision_ids_registered()
    cited: dict[str, list[str]] = {}
    for path in sorted(base.rglob("*")):
        if not path.is_file() or path.suffix not in DECISION_TEXT_SUFFIXES:
            continue
        if ".lake" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for match in DECISION_CITATION_PATTERN.finditer(text):
            cited.setdefault(match.group(0), []).append(
                str(path.relative_to(REPO_ROOT))
            )
    unregistered = {
        identifier: sorted(set(files))
        for identifier, files in cited.items()
        if identifier not in registered
    }
    return {
        "registered": len(registered),
        "cited": len(cited),
        "unregistered": unregistered,
        "files_scanned": sum(len(set(f)) for f in cited.values()),
    }


def validate() -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    # Integridade estrutural antes de qualquer carregamento: um YAML com
    # chave duplicada nao possui semantica univoca, e o parser padrao
    # descartaria silenciosamente parte do documento.
    yaml_duplicate_scan = scan_duplicate_yaml_keys()
    errors.extend(yaml_duplicate_scan["errors"])
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

    invariant_dependency = item_by_id.get("FOUND-FINITE-STATE-ABSTRACTION-001", {})
    if active == "FOUND-INVARIANT-UNREACHABILITY-001" and (
        invariant_dependency.get("status") != "VERIFIED"
        or invariant_dependency.get("result_review") != "APPROVED"
    ):
        errors.append(
            "FOUND-INVARIANT-UNREACHABILITY-001 cannot be active before "
            "FOUND-FINITE-STATE-ABSTRACTION-001 is VERIFIED with result_review APPROVED"
        )

    benchmark = item_by_id.get("LAB-BENCH-001", {})
    rh_nogo = item_by_id.get("RH-NOGO-001", {})
    semigroup = item_by_id.get("FOUND-SEMIGROUP-001", {})
    if active not in {"LAB-BENCH-001", "FOUND-SEMIGROUP-001", "RH-NOGO-001",
                      "FOUND-SEMIGROUP-002", "FOUND-FUNCTIONAL-GRAPH-001",
                      "FOUND-CYCLE-DETECTION-001", "ENG-FINITE-STATE-RUNTIME-001",
                      "ENG-FINITE-STATE-ENCODING-001",
                      "FOUND-FINITE-STATE-ABSTRACTION-001",
                      "FOUND-BISIMULATION-BOUNDARY-001",
                      "FOUND-INVARIANT-UNREACHABILITY-001"}:
        errors.append(
            "gate sequence requires LAB-BENCH-001, FOUND-SEMIGROUP-001, RH-NOGO-001, "
            "FOUND-SEMIGROUP-002, FOUND-FUNCTIONAL-GRAPH-001, "
            "FOUND-CYCLE-DETECTION-001 or ENG-FINITE-STATE-RUNTIME-001 "
            "as active_work_item"
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
    fcd = item_by_id.get("FOUND-CYCLE-DETECTION-001", {})
    if active == "ENG-FINITE-STATE-RUNTIME-001" and (
        fcd.get("status") != "VERIFIED" or fcd.get("result_review") != "APPROVED"
    ):
        errors.append("ENG-FINITE-STATE-RUNTIME-001 cannot be active before FOUND-CYCLE-DETECTION-001 is VERIFIED with result_review APPROVED")
    fsr = item_by_id.get("ENG-FINITE-STATE-RUNTIME-001", {})
    if active == "ENG-FINITE-STATE-ENCODING-001" and (
        fsr.get("status") != "VERIFIED" or fsr.get("result_review") != "APPROVED"
    ):
        errors.append("ENG-FINITE-STATE-ENCODING-001 cannot be active before ENG-FINITE-STATE-RUNTIME-001 is VERIFIED with result_review APPROVED")
    fse = item_by_id.get("ENG-FINITE-STATE-ENCODING-001", {})
    ffsa = item_by_id.get("FOUND-FINITE-STATE-ABSTRACTION-001", {})
    if active == "FOUND-BISIMULATION-BOUNDARY-001" and (
        ffsa.get("status") != "VERIFIED" or ffsa.get("result_review") != "APPROVED"
    ):
        errors.append("FOUND-BISIMULATION-BOUNDARY-001 cannot be active before FOUND-FINITE-STATE-ABSTRACTION-001 is VERIFIED with result_review APPROVED")
    if active == "FOUND-FINITE-STATE-ABSTRACTION-001" and (
        fse.get("status") != "VERIFIED" or fse.get("result_review") != "APPROVED"
    ):
        errors.append("FOUND-FINITE-STATE-ABSTRACTION-001 cannot be active before ENG-FINITE-STATE-ENCODING-001 is VERIFIED with result_review APPROVED")
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
        "FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_AUTHORIZED",
        "FOUND_CYCLE_DETECTION_001_FORMALIZATION_AUTHORIZED",
        "FOUND_CYCLE_DETECTION_001_RESULT_REVIEW_AUTHORIZED",
        "ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_PREPARATION_AUTHORIZED",
        "ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_REVIEW_AUTHORIZED",
        "ENG_FINITE_STATE_RUNTIME_001_FORMALIZATION_AUTHORIZED",
        "ENG_FINITE_STATE_RUNTIME_001_RESULT_REVIEW_AUTHORIZED",
        "ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_PREPARATION_AUTHORIZED",
        "ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW_AUTHORIZED",
        "ENG_FINITE_STATE_ENCODING_001_FORMALIZATION_AUTHORIZED",
        "ENG_FINITE_STATE_ENCODING_001_RESULT_REVIEW_AUTHORIZED",
        "FOUND_FINITE_STATE_ABSTRACTION_001_SPECIFICATION_PREPARATION_AUTHORIZED",
        "FOUND_FINITE_STATE_ABSTRACTION_001_SPECIFICATION_REVIEW_AUTHORIZED",
        "FOUND_FINITE_STATE_ABSTRACTION_001_FORMALIZATION_AUTHORIZED",
        "FOUND_FINITE_STATE_ABSTRACTION_001_RESULT_REVIEW_AUTHORIZED",
        "LAB_GOV_FRONTMATTER_SCAN_CORRECTION_AUTHORIZED",
        "FOUND_BISIMULATION_BOUNDARY_001_SPECIFICATION_PREPARATION_AUTHORIZED",
        "FOUND_BISIMULATION_BOUNDARY_001_SPECIFICATION_REVIEW_AUTHORIZED",
        "FOUND_BISIMULATION_BOUNDARY_001_FORMALIZATION_AUTHORIZED",
        "FOUND_BISIMULATION_BOUNDARY_001_RESULT_REVIEW_AUTHORIZED",
        "LAB_GOV_YAML_DUPLICATE_KEYS_CORRECTION_AUTHORIZED",
        "LAB_GOV_DECISION_LEDGER_CORRECTION_AUTHORIZED",
        "FOUND_INVARIANT_UNREACHABILITY_001_SPECIFICATION_PREPARATION_AUTHORIZED",
        "FOUND_INVARIANT_UNREACHABILITY_001_SPECIFICATION_REVIEW_AUTHORIZED",
        "FOUND_INVARIANT_UNREACHABILITY_001_FORMALIZATION_AUTHORIZED",
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

    decisions_doc = read_yaml(LAB_ROOT / "00_GOVERNANCE" / "DECISION_LEDGER.yaml")
    decision_entries = decisions_doc.get("decisions", [])
    decision_ids = [entry.get("decision_id") for entry in decision_entries]
    if len(decision_ids) != len(set(decision_ids)):
        errors.append("DECISION_LEDGER has duplicate decision_id")
    citation_scan = scan_decision_citations()
    for identifier, files in sorted(citation_scan["unregistered"].items()):
        errors.append(
            f"decision cited without ledger entry: {identifier} in {files}"
        )

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
        "yaml_duplicate_key_scan": {
            "files_scanned": yaml_duplicate_scan["files_scanned"],
            "yaml_files_scanned": yaml_duplicate_scan["yaml_files_scanned"],
            "markdown_files_seen": yaml_duplicate_scan["markdown_files_seen"],
            "markdown_front_matter_scanned":
                yaml_duplicate_scan["markdown_front_matter_scanned"],
            "duplicate_count": yaml_duplicate_scan["duplicate_count"],
            "files_with_duplicates": yaml_duplicate_scan["files_with_duplicates"],
            "identical_duplicates": yaml_duplicate_scan["identical_duplicates"],
            "divergent_duplicates": yaml_duplicate_scan["divergent_duplicates"],
            "unparsable_files": yaml_duplicate_scan["unparsable_files"],
            "malformed_front_matter": yaml_duplicate_scan["malformed_front_matter"],
            "scope": "yaml_files_and_markdown_front_matter",
            "status": (
                "PASS"
                if not yaml_duplicate_scan["duplicate_count"]
                and not yaml_duplicate_scan["malformed_front_matter"]
                else "FAIL"
            ),
        },
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
