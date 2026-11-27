"""The script values that scripts/repo_config.py reads from pyproject.toml."""

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
repo_config = importlib.import_module("repo_config")


def test_the_roadmap_project_is_the_number_that_the_config_gives(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[tool.labinacan]\nroadmap_project = 3\n")
    assert repo_config.roadmap_project(tmp_path) == 3


def test_a_project_with_no_roadmap_project_has_none(tmp_path):
    (tmp_path / "pyproject.toml").write_text('[tool.labinacan]\nname = "x"\n')
    assert repo_config.roadmap_project(tmp_path) is None
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "x"\n')
    assert repo_config.roadmap_project(tmp_path) is None
