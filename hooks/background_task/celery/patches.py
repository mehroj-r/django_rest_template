from __future__ import annotations

from patching.engine import PatchSpec
from patching.ops import FilePatcher


def read_snippet(filename: str) -> str:
    from pathlib import Path

    SNIPPETS_DIR = Path(__file__).resolve().parent / "snippets"
    return (SNIPPETS_DIR / filename).read_text(encoding="utf-8").rstrip("\n")


def apply_dependencies(patcher: FilePatcher) -> None:
    patcher.ensure_insert_after(
        "pyproject.toml",
        '    "uvicorn>=0.37.0",\n',
        '    "celery>=5.4.0",\n    "redis>=5.2.1",\n',
        marker='    "celery>=5.4.0",',
    )


def apply_settings(patcher: FilePatcher) -> None:
    celery_settings = read_snippet("celery_settings.txt")

    patcher.ensure_insert_before(
        "src/config/settings/base.py",
        'CORS_URLS_REGEX = r"^/api/.*$"\n',
        f"{celery_settings}\n\n",
        marker="CELERY_BROKER_URL",
    )


def apply_docker(patcher: FilePatcher, docker_prefix: str) -> None:
    celery_docker = read_snippet("celery_docker.txt").replace("{{ cookiecutter.docker_name_prefix }}", docker_prefix)
    celery_docker_prod = read_snippet("celery_docker_prod.txt").replace(
        "{{ cookiecutter.docker_name_prefix }}", docker_prefix
    )

    patcher.ensure_insert_before(
        "docker-compose.yml",
        "  web:\n",
        f"{celery_docker}\n",
        marker=f'    container_name: "{docker_prefix}-redis-dev"',
    )

    patcher.ensure_insert_before(
        "docker-compose.prod.yml",
        "  web:\n",
        f"{celery_docker_prod}\n",
        marker=f'    container_name: "{docker_prefix}-redis-prod"',
    )

    patcher.ensure_insert_after(
        "docker-compose.yml",
        "  app_data:\n",
        "  redis_data:\n",
        marker="  redis_data:",
    )

    patcher.ensure_insert_after(
        "docker-compose.prod.yml",
        "  app_data:\n",
        "  redis_data:\n",
        marker="  redis_data:",
    )


def apply_files(patcher: FilePatcher, project_slug: str) -> None:
    celery_app = read_snippet("celery_app.txt").replace("{{ cookiecutter.project_slug }}", project_slug)
    celery_init = read_snippet("celery_init.txt")

    patcher.create_file("src/core/celery.py", celery_app)
    patcher.ensure_contains("src/core/__init__.py", celery_init)


def apply_docs(patcher: FilePatcher) -> None:
    celery_docs = read_snippet("celery_docs.txt")
    patcher.create_file("docs/celery.md", celery_docs)


def get_patches(docker_prefix: str, project_slug: str) -> list[PatchSpec]:
    return [
        PatchSpec(
            patch_id="background_task.celery.dependencies",
            apply=apply_dependencies,
            priority=10,
        ),
        PatchSpec(
            patch_id="background_task.celery.settings",
            apply=apply_settings,
            priority=20,
        ),
        PatchSpec(
            patch_id="background_task.celery.docker",
            apply=lambda p: apply_docker(p, docker_prefix),
            priority=30,
        ),
        PatchSpec(
            patch_id="background_task.celery.files",
            apply=lambda p: apply_files(p, project_slug),
            priority=40,
        ),
        PatchSpec(
            patch_id="background_task.celery.docs",
            apply=apply_docs,
            priority=50,
        ),
    ]
