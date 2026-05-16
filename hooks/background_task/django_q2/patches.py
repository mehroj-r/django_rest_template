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
        '    "django-q2>=1.7.5",\n    "redis>=5.2.1",\n',
        marker='    "django-q2>=1.7.5",',
    )


def apply_settings(patcher: FilePatcher, project_slug: str) -> None:
    q2_settings = read_snippet("q2_settings.txt").replace("{{ cookiecutter.project_slug }}", project_slug)

    patcher.ensure_insert_after(
        "src/config/settings/base.py",
        '    "django_softdelete",\n',
        '    "django_q",\n',
        marker='    "django_q",',
    )

    patcher.ensure_insert_before(
        "src/config/settings/base.py",
        'CORS_URLS_REGEX = r"^/api/.*$"\n',
        f"{q2_settings}\n\n",
        marker="Q_CLUSTER",
    )


def apply_docker(patcher: FilePatcher, docker_prefix: str) -> None:
    q2_docker = read_snippet("q2_docker.txt").replace("{{ cookiecutter.docker_name_prefix }}", docker_prefix)
    q2_docker_prod = read_snippet("q2_docker_prod.txt").replace("{{ cookiecutter.docker_name_prefix }}", docker_prefix)

    patcher.ensure_insert_before(
        "docker-compose.yml",
        "  web:\n",
        f"{q2_docker}\n",
        marker=f'    container_name: "{docker_prefix}-redis-dev"',
    )

    patcher.ensure_insert_before(
        "docker-compose.prod.yml",
        "  web:\n",
        f"{q2_docker_prod}\n",
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


def apply_docs(patcher: FilePatcher) -> None:
    q2_docs = read_snippet("q2_docs.txt")
    patcher.create_file("docs/django_q2.md", q2_docs)


def get_patches(docker_prefix: str, project_slug: str) -> list[PatchSpec]:
    return [
        PatchSpec(
            patch_id="background_task.django_q2.dependencies",
            apply=apply_dependencies,
            priority=10,
        ),
        PatchSpec(
            patch_id="background_task.django_q2.settings",
            apply=lambda p: apply_settings(p, project_slug),
            priority=20,
        ),
        PatchSpec(
            patch_id="background_task.django_q2.docker",
            apply=lambda p: apply_docker(p, docker_prefix),
            priority=30,
        ),
        PatchSpec(
            patch_id="background_task.django_q2.docs",
            apply=apply_docs,
            priority=40,
        ),
    ]
