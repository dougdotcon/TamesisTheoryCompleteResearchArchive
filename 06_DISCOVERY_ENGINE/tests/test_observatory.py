import hashlib
import inspect

import pytest

from tamesis_discovery_engine import observatory
from tamesis_discovery_engine.observatory import (
    Dataset,
    DatasetConflictError,
    DatasetNotFoundError,
    DatasetRegistry,
)

from .conftest import FakeClock


def make_registry(tmp_path, clock=None):
    return DatasetRegistry(data_dir=tmp_path / "datasets", clock=clock or FakeClock())


def test_ingest_then_get_in_fresh_registry_returns_identical_metadata(tmp_path):
    data_dir = tmp_path / "datasets"
    registry = DatasetRegistry(data_dir=data_dir, clock=FakeClock())
    content = b"PDG 2024 particle listings, synthetic stand-in bytes for testing."
    dataset = registry.ingest("pdg", "2024", "Particle Data Group, 2024 review", content)

    fresh_registry = DatasetRegistry(data_dir=data_dir, clock=FakeClock())
    reloaded = fresh_registry.get("pdg", "2024")

    assert reloaded == dataset
    assert reloaded.name == "pdg"
    assert reloaded.version == "2024"
    assert reloaded.source_citation == "Particle Data Group, 2024 review"
    assert reloaded.checksum == hashlib.sha256(content).hexdigest()
    assert reloaded.size_bytes == len(content)
    assert isinstance(reloaded, Dataset)


def test_reingesting_same_content_is_a_noop_and_different_content_raises(tmp_path):
    registry = make_registry(tmp_path)
    content = b"CODATA 2022 fundamental physical constants, synthetic stand-in."
    first = registry.ingest("codata", "2022", "CODATA 2022 recommended values", content)

    again = registry.ingest("codata", "2022", "CODATA 2022 recommended values", content)
    assert again == first

    with pytest.raises(DatasetConflictError) as excinfo:
        registry.ingest(
            "codata", "2022", "CODATA 2022 recommended values", b"a completely different payload"
        )
    assert excinfo.value.name == "codata"
    assert excinfo.value.version == "2022"
    assert excinfo.value.existing_checksum == first.checksum

    # the failed re-ingest attempt must not have mutated the persisted record
    assert registry.get("codata", "2022") == first
    assert registry.verify_integrity("codata", "2022") is True


def test_verify_integrity_true_then_false_after_on_disk_tampering(tmp_path):
    data_dir = tmp_path / "datasets"
    registry = DatasetRegistry(data_dir=data_dir, clock=FakeClock())
    content = b"Gaia DR3 astrometric catalog subset, synthetic stand-in bytes."
    registry.ingest("gaia", "dr3", "Gaia Data Release 3 astrometry", content)

    assert registry.verify_integrity("gaia", "dr3") is True

    content_path = data_dir / "gaia" / "dr3" / "content.bin"
    content_path.write_bytes(b"corrupted or tampered bytes on disk")

    assert registry.verify_integrity("gaia", "dr3") is False


def test_get_with_no_version_returns_the_most_recently_ingested_version(tmp_path):
    registry = make_registry(tmp_path)
    registry.ingest("sparc", "v1", "SPARC rotation curves, release v1", b"sparc v1 payload")
    registry.ingest("sparc", "v2", "SPARC rotation curves, release v2", b"sparc v2 payload")
    latest = registry.ingest("sparc", "v3", "SPARC rotation curves, release v3", b"sparc v3 payload")

    assert registry.get("sparc") == latest
    assert registry.get("sparc").version == "v3"

    with pytest.raises(DatasetNotFoundError):
        registry.get("no-such-dataset")

    with pytest.raises(DatasetNotFoundError):
        registry.get("sparc", "v99")


def test_record_usage_used_by_and_datasets_used_by_round_trip(tmp_path):
    registry = make_registry(tmp_path)
    planck = registry.ingest("planck", "2018", "Planck 2018 cosmological parameters", b"planck bytes")
    odlyzko = registry.ingest(
        "odlyzko", "zeta-zeros-1e8", "Odlyzko tables of Riemann zeta zeros", b"odlyzko bytes"
    )

    registry.record_usage("DISC-2026-00001", "planck", "2018")
    registry.record_usage("DISC-2026-00001", "odlyzko", "zeta-zeros-1e8")
    registry.record_usage("DISC-2026-00002", "planck", "2018")

    assert registry.used_by("planck", "2018") == ["DISC-2026-00001", "DISC-2026-00002"]
    assert registry.used_by("odlyzko", "zeta-zeros-1e8") == ["DISC-2026-00001"]
    assert registry.used_by("planck", "1900") == []

    used_by_claim_one = registry.datasets_used_by("DISC-2026-00001")
    assert used_by_claim_one == [planck, odlyzko]

    used_by_claim_two = registry.datasets_used_by("DISC-2026-00002")
    assert used_by_claim_two == [planck]

    assert registry.datasets_used_by("DISC-2026-99999") == []

    with pytest.raises(DatasetNotFoundError):
        registry.record_usage("DISC-2026-00003", "no-such-dataset", "v1")


def test_module_has_no_network_dependency():
    source = inspect.getsource(observatory)
    for forbidden in ("requests", "urllib", "httpx", "socket"):
        assert forbidden not in source, f"observatory.py must not reference {forbidden!r}"
