from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

sys.dont_write_bytecode = True

if TYPE_CHECKING:
    from patching.engine import PatchSpec

ADMIN_UI = "{{ cookiecutter.admin_ui }}"
API_FRAMEWORK = "{{ cookiecutter.api_framework }}"
BACKGROUND_TASK = "{{ cookiecutter.background_task }}"
DOCKER_NAME_PREFIX = "{{ cookiecutter.docker_name_prefix }}"
OPEN_SOURCE_LICENSE = "{{ cookiecutter.open_source_license }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
REPO_DIR = "{{ cookiecutter._repo_dir }}"
TEMPLATE_REF = "{{ cookiecutter._template }}"


def remove_license_if_none() -> None:
    if OPEN_SOURCE_LICENSE == "None":
        Path("LICENSE").unlink(missing_ok=True)


def resolve_repo_dir() -> Path:
    repo_path = Path(REPO_DIR)
    template_path = Path(TEMPLATE_REF)
    env_pwd = os.environ.get("PWD")

    candidates: list[Path] = []
    if repo_path.is_absolute():
        candidates.append(repo_path)
    if template_path.is_absolute():
        candidates.append(template_path)

    if env_pwd:
        pwd_path = Path(env_pwd).resolve()
        candidates.append(pwd_path / repo_path)
        candidates.append(pwd_path / template_path)

    candidates.append((Path.cwd() / repo_path).resolve())
    candidates.append((Path.cwd() / template_path).resolve())

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    return candidates[0]


def bootstrap_hooks_imports() -> None:
    hooks_module_root = resolve_repo_dir() / "hooks"
    if not hooks_module_root.exists():
        raise RuntimeError(f"Cannot locate hooks module root: {hooks_module_root}")

    hooks_path = str(hooks_module_root)
    if hooks_path not in sys.path:
        sys.path.insert(0, hooks_path)


def collect_patches() -> list[PatchSpec]:
    patches: list[PatchSpec] = []

    if ADMIN_UI == "django-unfold" or BACKGROUND_TASK != "none" or API_FRAMEWORK == "django-modern-rest":
        bootstrap_hooks_imports()

    if API_FRAMEWORK == "django-modern-rest":
        from api_framework.django_modern_rest import get_patches as get_dmr_patches

        patches.extend(get_dmr_patches())

    if ADMIN_UI == "django-unfold":
        from admin_ui.unfold import get_patches as get_unfold_patches

        patches.extend(get_unfold_patches())

    if BACKGROUND_TASK == "celery":
        from background_task.celery import get_patches as get_celery_patches

        patches.extend(get_celery_patches(docker_prefix=DOCKER_NAME_PREFIX, project_slug=PROJECT_SLUG))

    if BACKGROUND_TASK == "django-q2":
        from background_task.django_q2 import get_patches as get_q2_patches

        patches.extend(get_q2_patches(docker_prefix=DOCKER_NAME_PREFIX, project_slug=PROJECT_SLUG))

    return patches


def main() -> int:
    remove_license_if_none()

    patches = collect_patches()
    if not patches:
        return 0

    from patching.engine import PatchEngine

    engine = PatchEngine(Path.cwd())
    applied = engine.run(patches)
    print(f"Applied hook patches: {', '.join(applied)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
