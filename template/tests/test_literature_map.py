"""Every literature review is on the map that the literature index draws."""

from pathlib import Path

from labinacan.literature_map import COMMAND, missing_from_map

ROOT = Path(__file__).parents[1]


def test_every_review_is_on_the_map():
    missing = missing_from_map(ROOT)
    assert missing == [], f"not on docs/literature/map.json, run uv run --extra map {COMMAND}: {missing}"
