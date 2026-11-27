# labinacan-template

The template of an agent-run research project. A new project gets a site, papers, posts and a literature review from the [labinacan](https://pypi.org/project/labinacan/) package. It also gets the checks that keep code and prose plain, a release, and the skills that agents follow to work its issues. It keeps only its own research code.

## Starting a new autoresearch project

1. **Create the repository** on GitHub, empty, and log in with `gh auth login`. The setup uses `gh` to configure the repository, so do this first.
2. **Copy the template** and answer its questions:

   ```bash
   uvx copier copy --trust gh:8W9aG/labinacan-template my-project
   ```

   The questions ask for these values:
   - the project's name, its package, its description and the maintainer's GitHub login;
   - the repository, the site's address, the Linear team and the Hugging Face dataset;
   - the brand's colours and the site's accent;
   - whether to publish the package to PyPI, whether Zenodo archives each release, and whether papers go to the alphaXiv AI Track (default: yes to all three). A local project answers no. Without PyPI it gets no publish workflow. Without Zenodo it gets no `CITATION.cff`: each paper keeps its metadata in `paper.yml`. Without alphaXiv it gets no `scripts/submit_paper.py`. The skills leave out the steps that are off;
   - whether to keep the example paper, post and literature review (default: no). Without them, `papers/`, `posts/` and `docs/literature/` start empty, and every check still passes.

   The answers write `pyproject.toml`, the `Makefile`, the README and the citations. `--trust` lets copier run the setup task, `scripts/setup_repo.py`. The task draws the brand. It creates the issue labels and sets the repository's description and homepage with `gh`. Then it lists what is left, such as the secrets to set.
3. **Push the first commit:**

   ```bash
   cd my-project
   git init && git add -A && git commit -m "The project, from labinacan-template"
   git remote add origin git@github.com:<owner>/<name>.git && git push -u origin main
   ```

   CI runs the project's checks on the push. A copy made with the default answers passes them, as this repository's own CI shows.
4. **Read the project's README.** It gives the next steps, such as the skills' own parts and the removal of the example's content.

To run the setup again, for example after creating the repository, use `uv run python scripts/setup_repo.py`.

### Without copier

GitHub's "Use this template" button gives this repository as it is, not a project: the project is the `template/` folder, and its `.jinja` files hold placeholders. To start by hand:

1. Move the contents of `template/` to the repository's root, and delete `copier.yml`, `ci/` and this README.
2. Drop the `.jinja` suffix from each file, and replace each `{{ name }}`, `{{ package }}` and every other placeholder with the project's own value. The questions in `copier.yml` list them, with their defaults. Rename the `{{package}}` folder to the package's name.
3. Fill in `[project]`, `[tool.labinacan]` and `[tool.labinacan.brand]` in `pyproject.toml`. Add the package to `PACKAGES` in the `Makefile` and to `[tool.mutmut] source_paths`.
4. Write each skill's `project.md` under `.claude/skills/`.
5. Delete the example paper, post and literature review, or keep them, and remove their lines from `papers/README.md`, `posts/README.md`, `docs/literature/README.md` and `docs/research-questions.md` if you delete them.
6. Put the project's own words in `scripts/leftover_terms.txt`, and run `python3 scripts/check_leftovers.py --update` for a new baseline.
7. Run `uv run python scripts/setup_repo.py` to draw the brand and set up the repository.

copier does all of this from the answers, so prefer it. A project started by hand can't take later changes with `copier update`.

## Taking later changes

In the project, run:

```bash
uvx copier update --trust
```

copier finds the changes to the template since the project's copy, from `.copier-answers.yml`. It applies them, and keeps the project's own changes. A clash shows as a Git conflict. A new release of `labinacan` comes in the same way: the template moves its pin in `pyproject.toml`. Run `copier update --trust --vcs-ref=HEAD` to take the template's newest commit instead of its newest tag.

## Layout

| Path | What it holds |
| --- | --- |
| `copier.yml` | the questions, and the setup task |
| `template/` | the project's files. A file whose name ends in `.jinja` holds an answer |
| `ci/check_update.sh` | the check that `copier update` takes a later change cleanly |
| `.github/workflows/template-ci.yml` | this repository's CI: a default copy, its checks and the update check |

## Develop

Make a copy with the default answers, and run its checks:

```bash
uvx copier copy --defaults --trust -d github_setup=false --vcs-ref HEAD . /tmp/project
cd /tmp/project && git init -q && git add -A && git commit -qm copy
make install lint test build
```

## Licence

MIT. See `LICENSE`.
