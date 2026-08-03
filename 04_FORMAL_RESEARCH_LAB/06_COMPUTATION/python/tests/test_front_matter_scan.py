"""Testes de regressao da cobertura do scanner em front matter Markdown.

O defeito historico nao estava no algoritmo de deteccao: ele sempre
funcionou. Estava na SELECAO de arquivos, que filtrava por extensao e
deixava de fora 332 documentos Markdown com front matter YAML — inclusive
`LAB_STATE.md`. A varredura era declarada integral e cobria 57 arquivos.

Estes testes fixam as duas coisas que mudaram: o escopo passou a incluir o
front matter, e `read_front_matter` deixou de aceitar "ultimo valor vence".
"""

import importlib.util
from pathlib import Path

import pytest

LAB_ROOT = Path(__file__).resolve().parents[3]
LABCTL_PATH = LAB_ROOT / "10_TOOLS" / "labctl.py"


def _load_labctl():
    spec = importlib.util.spec_from_file_location("labctl_front_matter", LABCTL_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


labctl = _load_labctl()


def _md(tmp_path: Path, text: str, name: str = "doc.md") -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_fm_test_001_clean_front_matter(tmp_path):
    """FM-TEST-001 — front matter limpo nao gera achado."""
    path = _md(tmp_path, "---\na: 1\nb: 2\n---\n\n# corpo\n")
    assert labctl.detect_duplicate_front_matter_keys(path) == []


def test_fm_test_002_duplicate_in_front_matter_is_detected(tmp_path):
    """FM-TEST-002 — a duplicata que antes passava agora eh encontrada."""
    path = _md(tmp_path, "---\nstatus: READY\nstatus: VERIFIED\n---\n\n# corpo\n")
    found = labctl.detect_duplicate_front_matter_keys(path)
    assert len(found) == 1
    assert found[0].key == "status"
    assert found[0].classification == "DIVERGENT_DUPLICATE"


def test_fm_test_003_identical_duplicate_also_rejected(tmp_path):
    """FM-TEST-003 — duplicata identica tambem eh proibida no front matter."""
    path = _md(tmp_path, "---\nstatus: READY\nstatus: READY\n---\n\n# corpo\n")
    found = labctl.detect_duplicate_front_matter_keys(path)
    assert len(found) == 1
    assert found[0].classification == "IDENTICAL_DUPLICATE"


def test_fm_test_004_reported_lines_map_to_the_file(tmp_path):
    """FM-TEST-004 — as linhas apontam para o arquivo, nao para o bloco."""
    path = _md(tmp_path, "---\nalpha: 1\nbeta: 2\nalpha: 3\n---\n\n# corpo\n")
    found = labctl.detect_duplicate_front_matter_keys(path)
    assert len(found) == 1
    # linha 1 eh o "---" de abertura; alpha aparece em 2 e reaparece em 4
    assert found[0].first_line == 2
    assert found[0].duplicate_line == 4


def test_fm_test_005_markdown_without_front_matter_is_ignored(tmp_path):
    """FM-TEST-005 — Markdown sem front matter nao produz achado nem erro."""
    path = _md(tmp_path, "# apenas um titulo\n\ntexto\n")
    assert labctl.detect_duplicate_front_matter_keys(path) == []


def test_fm_test_006_malformed_closing_delimiter_is_rejected(tmp_path):
    """FM-TEST-006 — delimitador de fechamento colado ao corpo eh malformado.

    Este eh exatamente o defeito encontrado em `LAB_STATE.md`: o `---` de
    fechamento dividia a linha com o primeiro titulo. Passava por ser
    aceito por uma expressao regular tolerante.
    """
    path = _md(tmp_path, "---\na: 1\n---# Estado atual\n")
    with pytest.raises(ValueError):
        labctl.detect_duplicate_front_matter_keys(path)


def test_fm_test_007_scan_reports_front_matter_scope(tmp_path):
    """FM-TEST-007 — a varredura reporta o escopo que realmente cobriu."""
    (tmp_path / "a.yaml").write_text("k: 1\n", encoding="utf-8")
    _md(tmp_path, "---\nk: 1\n---\n\n# c\n", "b.md")
    _md(tmp_path, "# sem front matter\n", "c.md")
    report = labctl.scan_duplicate_yaml_keys(tmp_path)
    assert report["yaml_files_scanned"] == 1
    assert report["markdown_files_seen"] == 2
    assert report["markdown_front_matter_scanned"] == 1
    assert report["files_scanned"] == 2
    assert report["duplicate_count"] == 0


def test_fm_test_008_scan_finds_duplicates_inside_markdown(tmp_path):
    """FM-TEST-008 — a varredura completa acha duplicata em Markdown."""
    _md(tmp_path, "---\nauthorized_action: A\nauthorized_action: B\n---\n\n# c\n")
    report = labctl.scan_duplicate_yaml_keys(tmp_path)
    assert report["duplicate_count"] == 1
    assert report["errors"][0].startswith(labctl.DUPLICATE_YAML_KEY)


def test_fm_test_009_malformed_front_matter_fails_the_scan(tmp_path):
    """FM-TEST-009 — front matter malformado reprova a varredura."""
    _md(tmp_path, "---\na: 1\n---# titulo\n")
    report = labctl.scan_duplicate_yaml_keys(tmp_path)
    assert len(report["malformed_front_matter"]) == 1
    assert any(e.startswith(labctl.MALFORMED_FRONT_MATTER) for e in report["errors"])


def test_fm_test_010_read_front_matter_rejects_duplicates(tmp_path):
    """FM-TEST-010 — "ultimo valor vence" deixou de ser aceito.

    Antes, `yaml.safe_load` resolvia silenciosamente para o ultimo valor.
    Num campo como `authorized_action` isso seria uma autorizacao escolhida
    pelo parser.
    """
    path = _md(tmp_path, "---\nauthorized_action: NOT_AUTHORIZED\nauthorized_action: EVERYTHING_AUTHORIZED\n---\n\n# c\n")
    with pytest.raises(ValueError) as excinfo:
        labctl.read_front_matter(path)
    assert labctl.DUPLICATE_YAML_KEY in str(excinfo.value)


def test_fm_test_011_read_front_matter_still_works_when_clean(tmp_path):
    """FM-TEST-011 — documento limpo continua sendo lido normalmente."""
    path = _md(tmp_path, "---\nid: X\nstatus: VERIFIED\n---\n\n# corpo\n")
    data, body = labctl.read_front_matter(path)
    assert data == {"id": "X", "status": "VERIFIED"}
    assert body.strip() == "# corpo"


def test_fm_test_012_lab_state_is_actually_covered():
    """FM-TEST-012 — LAB_STATE.md esta dentro da varredura.

    A regressao que este teste impede: voltar a declarar a varredura
    integral sem que o arquivo mais critico da governanca esteja nela.
    """
    markdown = labctl.markdown_files_under(labctl.LAB_ROOT)
    assert (labctl.LAB_ROOT / "LAB_STATE.md") in markdown
    assert labctl.detect_duplicate_front_matter_keys(labctl.LAB_ROOT / "LAB_STATE.md") == []


def test_fm_test_013_repository_front_matter_scan_is_clean():
    """FM-TEST-013 — a varredura ampliada do laboratorio esta limpa."""
    report = labctl.scan_duplicate_yaml_keys()
    assert report["duplicate_count"] == 0, report["errors"]
    assert report["malformed_front_matter"] == [], report["malformed_front_matter"]
    assert report["unparsable_files"] == []
    assert report["markdown_front_matter_scanned"] > 300
    assert report["files_scanned"] > report["yaml_files_scanned"]
