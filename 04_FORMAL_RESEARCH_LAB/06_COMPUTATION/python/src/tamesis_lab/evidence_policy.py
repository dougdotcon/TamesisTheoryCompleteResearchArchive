EVIDENCE_LEVELS = frozenset("HFCOPEITN")

FORBIDDEN_AUTOMATIC_PROMOTIONS = frozenset(
    {
        ("C", "T"),
        ("F", "T"),
        ("P", "E"),
        ("MANUSCRIPT", "I"),
    }
)


def can_promote_automatically(source: str, target: str) -> bool:
    """Return whether a promotion is allowed without an explicit gate."""
    return (source, target) not in FORBIDDEN_AUTOMATIC_PROMOTIONS


def validate_evidence_level(level: str) -> bool:
    return level in EVIDENCE_LEVELS

