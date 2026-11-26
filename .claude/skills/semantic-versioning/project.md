# This project's surfaces

The `semantic-versioning` skill reads this file. A new project lists its own public surfaces here.

The package version is `labinacan.__version__`.

## The surfaces

A change is **breaking** when it breaks one of these for a project that uses the template:

- **The config.** A key of `[tool.labinacan]` is removed or renamed, or its meaning changes (`labinacan/config.py`).
- **The Python API.** A public name in `labinacan` is removed or renamed, or its signature changes in an incompatible way.
- **The Make targets.** A target or a variable of `labinacan.mk` is removed or renamed.

## How each one changed

```bash
last=$(git describe --tags --abbrev=0)
git diff "$last" -- labinacan/config.py labinacan.mk
```

## This project's own check

None.
