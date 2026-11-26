# What the template holds

An agent-run research project needs much more than its research code: a site, papers with checked references, a literature review, a release, and rules that keep its prose plain. We cut those parts out of the repository of one such project and measured what the cut holds. It keeps 186 commits of history, 45 modules of a package, 14 page templates, 29 scripts and 11 skills. A lint of 19 commands and 314 tests pass on it with no file of the first project's field. A new project starts from this cut and adds only its own research.

**Status:** Preprint. Work left: #1 (a figure of the cut's growth over its releases).

## Introduction

A project in which agents propose, test and write up results spends much of its code on what is not research. Its site has to show papers and posts. Its papers need references that resolve, and figures drawn from data. Its agents need written rules for picking issues and releasing versions. When this code lives inside the first project, a second project has to copy it and then keep the copies in step by hand.

This paper describes the template that holds that code for any project. Its contributions are these:

- A measure of what the template holds when it is cut from its first project (Table 1).
- The checks that pass on the template alone.

The paper bears on research question 0, *Can a new research project start from the template in a day?* ([research questions](../../docs/research-questions.md)).

## Related work

The release follows Semantic Versioning (Preston-Werner, 2013): a change that breaks the public interface bumps the major version, and while the version is 0.y.z, anything may change. The literature review's page on the specification says how the template uses it.

## Method

We cut the template from its first project's repository with `git filter-repo`, which keeps the history of a list of paths and drops the rest. Each count in Table 1 is a file count of the cut, made with `git ls-files`, or the output of its own checks.

## The size of the cut

We asked how much of a project's code is generic. Table 1 gives what the cut holds.

**Table 1.** What the template holds when it is cut, and the checks that pass on it.

| Measure | Count |
| --- | --- |
| Commits of history | 186 |
| Package modules | 45 |
| Page templates | 14 |
| Scripts | 29 |
| Skills | 11 |
| Workflows | 8 |
| Test files | 29 |
| Lint commands | 19 |
| Tests that pass | 314 |

The package and the scripts are most of the cut. Two tests skip: the example project lists no workflow whose issues an agent may work, and it has no package of its own beside the template's.

## Discussion

The counts show that a small research project can start with a site, a release and a set of checks already in place. The skills are the part that a new project changes most, because each one has a part of its own.

## Limitations

The counts describe one cut at one date. They change with each release of the template.

## Conclusion

The template holds the generic parts of an agent-run research project, with their history, and its checks pass on it alone.

## References

- Preston-Werner, T. (2013). *Semantic versioning 2.0.0*. [semver.org](https://semver.org/spec/v2.0.0.html).

## Appendices

### Reproduce

```bash
git ls-files 'labinacan/*.py' | wc -l
make lint test
```
