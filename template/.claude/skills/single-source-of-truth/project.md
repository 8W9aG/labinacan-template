# This project's sources

The `single-source-of-truth` skill reads this file. A new project adds its own rows here.

## Where definitions live

| Concept | Source |
| --- | --- |
| The project's name, package, URLs and team | `[project]` and `[tool.labinacan]` in `pyproject.toml`, read by `labinacan/config.py` |
| The brand: the mark's cells and colours, and the accent | `[tool.labinacan.brand]` in `pyproject.toml` |
| Every page's site-wide values | `labinacan/site/build.py` (`build`) |
| The packages, generated files and other script values | `scripts/repo_config.py` |

## Copies that must exist

A test of a copy goes beside the test of what it copies, in `tests/`.
