set dotenv-load := true
set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

default:
    @just --list

help:
    @just --list

# Sync template dependencies to root for IDE support
sync:
    python scripts/sync-deps.py

# Generate a test project
test-gen:
    python scripts/generate-project.py /tmp/django-test-project

# Run tests in a newly generated test project
test: test-gen
    cd /tmp/django-test-project/src && uv sync && uv run manage.py test

# Clean up generated test projects
clean:
    rm -rf /tmp/django-test-project

# Lint the code using ruff and ty
lint:
    ruff check --extend-exclude "{{'{{'}}cookiecutter.project_slug{{'}}'}}" --extend-exclude "{{'{{'}} cookiecutter.project_slug {{'}}'}}" .
    ty check .

# Format the code using ruff
format:
    ruff format .