"""Canonical paths for the Tamesis M_c v1 workspace."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"


def ensure_workspace_dirs() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)


def data_path(name: str) -> Path:
    ensure_workspace_dirs()
    return DATA_DIR / name


def report_path(name: str) -> Path:
    ensure_workspace_dirs()
    return REPORTS_DIR / name
