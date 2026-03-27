# Cookiecutter Template

## Generate A Project (directly into target root)

Use the root script to render a project into a target directory without creating an extra nested
`<project_slug>` folder:

```bash
./generate-project.sh ./my-new-api
```

Equivalent Python entrypoint:

```bash
./generate-project.py ./my-new-api
```

### Non-interactive example

```bash
./generate-project.py ./my-new-api \
  --no-input \
  --context project_name="My New API" \
  --context project_slug="my_new_api" \
  --context github_username="my-org"
```

### Useful flags

- `--force`: allow generation into a non-empty target directory (merge/overwrite)
- `--template`: use a different template path (defaults to this repository)
- `--context KEY=VALUE`: override cookiecutter context values (can be repeated)

## Raw Cookiecutter (default nested output)

If you want plain cookiecutter behavior (creates `<output>/<project_slug>`):

```bash
cookiecutter .
cookiecutter . -o ./cookiecutter-output
```

## Key prompts

- `project_name`
- `project_slug`
- `distribution_name`
- `docker_name_prefix`
- `github_username`
- `admin_ui` (`default` or `django-unfold`)
