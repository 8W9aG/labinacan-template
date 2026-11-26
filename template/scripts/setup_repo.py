"""Set up a new project after ``copier copy``: its brand and its GitHub repository (#7002).

copier runs this once, after the first copy (``copier.yml``, ``_tasks``). It does these steps:

1. It draws ``mark.svg`` and ``logo.svg`` from ``[tool.labinacan.brand]``. Then it tries to
   draw the PNGs (``scripts/brand_images.py``), which need Chrome.
2. It uses ``gh`` to create the issue labels that the skills read. It also sets the
   repository's description and homepage. ``--brand-only`` skips this step.
3. It lists the secrets that the workflows read. ``gh`` can't know their values, so the
   maintainer sets them.

Each step that can't run here is printed with what to do, and the script still exits 0, so
that the copy is kept. Run it again at any time::

    uv run python scripts/setup_repo.py
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from labinacan.config import config, use  # noqa: E402

# The labels that the skills and scripts/next_issue.py read, with a colour and a meaning.
LABELS = {
    "priority: urgent": ("B60205", "Breaks CI, a release or stored records"),
    "priority: high": ("D93F0B", "Blocks a new result, or lets a wrong one through"),
    "priority: medium": ("FBCA04", "Useful, and blocks nothing"),
    "priority: low": ("C2E0C6", "Nice to have"),
    "proposed": ("EDEDED", "Held back until the maintainer removes this label"),
    "area: code quality and tooling": ("1D76DB", "Checks, scripts and CI"),
    "area: literature": ("5319E7", "A review of a paper or post"),
    "area: papers": ("0E8A16", "A paper, its figures and references"),
    "area: site": ("006B75", "The built site"),
}

# The secrets that the workflows read (.github/workflows), and what each one is for.
SECRETS = {
    "LINEAR_API_KEY": "the two-way sync of issues with Linear",
    "ROADMAP_TOKEN": "the Priority field of the GitHub Roadmap project",
    "HF_TOKEN": "the link check, which reads from Hugging Face (a read-only token)",
}

Runner = Callable[[Sequence[str]], subprocess.CompletedProcess]


def _run(cmd: Sequence[str]) -> subprocess.CompletedProcess:
    """Run ``cmd`` and capture its output. A failure is returned, not raised.

    Args:
        cmd: The command and its arguments.

    Returns:
        The finished process.
    """
    return subprocess.run(list(cmd), capture_output=True, text=True, check=False)


def draw_brand(todo: list[str], run: Runner = _run) -> None:
    """Write the brand's SVGs, then try to draw its PNGs, which need Chrome.

    Args:
        todo: The list of what couldn't run, which this appends to.
        run: Runs a command (a parameter so that tests can replace it).
    """
    from labinacan.site.brand import write_svgs

    write_svgs()
    drawn = run([sys.executable, str(ROOT / "scripts" / "brand_images.py")])
    if drawn.returncode != 0:
        todo.append("Draw the brand's PNGs where Chrome is installed: "
                    "uv run python scripts/brand_images.py")  # fmt: skip


def setup_github(todo: list[str], run: Runner = _run) -> None:
    """Create the labels, and set the description and homepage, of the project's repository.

    Args:
        todo: The list of what couldn't run, which this appends to.
        run: Runs a command (a parameter so that tests can replace it).
    """
    c = config()
    repo = c.repo
    if shutil.which("gh") is None:
        todo.append("Install gh (cli.github.com), then run: uv run python scripts/setup_repo.py")
        return
    if run(["gh", "auth", "status"]).returncode != 0:
        todo.append("Log in with gh auth login, then run: uv run python scripts/setup_repo.py")
        return
    if run(["gh", "repo", "view", repo]).returncode != 0:
        todo.append(f"Create {repo} on GitHub and push, then run: "
                    "uv run python scripts/setup_repo.py")  # fmt: skip
        return
    for name, (colour, meaning) in LABELS.items():
        made = run(["gh", "label", "create", name, "--repo", repo, "--force",
                    "--color", colour, "--description", meaning])  # fmt: skip
        if made.returncode != 0:
            todo.append(f"Create the label {name!r}: {made.stderr.strip()}")
    edited = run(["gh", "repo", "edit", repo, "--description", c.description,
                  "--homepage", c.site_url])  # fmt: skip
    if edited.returncode != 0:
        todo.append(f"Set the repository's description and homepage: {edited.stderr.strip()}")
    print(f"Set up {repo}: {len(LABELS)} labels, the description and the homepage.")


def secrets_todo() -> list[str]:
    """What the maintainer must set by hand: each secret that the workflows read.

    Returns:
        One line for each secret.

    Examples:
        >>> secrets_todo()[0].startswith("Set the secret LINEAR_API_KEY (gh secret set")
        True
    """
    return [f"Set the secret {name} (gh secret set {name}), for {why}"
            for name, why in SECRETS.items()]  # fmt: skip


def main(argv: Sequence[str] | None = None, run: Runner = _run) -> list[str]:
    """Set up the project, and print what is left to do.

    Args:
        argv: The command line. ``--brand-only`` skips the repository.
        run: Runs a command (a parameter so that tests can replace it).

    Returns:
        What couldn't run here, in the order printed.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--brand-only", action="store_true", help="draw the brand only")
    args = parser.parse_args(argv)
    use(ROOT / "pyproject.toml")
    todo: list[str] = []
    draw_brand(todo, run)
    if not args.brand_only:
        setup_github(todo, run)
    todo += secrets_todo()
    print("Left to do:" if todo else "Nothing left to do.")
    for line in todo:
        print(f"- {line}")
    return todo


if __name__ == "__main__":
    main()
