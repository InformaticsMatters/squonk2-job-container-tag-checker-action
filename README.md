# Squonk2 job definition container tag checker action
A GitHub Action that checks the repository's container image tags
present in Squonk2 Job Definition files. All container images must have
explicit and official tags, e.g. must be a sequence of numbers
using the pattern "N.N[.N]".

## Example usage
The repository under test is automatically mapped into the action container,
so you simply have to identify the action, after checking out the
repository's files...

```yaml
- name: Checkout
  uses: actions/checkout@v4
- name: Squonk2 job container tag checker
  uses: informaticsmatters/squonk2-job-container-tag-checker-action@v1
```
