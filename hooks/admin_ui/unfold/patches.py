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
        '    "django-filter>=25.1",\n',
        '    "django-unfold>=0.63.0",\n',
        marker='    "django-unfold>=0.63.0",',
    )

    patcher.ensure_insert_after(
        "uv.lock",
        '    { name = "django-filter" },\n',
        '    { name = "django-unfold" },\n',
        marker='    { name = "django-unfold" },',
    )

    patcher.ensure_insert_after(
        "uv.lock",
        '    { name = "django-filter", specifier = ">=25.1" },\n',
        '    { name = "django-unfold", specifier = ">=0.63.0" },\n',
        marker='    { name = "django-unfold", specifier = ">=0.63.0" },',
    )


def apply_admin_import(patcher: FilePatcher) -> None:
    patcher.ensure_replace(
        "src/core/admin.py",
        "from django.contrib.admin import ModelAdmin\n",
        "from unfold.admin import ModelAdmin\n",
        marker="from unfold.admin import ModelAdmin",
    )


def apply_settings(patcher: FilePatcher) -> None:
    unfold_apps = read_snippet("unfold_apps.txt")
    unfold_settings = read_snippet("unfold_settings.txt")

    patcher.ensure_replace(
        "src/config/settings/base.py",
        "UNFOLD_APPS = []\n",
        f"{unfold_apps}\n",
        marker="unfold.contrib.filters",
    )

    patcher.ensure_insert_before(
        "src/config/settings/base.py",
        'CORS_URLS_REGEX = r"^/api/.*$"\n',
        f"{unfold_settings}\n\n",
        marker="UNFOLD = {",
    )


def apply_uv_lock_package(patcher: FilePatcher) -> None:
    uv_lock_block = read_snippet("uv_lock_unfold_package.toml")

    patcher.ensure_insert_before(
        "uv.lock",
        '[[package]]\nname = "djangorestframework"\n',
        f"{uv_lock_block}\n\n",
        marker='[[package]]\nname = "django-unfold"\nversion = "0.78.1"\n',
    )


def get_patches() -> list[PatchSpec]:
    return [
        PatchSpec(
            patch_id="admin_ui.unfold.dependencies",
            apply=apply_dependencies,
            priority=10,
        ),
        PatchSpec(
            patch_id="admin_ui.unfold.admin_import",
            apply=apply_admin_import,
            priority=20,
        ),
        PatchSpec(
            patch_id="admin_ui.unfold.settings",
            apply=apply_settings,
            priority=30,
        ),
        PatchSpec(
            patch_id="admin_ui.unfold.uv_lock_package",
            apply=apply_uv_lock_package,
            priority=40,
            after=("admin_ui.unfold.dependencies",),
        ),
    ]
