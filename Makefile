# The example project's values for labinacan.mk (#6631). A new project sets its own.
DIST_NAME := labinacan
PACKAGES := labinacan
PROJECT_LINT := project-lint

include labinacan.mk

.PHONY: project-lint sample-run

# The project's own checks, which `make lint` runs: no word of another project.
project-lint:
	python3 scripts/check_leftovers.py

# The site that CI's accessibility check opens: here, the example project's own site.
sample-run: build
