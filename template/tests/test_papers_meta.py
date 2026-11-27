"""Each paper's metadata file, which scripts/papers.py writes and checks (#3150)."""

import importlib
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
papers = importlib.import_module("papers")


def test_the_authors_are_the_projects_people_then_the_group(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nauthors = [{ name = "Ada Lovelace", email = "a@example.org" }]\n'
    )
    assert papers.authors(tmp_path) == [{"name": "Ada Lovelace"}, papers.GROUP]


def _paper(tmp_path) -> Path:
    """A papers/ folder with one listed paper that has a title, an abstract and a body."""
    papers_dir = tmp_path / "papers"
    (papers_dir / "p").mkdir(parents=True)
    (papers_dir / "README.md").write_text("# Papers\n\n- 2026-11-27: [P](p/README.md)\n")
    (papers_dir / "p" / "README.md").write_text("# P\n\nThe abstract.\n\n## Results\n\nText.\n")
    return papers_dir


def test_a_paper_yml_has_no_cff_fields_and_passes_the_check(tmp_path, monkeypatch):
    monkeypatch.setattr(papers, "META", "paper.yml")
    monkeypatch.setattr(papers, "CFF", False)
    papers_dir = _paper(tmp_path)
    papers.new("p", "#1 (the rest)", papers_dir)
    meta = yaml.safe_load((papers_dir / "p" / "paper.yml").read_text())
    assert "cff-version" not in meta and "message" not in meta
    assert meta["version"] == papers.PREPRINT and not (papers_dir / "p" / "CITATION.cff").exists()
    assert papers.check(papers_dir) == []

    papers.publish("p", papers_dir, today="2026-11-28")
    assert papers.check(papers_dir) == []
    (papers_dir / "p" / "README.md").write_text(
        (papers_dir / "p" / "README.md").read_text() + "A change.\n"
    )
    assert papers.check(papers_dir) == [
        "p: the published text or results changed: add an addendum instead"
    ]


def test_a_missing_paper_yml_names_the_file(tmp_path, monkeypatch):
    monkeypatch.setattr(papers, "META", "paper.yml")
    papers_dir = _paper(tmp_path)
    text = (papers_dir / "p" / "README.md").read_text()
    (papers_dir / "p" / "README.md").write_text(
        text.replace("The abstract.\n", "The abstract.\n\n**Status:** Preprint. Work left: #1\n")
    )
    assert papers.check(papers_dir) == ["p: no paper.yml (scripts/papers.py new)"]


def test_a_citation_cff_keeps_its_cff_fields(tmp_path, monkeypatch):
    monkeypatch.setattr(papers, "CFF", True)
    papers_dir = _paper(tmp_path)
    cff = papers.citation(papers_dir / "p", "2026-11-27", papers.PREPRINT)
    assert cff["cff-version"] == "1.2.0" and cff["type"] == "article"
