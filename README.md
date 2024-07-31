# A job definition image tag checker action

[![build](https://github.com/informaticsmatters/squonk2-job-image-tag-checker-action/actions/workflows/build.yaml/badge.svg)](https://github.com/informaticsmatters/squonk2-job-image-tag-checker-action/actions/workflows/build.yaml)


![GitHub Tag](https://img.shields.io/github/v/tag/informaticsmatters/squonk2-job-image-tag-checker-action)

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A GitHub Action that is used to check Squonk2 Job Definition repositories to
check the validity of container image tags found in Job Definition and
Nextflow files.

All container images must have explicit and official tags that
must be a sequence of numbers using the pattern `N.N[.N]`.

The action can also be used as a [pre-commit] hook.

## Example usage (as an Action)
The repository under test is automatically mapped into the action's container,
so you simply have to identify the action, after checking out the repository's files...

```yaml
- name: Checkout
  uses: actions/checkout@v4
- name: Squonk2 job container tag checker
  uses: informaticsmatters/squonk2-job-container-tag-checker-action@v1
```

## Example usage (using pre-commit)
The repository code can also be used as a [pre-commit] hook. To do this you simply
need to add a `.pre-commit-config.yaml` file to the root of the repository you want to
use the pre-commit hook in with the following `repo` definition: -

```yaml
- repo: https://github.com/InformaticsMatters/squonk2-job-image-tag-checker-action
  rev: 1.0.0-alpha.5
  hooks:
  - id: squonk2-job-image-tag-checker
```

## Contributing
The project uses: -

- [pre-commit] to enforce linting of files prior to committing them to the
  upstream repository
- [Commitizen] to enforce a [Conventional Commit] commit message format
- [Black] as a code formatter

You **MUST** comply with these choices in order to  contribute to the project.

To get started review the pre-commit utility and the conventional commit style
and then setup your local clone by following the **Installation** and
**Quick Start** sections: -

    pip install --upgrade pip
    pip install -r build-requirements.txt
    pre-commit install -t commit-msg -t pre-commit

Now the project's rules will run on every commit, and you can check the
current health of your clone with: -

    pre-commit run --all-files

Create a virtual environment if you're going to develop code.

---

[black]: https://black.readthedocs.io/en/stable
[commitizen]: https://commitizen-tools.github.io/commitizen/
[conventional commit]: https://www.conventionalcommits.org/en/v1.0.0/
[pre-commit]: https://pre-commit.com
