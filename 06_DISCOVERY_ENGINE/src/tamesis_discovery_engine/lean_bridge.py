"""Formal Proof / Lean Bridge — Module 9 of the Tamesis Discovery Engine.

A bridge from a ``CONFIRMED`` claim into a Lean4 formalization, for the
subset of results with a genuine mathematical core
(``CHECKLIST_09_FORMAL_PROOF_LEAN_BRIDGE.md``, ``ROADMAP.md`` Stage 2 item
9). "A bridge from a CONFIRMED claim" is the literal requirement this
module enforces, not merely documents: :meth:`LeanBridge.formalize` looks
the claim up via Stage 1's :class:`~tamesis_discovery_engine.registry.Registry`
and raises :class:`ClaimNotConfirmedError` for anything short of
``CONFIRMED`` — a claim that is merely ``RESULT`` or even
``ADVERSARIAL_REVIEW``-passed-but-not-yet-verdicted has no business being
formalized as if it were an accepted fact.

Hard scope boundary
--------------------
This module manages its own, completely separate Lean project directory
under ``06_DISCOVERY_ENGINE/lean_scratch/``. It must NEVER write into,
modify, or execute a build against ``04_FORMAL_RESEARCH_LAB`` — that is
the archive's own real, governed Lean formalization line with its own
history and provenance (referenced here only as prose, never as a path
this module opens for writing); generated engine stub files have no
business there. Generated per-claim ``.lean`` files live under
``lean_scratch/generated/`` and are not committed to git — they are
reproducible at any time from a claim's own record, not source of truth.

Scratch project shape: bare ``lean``, no Lake project
-------------------------------------------------------
Before writing this module, its intended compilation mechanism was
verified empirically in this environment: ``lean --version`` reports
``4.33.0-rc1``, and a throwaway trivial ``.lean`` file run through a bare
``lean <file>.lean`` invocation (no ``lakefile``, no Mathlib import, no
project structure) correctly compiled a true statement
(``theorem t : (1:Nat) + 1 = 2 := by decide``, exit 0), correctly failed a
false-but-well-formed statement with a real compiler diagnostic ("Tactic
`decide` proved that the proposition ... is false", exit 1), and
correctly failed a syntactically malformed statement with a real parser
diagnostic ("unexpected token ...", exit 1) — without crashing the ``lean``
process in either failure case. Since the trivial, no-``Mathlib`` claims
this bridge is scoped to check need nothing a bare invocation doesn't
already provide, a Lake project (``lakefile.toml`` + ``lake build``) would
be pure overhead: extra setup, an extra dependency-resolution step, and a
slower first invocation for no behavioral gain here. The scratch project
is therefore just a ``lean-toolchain`` file (pinned to ``4.33.0-rc1``, the
version already installed in this environment and the same pin
``04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/lean-toolchain`` uses) plus the
``generated/`` directory for per-claim sources — no ``lakefile`` at all.

Timing: the very first ``lean`` invocation in a cold environment measured
~18s (OS page/library cache warm-up for the ``lean`` binary itself, not a
per-compile cost); every subsequent invocation of a trivial file measured
~0.2-0.3s. That one-time warm-up is not a reason to skip or shorten the
test suite — it happens once per process, not once per compile.

This module reuses Stage 1's :class:`~tamesis_discovery_engine.ledger.Ledger`
for outcomes rather than inventing its own persistence: every
:meth:`LeanBridge.formalize` call — compiled or not — appends exactly one
entry, honestly summarizing what the compiler actually reported.
"""

from __future__ import annotations

import dataclasses
import subprocess
import time
from pathlib import Path
from typing import Optional

from .claim import ClaimState
from .ledger import Ledger
from .registry import Registry

__all__ = [
    "LeanFormalizationResult",
    "LeanBridge",
    "ClaimNotConfirmedError",
    "DEFAULT_SCRATCH_DIR",
]

DEFAULT_SCRATCH_DIR = Path(__file__).resolve().parent.parent.parent / "lean_scratch"

_LEAN_TOOLCHAIN = "leanprover/lean4:v4.33.0-rc1"
_LEAN_FORMALIZE_DECISION_TYPE = "LEAN_FORMALIZE"
_DEFAULT_TIMEOUT_SECONDS = 120.0


