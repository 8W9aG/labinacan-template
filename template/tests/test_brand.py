"""The brand's committed SVGs are the ones that the config draws (#7002).

``scripts/setup_repo.py`` and ``scripts/brand_images.py`` write them. A change to
``[tool.labinacan.brand]``, or to the name, needs them drawn again.
"""

from __future__ import annotations

from pathlib import Path

from labinacan.config import use
from labinacan.site.brand import source, write_svgs

ROOT = Path(__file__).resolve().parents[1]


def test_the_committed_svgs_are_drawn_from_the_config(tmp_path):
    use(ROOT / "pyproject.toml")
    write_svgs(tmp_path)
    for name in ("mark.svg", "logo.svg"):
        drawn = (tmp_path / name).read_text(encoding="utf-8")
        assert (source() / name).read_text(encoding="utf-8") == drawn, (
            f"{name} is stale: run uv run python scripts/brand_images.py"
        )
