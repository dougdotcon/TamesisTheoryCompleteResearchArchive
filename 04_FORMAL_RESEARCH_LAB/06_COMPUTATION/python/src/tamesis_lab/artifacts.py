from pathlib import Path


def find_forbidden_lean_tokens(root: Path) -> list[Path]:
    """Find Lean files containing proof-shortcut tokens."""
    findings: list[Path] = []
    for path in root.rglob("*.lean"):
        text = path.read_text(encoding="utf-8")
        if "sorry" in text or "admit" in text:
            findings.append(path)
    return findings

