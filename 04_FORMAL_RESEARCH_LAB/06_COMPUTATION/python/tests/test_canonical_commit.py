"""Testes da validacao nao destrutiva de LAB_STATE.canonical_commit.

O `runner` do labctl eh injetado, entao a tabela de decisao eh testada sem
tocar no repositorio: nenhum branch eh criado e nenhum historico eh
reescrito.
"""

import importlib.util
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[3]
LABCTL_PATH = LAB_ROOT / "10_TOOLS" / "labctl.py"


def _load_labctl():
    spec = importlib.util.spec_from_file_location("labctl_under_test", LABCTL_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


labctl = _load_labctl()

SHA = "39e3d95925a7038da307017216dd4cb8e49c572a"


class Recorder:
    """Runner falso: devolve codigos programados e grava os comandos."""

    def __init__(self, cat_file: int, ancestor: int | None = None):
        self.cat_file = cat_file
        self.ancestor = ancestor
        self.calls: list[list[str]] = []

    def __call__(self, args: list[str]) -> int:
        self.calls.append(list(args))
        if args[1] == "cat-file":
            return self.cat_file
        if args[1] == "merge-base":
            assert self.ancestor is not None, "merge-base nao deveria ser chamado"
            return self.ancestor
        raise AssertionError(f"comando git inesperado: {args}")


def test_missing_canonical_commit_is_unavailable():
    runner = Recorder(cat_file=0, ancestor=0)
    result = labctl.check_canonical_commit(None, runner=runner)
    assert result["status"] == labctl.CANONICAL_COMMIT_UNAVAILABLE
    assert runner.calls == [], "git nao deve ser chamado sem commit"


def test_absent_object_is_unavailable_and_recommends_full_history():
    runner = Recorder(cat_file=128)
    result = labctl.check_canonical_commit(SHA, runner=runner)
    assert result["status"] == labctl.CANONICAL_COMMIT_UNAVAILABLE
    assert "unshallow" in result["message"]
    # merge-base nao deve ser tentado se o objeto nem existe
    assert [c[1] for c in runner.calls] == ["cat-file"]


def test_ancestor_exit_zero_is_pass():
    runner = Recorder(cat_file=0, ancestor=0)
    result = labctl.check_canonical_commit(SHA, runner=runner)
    assert result["status"] == labctl.CANONICAL_COMMIT_PASS
    assert [c[1] for c in runner.calls] == ["cat-file", "merge-base"]


def test_equality_with_head_is_accepted():
    """canonical_commit == HEAD deve passar: a ancestralidade nao eh estrita.

    O teste confirma que a implementacao delega a decisao ao proprio git
    (`merge-base --is-ancestor` eh reflexivo) e NAO acrescenta uma comparacao
    `canonical_commit != HEAD`.
    """
    runner = Recorder(cat_file=0, ancestor=0)
    result = labctl.check_canonical_commit(SHA, runner=runner)
    assert result["status"] == labctl.CANONICAL_COMMIT_PASS
    assert runner.calls == [
        ["git", "cat-file", "-e", f"{SHA}^{{commit}}"],
        ["git", "merge-base", "--is-ancestor", SHA, "HEAD"],
    ]
    # nenhuma consulta extra a HEAD para rejeitar igualdade
    assert not any("rev-parse" in c for c in runner.calls)


def test_non_ancestor_exit_one_is_error():
    runner = Recorder(cat_file=0, ancestor=1)
    result = labctl.check_canonical_commit(SHA, runner=runner)
    assert result["status"] == labctl.CANONICAL_COMMIT_NOT_ANCESTOR
    assert result["exit_code"] == 1


def test_git_failure_is_not_reported_as_non_ancestor():
    """Exit diferente de 0 e 1 eh erro do git, nao veredito de ancestralidade."""
    for code in (2, 128, 129):
        runner = Recorder(cat_file=0, ancestor=code)
        result = labctl.check_canonical_commit(SHA, runner=runner)
        assert result["status"] == labctl.CANONICAL_COMMIT_GIT_ERROR
        assert result["status"] != labctl.CANONICAL_COMMIT_NOT_ANCESTOR
        assert result["exit_code"] == code


def test_statuses_are_distinct():
    statuses = {
        labctl.CANONICAL_COMMIT_PASS,
        labctl.CANONICAL_COMMIT_UNAVAILABLE,
        labctl.CANONICAL_COMMIT_NOT_ANCESTOR,
        labctl.CANONICAL_COMMIT_GIT_ERROR,
    }
    assert len(statuses) == 4
