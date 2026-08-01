"""Testes de regressao do detector de chaves YAML duplicadas.

A politica do laboratorio nao aceita "ultimo valor vence": um mapa com
duas definicoes da mesma chave nao possui semantica univoca, ainda que os
valores coincidam. Estes testes nao consideram sucesso o fato de
`yaml.safe_load` devolver um objeto — ele devolve, e eh justamente esse o
problema.
"""

import importlib.util
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[3]
LABCTL_PATH = LAB_ROOT / "10_TOOLS" / "labctl.py"


def _load_labctl():
    spec = importlib.util.spec_from_file_location("labctl_yaml_dup", LABCTL_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


labctl = _load_labctl()


def _write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "sample.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_yaml_test_001_clean_file(tmp_path):
    """YAML-TEST-001 — arquivo limpo nao gera achado."""
    path = _write(tmp_path, "a: 1\nb: 2\n")
    assert labctl.detect_duplicate_yaml_keys(path) == []


def test_yaml_test_002_identical_duplicate(tmp_path):
    """YAML-TEST-002 — duplicata identica tambem eh proibida."""
    path = _write(tmp_path, "a: 1\na: 1\n")
    found = labctl.detect_duplicate_yaml_keys(path)
    assert len(found) == 1
    assert found[0].key == "a"
    assert found[0].classification == "IDENTICAL_DUPLICATE"
    assert labctl.DUPLICATE_YAML_KEY in found[0].as_error()


def test_yaml_test_003_divergent_duplicate(tmp_path):
    """YAML-TEST-003 — duplicata divergente eh classificada como tal."""
    path = _write(tmp_path, "a: 1\na: 2\n")
    found = labctl.detect_duplicate_yaml_keys(path)
    assert len(found) == 1
    assert found[0].classification == "DIVERGENT_DUPLICATE"
    assert found[0].first_value == "1"
    assert found[0].duplicate_value == "2"


def test_yaml_test_004_nested_mapping(tmp_path):
    """YAML-TEST-004 — duplicata em mapa aninhado, com caminho completo."""
    path = _write(tmp_path, "root:\n  item:\n    status: READY\n    status: VERIFIED\n")
    found = labctl.detect_duplicate_yaml_keys(path)
    assert len(found) == 1
    assert found[0].mapping_path == "root.item"
    assert found[0].key == "status"
    assert found[0].classification == "DIVERGENT_DUPLICATE"


def test_yaml_test_005_mapping_inside_sequence(tmp_path):
    """YAML-TEST-005 — mapa dentro de sequencia, com indice no caminho."""
    path = _write(tmp_path, "items:\n  - id: A\n    status: READY\n    status: VERIFIED\n")
    found = labctl.detect_duplicate_yaml_keys(path)
    assert len(found) == 1
    assert found[0].mapping_path == "items[0]"
    assert found[0].key == "status"


def test_yaml_test_006_same_key_in_distinct_mappings(tmp_path):
    """YAML-TEST-006 — a mesma chave em mapas distintos nao eh duplicata."""
    path = _write(tmp_path, "first:\n  status: READY\nsecond:\n  status: VERIFIED\n")
    assert labctl.detect_duplicate_yaml_keys(path) == []


def test_yaml_test_007_multiple_documents(tmp_path):
    """YAML-TEST-007 — todos os documentos separados por --- sao percorridos."""
    path = _write(tmp_path, "a: 1\nb: 2\n---\nc: 3\nc: 4\n")
    found = labctl.detect_duplicate_yaml_keys(path)
    assert len(found) == 1
    assert found[0].document_index == 1
    assert found[0].key == "c"


def test_yaml_test_008_reported_lines(tmp_path):
    """YAML-TEST-008 — a primeira linha e a linha duplicada sao exatas."""
    path = _write(tmp_path, "# comentario\nalpha: 1\nbeta: 2\nalpha: 3\n")
    found = labctl.detect_duplicate_yaml_keys(path)
    assert len(found) == 1
    assert found[0].first_line == 2
    assert found[0].duplicate_line == 4
    error = found[0].as_error()
    assert ":4 " in error
    assert "first_defined_at=2" in error


def test_yaml_test_009_sequence_values_are_not_duplicates(tmp_path):
    """Valores repetidos em lista NAO sao chaves duplicadas."""
    path = _write(tmp_path, "items:\n  - NOT_AUTHORIZED\n  - NOT_AUTHORIZED\n")
    assert labctl.detect_duplicate_yaml_keys(path) == []


def test_repository_scan_is_clean():
    """A varredura integral do laboratorio nao pode ter duplicatas."""
    report = labctl.scan_duplicate_yaml_keys()
    assert report["duplicate_count"] == 0, report["errors"]
    assert report["files_with_duplicates"] == 0
    assert report["unparsable_files"] == []
    assert report["files_scanned"] > 0


def test_validate_rejects_duplicate_keys(tmp_path, monkeypatch):
    """Qualquer duplicata faz `labctl validate` reprovar, com o codigo certo."""
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "dup.yaml").write_text("k: 1\nk: 1\n", encoding="utf-8")
    report = labctl.scan_duplicate_yaml_keys(tmp_path)
    assert report["duplicate_count"] == 1
    assert report["identical_duplicates"] == 1
    assert report["errors"][0].startswith(labctl.DUPLICATE_YAML_KEY)


def test_scan_ignores_generated_directories(tmp_path):
    """Diretorios de dependencia e cache ficam fora do escopo."""
    for excluded in (".lake", "__pycache__", ".venv", "node_modules"):
        directory = tmp_path / excluded
        directory.mkdir()
        (directory / "dup.yaml").write_text("k: 1\nk: 2\n", encoding="utf-8")
    report = labctl.scan_duplicate_yaml_keys(tmp_path)
    assert report["files_scanned"] == 0
    assert report["duplicate_count"] == 0