class ClaimNotConfirmedError(Exception):
    """Raised by ``LeanBridge.formalize`` when the claim is not ``CONFIRMED``.

    This is what makes the module *enforce* "a bridge from a CONFIRMED
    claim" rather than merely document it: the Lean compiler is never
    invoked for a claim in any other state, including the four other
    terminal verdicts (``REFUTED``, ``INCONCLUSIVE``, ``NULL``).
    """

    def __init__(self, claim_id: str, actual_state: ClaimState):
        self.claim_id = claim_id
        self.actual_state = actual_state
        super().__init__(
            f"Cannot formalize claim {claim_id!r}: expected state CONFIRMED, found "
            f"{actual_state.value}"
        )


@dataclasses.dataclass(frozen=True)
class LeanFormalizationResult:
    compiled: bool
    stdout: str
    stderr: str
    duration_seconds: float
    lean_file_path: str


class LeanBridge:
    """Formalizes ``CONFIRMED`` claims as Lean4 theorems in an isolated scratch project.

    ``registry`` is the Module 1 :class:`~tamesis_discovery_engine.registry.Registry`
    this class reads claim state through (it never mutates a ``Claim``).
    ``ledger`` is the Module 5 :class:`~tamesis_discovery_engine.ledger.Ledger`
    every :meth:`formalize` call appends exactly one entry to, compiled or
    not. ``scratch_dir`` defaults to ``06_DISCOVERY_ENGINE/lean_scratch``
    (created on first use if absent, see the module docstring for its
    shape); pass an explicit directory (e.g. a pytest ``tmp_path``) to keep
    a bridge's generated files isolated. ``timeout_seconds`` bounds a
    single ``lean`` invocation — the compiles this bridge is scoped to are
    trivial and finish in well under a second, so a hung/runaway compile is
    reported as a failed (``compiled=False``) result rather than hanging
    the caller forever.
    """

    def __init__(
        self,
        registry: Registry,
        ledger: Ledger,
        scratch_dir: Optional[Path | str] = None,
        timeout_seconds: float = _DEFAULT_TIMEOUT_SECONDS,
    ):
        self.registry = registry
        self.ledger = ledger
        self.scratch_dir = Path(scratch_dir) if scratch_dir is not None else DEFAULT_SCRATCH_DIR
        self.generated_dir = self.scratch_dir / "generated"
        self.timeout_seconds = timeout_seconds

    def formalize(self, claim_id: str, lean_source: str, theorem_name: str) -> LeanFormalizationResult:
        claim = self.registry.get(claim_id)
        if claim.state is not ClaimState.CONFIRMED:
            raise ClaimNotConfirmedError(claim_id, claim.state)

        self._ensure_scratch_project()
        lean_file_path = self.generated_dir / f"{claim_id}.lean"
        lean_file_path.write_text(lean_source)

        result = self._compile(lean_file_path)

        outcome = "compiled" if result.compiled else "FAILED to compile"
        self.ledger.append(
            claim_id,
            _LEAN_FORMALIZE_DECISION_TYPE,
            f"Lean formalization {theorem_name!r} {outcome} in "
            f"{result.duration_seconds:.3f}s ({lean_file_path.name})",
        )
        return result

    def _ensure_scratch_project(self) -> None:
        self.scratch_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        toolchain_path = self.scratch_dir / "lean-toolchain"
        if not toolchain_path.exists():
            toolchain_path.write_text(_LEAN_TOOLCHAIN + "\n")

    def _compile(self, lean_file_path: Path) -> LeanFormalizationResult:
        start = time.monotonic()
        try:
            proc = subprocess.run(
                ["lean", str(lean_file_path)],
                cwd=self.scratch_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )
            duration = time.monotonic() - start
            return LeanFormalizationResult(
                compiled=(proc.returncode == 0),
                stdout=proc.stdout,
                stderr=proc.stderr,
                duration_seconds=duration,
                lean_file_path=str(lean_file_path),
            )
        except subprocess.TimeoutExpired as exc:
            duration = time.monotonic() - start
            return LeanFormalizationResult(
                compiled=False,
                stdout=(exc.stdout or "") if isinstance(exc.stdout, str) else "",
                stderr=f"lean invocation exceeded timeout of {self.timeout_seconds}s and was killed",
                duration_seconds=duration,
                lean_file_path=str(lean_file_path),
            )
