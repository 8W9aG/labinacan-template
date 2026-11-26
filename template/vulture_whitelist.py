"""Names that vulture reports as unused, but that a project calls: the package's public API.

The template has no research code of its own, so its public functions, such as the figure
helpers and the CLI commands a project mounts, have no caller here. Written with
``vulture labinacan scripts --make-whitelist``.
"""

# ruff: noqa
_.handle_starttag  # unused method (scripts/check_site_links.py:37)
_.MAX_WORDS  # unused attribute (scripts/ste_prose.py:62)
