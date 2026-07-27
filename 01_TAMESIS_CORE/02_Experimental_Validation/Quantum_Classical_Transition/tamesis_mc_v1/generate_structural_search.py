"""Generate exhaustive textual evidence for structural-parameter occurrences."""

from __future__ import annotations

import re
from pathlib import Path

from config import reject_runtime_overrides


BASE = Path(__file__).resolve().parent
REPO = BASE.parents[3]
REPORT = BASE / "reports" / "STRUCTURAL_PARAMETER_SEARCH_EVIDENCE.md"
EXTENSIONS = {".py", ".yaml", ".yml", ".json", ".toml", ".md", ".ipynb"}
PATTERNS = {
    "frozen_Mc_exact": r"5\.292674126(?:388712|4)",
    "frozen_Mc_rounded": r"5\.29(?:2674)?[eE][+-]?[-]?16",
    "historical_2p2e14": r"2\.2[eE][+-]?[-]?14",
    "historical_1p25e16": r"1\.25[eE][+-]?[-]?16",
    "Mc_symbol": r"\b(?:M_c|Mc|mc_kg)\b",
    "tau_c": r"\btau_c\b",
    "alpha": r"\balpha\b",
    "transition_width": r"transition[_ -]?width|largura da transi",
    "phase_root": r"phase_space_root|root[- ]?eighth|raiz oitava|raiz[- ]?8|\^\s*\(?1\s*/\s*8\)?",
    "structural_exponent": r"exponent|expoente|\*\*\s*2(?:\.0)?",
    "rate_recalculation": r"intrinsic_rate|gamma_T|Gamma_T|threshold_rate|tamesis_rate",
    "model_summary_read": r"model_summary\.json",
    "environment_or_cli": r"os\.environ|os\.getenv|getenv\(|argparse|sys\.argv|TAMESIS_MC_",
}
COMBINED = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in PATTERNS.items()), re.IGNORECASE)


def classify(path: Path, line: str) -> tuple[str, str]:
    rel = path.relative_to(REPO).as_posix()
    executable = "yes" if path.suffix in {".py", ".ipynb"} else "no"
    if path == BASE / "config" / "tamesis_mc_v1.yaml":
        return executable, "canonical_source"
    if path.name.startswith("test_") or "fixture" in rel.lower():
        return executable, "test_fixture"
    if path.suffix == ".md":
        return executable, "documentation"
    if path.is_relative_to(BASE):
        if path.suffix in {".yaml", ".json"} and "config/" in rel:
            return executable, "canonical_source"
        if path.suffix == ".py":
            if any(token in line for token in ("CONTRACT", "contract.", "load_v1_contract", "McModel")):
                return executable, "canonical_use"
            if re.search(r"5\.292674126|5\.29[eE].*16|1\.25[eE].*16|2\.2[eE].*14", line):
                return executable, "suspicious_duplicate"
            return executable, "canonical_use"
        return executable, "documentation"
    if "90_LEGACY" in path.parts or path.suffix in {".py", ".ipynb", ".json", ".yaml", ".yml"}:
        return executable, "expected_legacy"
    return executable, "documentation"


def main() -> None:
    reject_runtime_overrides()
    rows = []
    files_scanned = 0
    for path in sorted(REPO.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS or "__pycache__" in path.parts or ".git" in path.parts:
            continue
        files_scanned += 1
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, start=1):
            matches = sorted({match.lastgroup for match in COMBINED.finditer(line) if match.lastgroup})
            if not matches:
                continue
            executable, classification = classify(path, line)
            context = line.strip().replace("|", "\\|")[:220]
            rows.append((", ".join(matches), path.relative_to(REPO).as_posix(), number, context, executable, classification))
    header = [
        "# Structural Parameter Search Evidence",
        "",
        f"Repository scope: `{REPO}`. Files scanned: **{files_scanned}**. Matching lines: **{len(rows)}**.",
        "",
        "The scan includes Python, YAML, JSON, TOML, Markdown and notebooks. Classification is lexical; suspicious rows require semantic review and are not automatically conflicts.",
        "",
        "| Ocorrência | Arquivo | Linha | Contexto | Executável? | Classificação |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    body = [f"| {kind} | `{path}` | {line_no} | `{context}` | {executable} | `{classification}` |" for kind, path, line_no, context, executable, classification in rows]
    REPORT.write_text("\n".join(header + body) + "\n", encoding="utf-8")
    print(f"wrote {REPORT} with {len(rows)} matching lines from {files_scanned} files")


if __name__ == "__main__":
    main()
