#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def parse_context(values: list[str]) -> dict[str, str]:
    context: dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise ValueError(f"Invalid --context value '{item}'. Expected key=value.")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid --context value '{item}'. Key cannot be empty.")
        context[key] = value
    return context


def prepare_target_directory(target_dir: Path, force: bool) -> None:
    if target_dir.exists() and not target_dir.is_dir():
        raise RuntimeError(f"Target path exists and is not a directory: {target_dir}")

    target_dir.mkdir(parents=True, exist_ok=True)

    if any(target_dir.iterdir()) and not force:
        raise RuntimeError(
            f"Target directory is not empty: {target_dir}. "
            "Use --force to merge/overwrite existing files."
        )


def copy_entry(source: Path, destination: Path) -> None:
    if source.is_dir():
        if destination.exists() and destination.is_file():
            destination.unlink()
        shutil.copytree(source, destination, dirs_exist_ok=True)
        return

    if destination.exists() and destination.is_dir():
        shutil.rmtree(destination)
    shutil.copy2(source, destination)


def flatten_generated_project(source_root: Path, target_root: Path) -> None:
    for entry in source_root.iterdir():
        copy_entry(entry, target_root / entry.name)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a project from this cookiecutter template directly into "
            "the target directory root (no nested project_slug folder)."
        )
    )
    parser.add_argument(
        "target_dir", help="Directory where generated project files will be placed"
    )
    parser.add_argument(
        "--template",
        default=str(Path(__file__).resolve().parent),
        help="Path to cookiecutter template repository (default: this repository)",
    )
    parser.add_argument(
        "--no-input",
        action="store_true",
        help="Run non-interactively using defaults plus any --context overrides",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow generating into a non-empty target directory (merge/overwrite)",
    )
    parser.add_argument(
        "--context",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Extra cookiecutter context value (can be passed multiple times)",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    template_path = Path(args.template).expanduser().resolve()
    target_dir = Path(args.target_dir).expanduser().resolve()

    if not template_path.exists():
        print(f"Error: template path does not exist: {template_path}", file=sys.stderr)
        return 2

    try:
        extra_context = parse_context(args.context)
        prepare_target_directory(target_dir, force=args.force)
    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    try:
        import importlib

        cookiecutter_module = importlib.import_module("cookiecutter.main")
        cookiecutter_fn = getattr(cookiecutter_module, "cookiecutter")
    except Exception:  # noqa: BLE001
        print(
            "Error: cookiecutter is not installed. Install it with: pip install cookiecutter",
            file=sys.stderr,
        )
        return 2

    with TemporaryDirectory(prefix="cookiecutter-render-") as temp_dir:
        try:
            generated_project = cookiecutter_fn(
                str(template_path),
                no_input=args.no_input,
                output_dir=temp_dir,
                extra_context=extra_context or None,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"Error: cookiecutter generation failed: {exc}", file=sys.stderr)
            return 1

        flatten_generated_project(Path(generated_project), target_dir)

    print(f"Project generated at: {target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
