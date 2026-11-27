"""The project's DOI link, which scripts/papers.py puts in a paper's alphaXiv submission."""

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
papers = importlib.import_module("papers")


def test_a_project_with_a_doi_links_it(tmp_path, monkeypatch):
    (tmp_path / "CITATION.cff").write_text("title: T\ndoi: 10.5281/zenodo.1\n", encoding="utf-8")
    monkeypatch.setattr(papers, "ROOT", tmp_path)
    assert papers.doi_link() == ["https://doi.org/10.5281/zenodo.1"]


def test_a_project_without_a_doi_has_no_doi_link(tmp_path, monkeypatch):
    # A project that Zenodo doesn't archive has no DOI in its CITATION.cff.
    (tmp_path / "CITATION.cff").write_text("title: T\n", encoding="utf-8")
    monkeypatch.setattr(papers, "ROOT", tmp_path)
    assert papers.doi_link() == []
