# Development Guide

This project follows a standard `src/` layout with packaging metadata defined in `pyproject.toml`.

## Requirements

- Python 3.8+
- `pip` for dependency management

Install dev dependencies:

```bash
pip install -e .[dev]
```

## Code quality

Run Ruff to lint the code base:

```bash
ruff check .
```

## Testing & coverage

Tests are written with `pytest` and collect coverage information automatically.

```bash
pytest
```

Coverage reports are printed to the terminal and should remain near 100% for new contributions.

## Continuous integration

GitHub Actions executes linting and test jobs on every push and pull request (`.github/workflows/ci.yml`). Ensure the workflow passes locally before submitting changes.

## Releasing

1. Update the version in `pyproject.toml` and `readme.md` if necessary.
2. Build the distribution:

   ```bash
   python -m build
   ```

3. Publish via your preferred tooling, e.g. `twine`.
