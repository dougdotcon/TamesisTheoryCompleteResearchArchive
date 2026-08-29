"""Hypothesis Engine — Module 11 of the Tamesis Discovery Engine (Stage 3a).

Turns a vague claim ("I think X causes Y") into a structured, falsifiable
spec (prediction, null model, competing model, effect size, threshold),
building on Module 1's :class:`~tamesis_discovery_engine.registry.Registry`
and :class:`~tamesis_discovery_engine.claim.Claim` rather than redefining
either.

Scope honesty constraint
-------------------------
This module does not perform any automated free-text inference to
"understand" a vague claim and generate its null model, competing model,
effect size metric, or threshold on its own behalf — that would be exactly
the kind of fabricated rigor this archive's own ethos (and Module 4's own
precedent) rejects. What it actually does is provide a **structured spec
type**, :class:`FalsifiableSpec`, with field-completeness validation, so
that turning a vague idea into a falsifiable spec is a deliberate, explicit
authoring step (a human or an agent filling in real fields) rather than an
unstructured free-text ``statement`` string.

That discipline is enforced only for callers that go through
:meth:`HypothesisEngine.pre_register` — it is **not** a system-wide
guarantee. :meth:`Registry.advance`/:meth:`~tamesis_discovery_engine.DiscoveryEngine.advance`
remain generic, ungated state-machine transitions (as they are for every
other Stage 1 state change, and as Stage 1's own tests already rely on to
pre-register spec-less claims) and never check :class:`FalsifiableSpec`
completeness, because neither method knows this module or
:class:`FalsifiableSpec` exists. A caller that reaches ``PRE_REGISTERED``
through :meth:`Registry.advance`/:meth:`~tamesis_discovery_engine.DiscoveryEngine.advance`
directly — instead of through :meth:`HypothesisEngine.pre_register` —
bypasses this discipline entirely, even for a claim that
:meth:`HypothesisEngine.draft` itself created. "Encodes the discipline"
here means the validation :meth:`HypothesisEngine.draft` and
:meth:`HypothesisEngine.pre_register` themselves perform, not a hook
wired into :meth:`Registry.create`/:meth:`Registry.advance`.

:meth:`FalsifiableSpec.validate` only ever checks *structural* completeness
(are the required fields present and non-empty) — never whether the
content is scientifically sound. Judging content is Module 4's job
(:class:`~tamesis_discovery_engine.adversarial.AdversarialReviewer`),
applied later in the claim's life, once there is a result to review.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, List, Optional

from .claim import Claim, ClaimState
from .registry import Registry

SPEC_METADATA_KEY = "falsifiable_spec"

_REQUIRED_STRING_FIELDS = ("prediction", "null_model", "effect_size_metric")


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    return False


@dataclasses.dataclass
class FalsifiableSpec:
    """A structured, falsifiable spec for one hypothesis.

    ``raw_claim`` is the original vague free-text idea, kept only for
    provenance — it is never parsed or interpreted by this module.
    ``prediction``/``null_model``/``effect_size_metric``/``threshold`` are
    the fields authored to make the claim checkable. ``competing_model``
    may be ``None`` only when ``competing_model_rationale`` explains why no
    competing explanation applies — one of the two must always be present.
    """

    raw_claim: str
    prediction: str
    null_model: str
    effect_size_metric: str
    threshold: Any
    competing_model: Optional[str] = None
    competing_model_rationale: Optional[str] = None

    def validate(self) -> List[str]:
        problems: List[str] = []
        for field_name in _REQUIRED_STRING_FIELDS:
            if _is_empty(getattr(self, field_name)):
                problems.append(f"{field_name} must be non-empty")
        if _is_empty(self.threshold):
            problems.append("threshold must be non-empty")
        if _is_empty(self.competing_model) and _is_empty(self.competing_model_rationale):
            problems.append(
                "competing_model and competing_model_rationale are both empty: "
                "either name a competing explanation or explain why none applies"
            )
        return problems

    def to_claim_metadata(self) -> Dict[str, Any]:
        return {SPEC_METADATA_KEY: dataclasses.asdict(self)}

    @classmethod
    def from_claim_metadata(cls, metadata: Dict[str, Any]) -> "FalsifiableSpec":
        if SPEC_METADATA_KEY not in metadata:
            raise KeyError(
                f"metadata does not contain a {SPEC_METADATA_KEY!r} entry: "
                f"this claim was not drafted through HypothesisEngine.draft()"
            )
        return cls(**metadata[SPEC_METADATA_KEY])


class IncompleteSpecError(Exception):
    """Raised when a :class:`FalsifiableSpec` is structurally incomplete.

    Covers both :meth:`HypothesisEngine.draft` (spec invalid before a claim
    is ever created) and :meth:`HypothesisEngine.pre_register` (the spec
    stored in an existing claim's metadata was hand-edited into an invalid
    state after ``draft()``). ``problems`` always carries the exact list
    :meth:`FalsifiableSpec.validate` produced, so the caller sees precisely
    what is missing.
    """

    def __init__(self, action: str, problems: List[str], claim_id: Optional[str] = None):
        self.action = action
        self.problems = list(problems)
        self.claim_id = claim_id
        subject = f"claim {claim_id}" if claim_id else "spec"
        super().__init__(
            f"Cannot {action} {subject}: falsifiable spec is structurally "
            f"incomplete ({'; '.join(self.problems)})"
        )


class HypothesisEngine:
    """Wraps Module 1's ``Registry`` with the falsifiable-spec discipline.

    Carries no state and no ``data_dir`` of its own — every method takes
    the caller's :class:`~tamesis_discovery_engine.registry.Registry`
    explicitly, so one engine works across as many registries as needed
    and adds nothing to what Module 1 already persists.
    """

    @staticmethod
    def draft(registry: Registry, title: str, spec: FalsifiableSpec) -> Claim:
        problems = spec.validate()
        if problems:
            raise IncompleteSpecError("draft", problems)
        return registry.create(title, spec.raw_claim, metadata=spec.to_claim_metadata())

    @staticmethod
    def pre_register(registry: Registry, claim_id: str) -> Claim:
        claim = registry.get(claim_id)
        try:
            spec = FalsifiableSpec.from_claim_metadata(claim.metadata)
        except (KeyError, TypeError):
            raise IncompleteSpecError(
                "pre-register",
                [
                    f"no {SPEC_METADATA_KEY!r} entry, or the stored entry does not match "
                    "FalsifiableSpec's required fields"
                ],
                claim_id=claim_id,
            ) from None

        problems = spec.validate()
        if problems:
            raise IncompleteSpecError("pre-register", problems, claim_id=claim_id)

        return registry.advance(claim_id, ClaimState.PRE_REGISTERED)
