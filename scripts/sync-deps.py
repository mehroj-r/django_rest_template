import subprocess
import tomllib
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
TEMPLATE_TOML = ROOT_DIR / "{{cookiecutter.project_slug}}/pyproject.toml"


def main():
    if not TEMPLATE_TOML.exists():
        print(f"Error: Template pyproject.toml not found at {TEMPLATE_TOML}")
        return

    with open(TEMPLATE_TOML, "rb") as f:
        template_data = tomllib.load(f)

    deps = template_data.get("project", {}).get("dependencies", [])
    dev_deps = template_data.get("dependency-groups", {}).get("dev", [])

    all_deps = deps + dev_deps

    if not all_deps:
        print("No dependencies found in template pyproject.toml.")
        return

    print("Installing template dependencies directly for IDE support...")
    try:
        subprocess.run(["uv", "pip", "install"] + all_deps, check=True)
        print("Successfully installed template dependencies.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")


if __name__ == "__main__":
    main()
