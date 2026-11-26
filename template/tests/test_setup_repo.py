"""The setup after ``copier copy`` (scripts/setup_repo.py, #7002), with ``gh`` faked."""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location("setup_repo", ROOT / "scripts" / "setup_repo.py")
setup_repo = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(setup_repo)


class Fake:
    """Records each command, and fails the ones whose start is in ``fail``."""

    def __init__(self, *fail: tuple[str, ...]):
        self.calls: list[list[str]] = []
        self.fail = fail

    def __call__(self, cmd):
        cmd = list(cmd)
        self.calls.append(cmd)
        code = 1 if any(tuple(cmd[: len(f)]) == f for f in self.fail) else 0
        return subprocess.CompletedProcess(cmd, code, "", "refused" if code else "")

    def gh(self, *start: str) -> list[list[str]]:
        """The calls of ``gh`` that start with ``start``."""
        return [c for c in self.calls if c[: len(start) + 1] == ["gh", *start]]


@pytest.fixture
def brand(monkeypatch):
    """The brand's SVGs are drawn into nothing, so a test writes no committed file."""
    drawn = []
    monkeypatch.setattr("labinacan.site.brand.write_svgs", lambda: drawn.append(True))
    return drawn


@pytest.fixture
def with_gh(monkeypatch):
    monkeypatch.setattr(setup_repo.shutil, "which", lambda name: f"/bin/{name}")


def test_a_full_setup_makes_every_label_and_sets_the_repo(brand, with_gh, capsys):
    run = Fake()
    todo = setup_repo.main([], run)
    repo = setup_repo.config().repo
    assert brand == [True]
    assert run.calls[0][1].endswith("brand_images.py")
    assert [c[3] for c in run.gh("label", "create")] == list(setup_repo.LABELS)
    assert all(c[4:6] == ["--repo", repo] for c in run.gh("label", "create"))
    assert run.gh("repo", "edit") == [["gh", "repo", "edit", repo, "--description",
                                        setup_repo.config().description,
                                        "--homepage", setup_repo.config().site_url]]  # fmt: skip
    assert todo == setup_repo.secrets_todo()
    out = capsys.readouterr().out
    assert f"Set up {repo}: {len(setup_repo.LABELS)} labels" in out
    assert out.count("\n- ") == len(setup_repo.SECRETS)


def test_brand_only_never_calls_gh(brand, with_gh):
    run = Fake()
    assert setup_repo.main(["--brand-only"], run) == setup_repo.secrets_todo()
    assert run.gh() == []


def test_pngs_that_cant_be_drawn_are_left_to_do(brand):
    run = Fake((setup_repo.sys.executable,))
    todo: list[str] = []
    setup_repo.draw_brand(todo, run)
    assert todo == ["Draw the brand's PNGs where Chrome is installed: "
                    "uv run python scripts/brand_images.py"]  # fmt: skip


def test_no_gh_is_left_to_do(monkeypatch):
    monkeypatch.setattr(setup_repo.shutil, "which", lambda name: None)
    todo: list[str] = []
    setup_repo.setup_github(todo, Fake())
    assert todo == ["Install gh (cli.github.com), then run: uv run python scripts/setup_repo.py"]


@pytest.mark.parametrize(
    ("fails", "says"),
    [
        (("gh", "auth"), "Log in with gh auth login"),
        (("gh", "repo", "view"), "Create {repo} on GitHub and push"),
    ],
)
def test_no_login_or_no_repo_stops_before_any_change(with_gh, fails, says):
    run = Fake(fails)
    todo: list[str] = []
    setup_repo.setup_github(todo, run)
    assert len(todo) == 1
    assert todo[0].startswith(says.format(repo=setup_repo.config().repo))
    assert run.gh("label") == [] and run.gh("repo", "edit") == []


def test_each_refused_change_is_left_to_do(with_gh):
    run = Fake(("gh", "label", "create", "proposed"), ("gh", "repo", "edit"))
    todo: list[str] = []
    setup_repo.setup_github(todo, run)
    assert todo == [
        "Create the label 'proposed': refused",
        "Set the repository's description and homepage: refused",
    ]
    assert len(run.gh("label", "create")) == len(setup_repo.LABELS)  # the others still made


def test_nothing_left_is_said(brand, monkeypatch, capsys):
    monkeypatch.setattr(setup_repo, "secrets_todo", list)
    assert setup_repo.main(["--brand-only"], Fake()) == []
    assert capsys.readouterr().out == "Nothing left to do.\n"


def test_the_real_runner_returns_a_failure_instead_of_raising():
    done = setup_repo._run([setup_repo.sys.executable, "-c", "import sys; sys.exit(3)"])
    assert done.returncode == 3
