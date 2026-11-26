#!/usr/bin/env bash
# Check that `copier update` takes a later template change cleanly (#7002). It copies the
# project from a scratch clone of this template, commits it, adds a change to the clone, and
# updates. It fails on a conflict, a .rej file, or a change that didn't arrive.
set -euo pipefail

work="$(mktemp -d)"
git clone --quiet "$(git rev-parse --show-toplevel)" "$work/template"
git -C "$work/template" checkout --quiet "$(git rev-parse HEAD)"
git -C "$work/template" switch --quiet -c update-check
copier copy --quiet --defaults --trust -d github_setup=false --vcs-ref HEAD \
  "$work/template" "$work/project"
git -C "$work/project" init --quiet
git -C "$work/project" add -A
git -C "$work/project" -c user.name=ci -c user.email=ci@example.org commit --quiet -m copy

marker="# A later change of the template, which copier update must bring in."
echo "$marker" >> "$work/template/template/labinacan.mk"
git -C "$work/template" -c user.name=ci -c user.email=ci@example.org commit --quiet -am later

cd "$work/project"
copier update --quiet --defaults --trust --vcs-ref HEAD
if find . -name '*.rej' -not -path './.git/*' | grep -q .; then
  echo "copier update left .rej files"; exit 1
fi
if git diff --name-only --diff-filter=U | grep -q .; then
  echo "copier update left conflicts"; exit 1
fi
grep -qxF "$marker" labinacan.mk || { echo "the template's change didn't arrive"; exit 1; }
changed="$(git status --porcelain | awk '{print $2}' | sort | tr '\n' ' ')"
[ "$changed" = ".copier-answers.yml labinacan.mk " ] \
  || { echo "copier update changed more than it should: $changed"; exit 1; }
echo "copier update took the template's change cleanly."
