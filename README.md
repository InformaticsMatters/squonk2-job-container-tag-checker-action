# A job definition container tag checker action
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
- repo: https://github.com/InformaticsMatters/squonk2-job-container-tag-checker-action
  rev: 1.0.0-alpha.3
  hooks:
  - id: squonk2-job-container-tag-checker
```

---

[pre-commit]: https://pre-commit.com/
