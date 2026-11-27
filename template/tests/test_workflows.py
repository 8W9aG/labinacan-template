"""The workflows install what each script that they run imports."""

import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
BARE = re.compile(r"(?<![\w/-])python3 (scripts/[\w./-]+\.py)")


def _needs_labinacan(script: Path, seen: set[Path] | None = None) -> bool:
    """Whether ``script`` imports labinacan, itself or through a script beside it."""
    seen = seen if seen is not None else set()
    if script in seen or not script.is_file():
        return False
    seen.add(script)
    text = script.read_text(encoding="utf-8")
    if re.search(r"^\s*(from|import) labinacan\b", text, re.M):
        return True
    local = re.findall(r"^\s*(?:from|import) (\w+)", text, re.M)
    return any(_needs_labinacan(script.parent / f"{name}.py", seen) for name in local)


def test_no_workflow_runs_a_script_that_needs_labinacan_with_bare_python():
    # A bare python3 has no labinacan: the Linear sync failed with ModuleNotFoundError.
    bad = [
        f"{workflow.name}: {path}"
        for workflow in sorted((ROOT / ".github" / "workflows").glob("*.yml"))
        for path in BARE.findall(workflow.read_text(encoding="utf-8"))
        if _needs_labinacan(ROOT / path)
    ]
    assert bad == []


def test_the_check_finds_a_script_that_imports_labinacan_through_another(tmp_path):
    (tmp_path / "a.py").write_text("import b\n")
    (tmp_path / "b.py").write_text("from labinacan.config import config\n")
    (tmp_path / "c.py").write_text("import json\n")
    assert _needs_labinacan(tmp_path / "a.py") and not _needs_labinacan(tmp_path / "c.py")


def test_auto_merge_merges_only_after_ci_passes():
    # Without required checks (a private repository on GitHub's free plan), `gh pr merge
    # --auto` merges at once. So the only merge is the one in merge_after_ci, after CI.
    text = (ROOT / ".github" / "workflows" / "auto-merge.yml").read_text(encoding="utf-8")
    body = text.split("merge_after_ci() {", 1)[1].split("\n          }\n", 1)[0]
    merges = re.findall(r"gh pr merge \"\$PR\" [^\n]*--squash", text)
    assert len(merges) == 1 and merges[0] in body
    assert 'if [ "$state" != passed ]; then' in body and "return 0" in body
