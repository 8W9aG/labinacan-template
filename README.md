# labinacan

labinacan is the part of an agent-run research project that doesn't depend on what it studies. It gives the project its site, papers, posts and literature review. It also gives the checks that keep code and prose plain, the release, and the skills that agents follow to work the project's issues.

This repository is also the example project. Its own `pyproject.toml`, papers, posts and review are the smallest project that builds and passes CI.

## Starting a new autoresearch project

1. **Copy the template.** Use this repository as a template on GitHub, or clone it, into a repository of your own.
2. **Name the project.** In `pyproject.toml`, set `[project]` (the distribution's name, its description, its URLs and its maintainer) and `[tool.labinacan]`:

   | Key | What it is |
   | --- | --- |
   | `name` | the project's name as people read it |
   | `package` | its Python package, which holds `__version__` |
   | `env_prefix` | the prefix of its environment variables |
   | `linear_team` | the Linear team that mirrors its issues |
   | `maintainer` | the maintainer's GitHub login, whose issues agents may work |
   | `hf_dataset` | the Hugging Face dataset of the inputs that its papers cite |
   | `generated` | the files that a tool writes, which the checks of hand-written files skip |
   | `data_only` | the folders whose changes alone run no lint and tests |
   | `automatic_issue_workflows` | the workflows whose failure issues an agent may work |

   `[tool.labinacan.brand]` draws the mark, the logo and the social card, and gives the site's accent. `[tool.labinacan.size_budget]`, `[tool.labinacan.exchange]` and `[tool.labinacan.breaking]` are optional.
3. **Add your package** beside `labinacan/`, and list it in `PACKAGES` in the `Makefile` and in `[tool.mutmut] source_paths`. `labinacan/` imports nothing from it, and `tests/test_labinacan_boundary.py` checks that.
4. **Write the project's part of each skill.** A skill that has a `project.md` beside its `SKILL.md` reads it first. Examples are the release's own steps, the breaking surfaces, a paper's authors and the priorities of issues. Copy the example's and change it.
5. **Build and check:** `make install`, `make lint`, `make test`, then `make build` and `make serve`.
6. **Remove the example's content:** the sample paper in `papers/`, the post in `posts/`, the review in `docs/literature/` and `CHANGELOG.md`'s entries. Write your own.

`scripts/check_leftovers.py` finds words of another project in the template's files. A new project runs it once with its own words in `scripts/leftover_terms.txt` and a baseline of its own.

## Layout

| Path | What it holds |
| --- | --- |
| `labinacan/` | the package: config, site build, papers, posts, literature pages, PII checks, social posting, R2 sync |
| `labinacan.mk` | the Make targets that the `Makefile` includes |
| `scripts/` | the checks of code and prose, the changelog, mutation testing, the issue loop and Linear sync |
| `.claude/skills/` | the skills that agents follow |
| `.github/workflows/` | CI, CodeQL, the secret scan, the link check, publishing and issue syncs |
| `papers/`, `posts/`, `docs/literature/` | the example project's content |

## Licence

MIT. See `LICENSE`.
