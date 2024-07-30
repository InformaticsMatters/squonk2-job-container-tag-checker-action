# Squonk2 job definition container tag checker action
A GitHub Action that checks the repository's container image tags
present in Squonk2 Job Definition files. All container images must have
explicit tags, i.e. cannot be `latest` or `stable`.

## Example usage
The repository is automaticlaly mapped into the action container,
so you simply have to identify the action, after having checked out the
repository..

```yaml
- name: Checkout
  uses: actions/checkout@v4
- name: Squonk2 job container tag checker
  uses: informaticsmatters/squonk2-job-container-tag-checker-action@v1
```
