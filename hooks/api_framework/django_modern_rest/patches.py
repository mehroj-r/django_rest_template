from __future__ import annotations

from pathlib import Path

from patching.engine import PatchSpec
from patching.ops import FilePatcher


def read_snippet(filename: str) -> str:
    snippets_dir = Path(__file__).resolve().parent / "snippets"
    return (snippets_dir / filename).read_text(encoding="utf-8").rstrip("\n") + "\n"


def replace_file(patcher: FilePatcher, relative_path: str, snippet_file: str) -> None:
    patcher.write_text(relative_path, read_snippet(snippet_file))


def apply_dependencies(patcher: FilePatcher) -> None:
    patcher.ensure_remove(
        "pyproject.toml",
        '    "djangorestframework>=3.16.0",\n',
    )
    patcher.ensure_remove(
        "pyproject.toml",
        '    "djangorestframework-simplejwt[crypto]>=5.5.1",\n',
    )
    patcher.ensure_remove(
        "pyproject.toml",
        '    "markdown>=3.8.2",\n',
    )
    patcher.ensure_insert_after(
        "pyproject.toml",
        '    "whitenoise>=6.11.0",\n',
        '    "django-modern-rest[msgspec,jwt,openapi]>=0.8.0",\n',
        marker='    "django-modern-rest[msgspec,jwt,openapi]>=0.8.0",',
    )


def apply_settings(patcher: FilePatcher) -> None:
    patcher.ensure_insert_after(
        "src/config/settings/base.py",
        "from decouple import config\n",
        "from dmr.parsers import JsonParser\nfrom dmr.renderers import JsonRenderer\n",
        marker="from dmr.renderers import JsonRenderer",
    )
    patcher.ensure_replace(
        "src/config/settings/base.py",
        '    "rest_framework",\n    "rest_framework_simplejwt",\n',
        '    "dmr",\n',
        marker='    "dmr",',
    )
    patcher.ensure_replace(
        "src/config/settings/base.py",
        "REST_FRAMEWORK = {\n"
        '    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],\n'
        '    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],\n'
        '    "DEFAULT_PAGINATION_CLASS": "core.utils.pagination.CustomPagination",\n'
        '    "PAGE_SIZE": 10,\n'
        '    "EXCEPTION_HANDLER": "core.api.exceptions.CustomAPIExceptionHandler.handle",  # noqa\n'
        "}\n",
        "DMR_SETTINGS = {\n"
        '    "parsers": [JsonParser()],\n'
        '    "renderers": [JsonRenderer()],\n'
        '    "validate_responses": True,\n'
        '    "semantic_responses": True,\n'
        '    "global_error_handler": "core.api.exceptions.global_error_handler",\n'
        "}\n",
        marker="DMR_SETTINGS = {",
    )


def apply_dev_urls(patcher: FilePatcher) -> None:
    patcher.ensure_remove(
        "src/config/urls/dev.py",
        '        path("api-auth/", include("rest_framework.urls")),\n',
        on_missing="skip",
    )


def apply_full_file_replacements(patcher: FilePatcher) -> None:
    replace_file(patcher, "src/core/api/views.py", "core_api_views.py")
    replace_file(patcher, "src/core/api/exceptions.py", "core_api_exceptions.py")
    replace_file(patcher, "src/core/utils/pagination.py", "core_utils_pagination.py")
    replace_file(patcher, "src/api/v1/core/views/auth.py", "auth_views.py")
    replace_file(patcher, "src/api/v1/core/views/misc.py", "misc_views.py")


def apply_docs(patcher: FilePatcher) -> None:
    patcher.ensure_replace(
        "README.md",
        "- **JWT Authentication**: Secure endpoints using `rest_framework_simplejwt`.\n",
        "- **JWT Authentication**: Secure endpoints using `django-modern-rest` JWT controllers.\n",
    )
    patcher.ensure_replace(
        "README.md",
        "- Uses JWT (JSON Web Token) via `rest_framework_simplejwt`.\n",
        "- Uses JWT (JSON Web Token) via `django-modern-rest`.\n",
    )


def get_patches() -> list[PatchSpec]:
    return [
        PatchSpec(
            patch_id="api_framework.django_modern_rest.dependencies",
            apply=apply_dependencies,
            priority=10,
        ),
        PatchSpec(
            patch_id="api_framework.django_modern_rest.settings",
            apply=apply_settings,
            priority=20,
        ),
        PatchSpec(
            patch_id="api_framework.django_modern_rest.dev_urls",
            apply=apply_dev_urls,
            priority=30,
        ),
        PatchSpec(
            patch_id="api_framework.django_modern_rest.full_files",
            apply=apply_full_file_replacements,
            priority=40,
        ),
        PatchSpec(
            patch_id="api_framework.django_modern_rest.docs",
            apply=apply_docs,
            priority=50,
        ),
    ]
