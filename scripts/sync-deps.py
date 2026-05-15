import tomllib
import re
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
TEMPLATE_TOML = ROOT_DIR / "{{cookiecutter.project_slug}}/pyproject.toml"
ROOT_TOML = ROOT_DIR / "pyproject.toml"

def main():
    with open(TEMPLATE_TOML, "rb") as f:
        template_data = tomllib.load(f)
    
    deps = template_data.get("project", {}).get("dependencies", [])
    dev_deps = template_data.get("dependency-groups", {}).get("dev", [])
    
    all_deps = deps + dev_deps
    
    with open(ROOT_TOML, "r") as f:
        root_content = f.read()
        
    template_group_str = "[dependency-groups]\ndev = [\n"
    for dep in all_deps:
        template_group_str += f'    "{dep}",\n'
    template_group_str += "]\n"
    
    if "[dependency-groups]" in root_content:
        root_content = re.sub(r'\[dependency-groups].*', template_group_str, root_content, flags=re.DOTALL)
    else:
        root_content = root_content.rstrip() + "\n\n" + template_group_str
        
    with open(ROOT_TOML, "w") as f:
        f.write(root_content)
        
    print("Dependencies synced. Running uv sync...")
    subprocess.run(["uv", "sync"], check=True)

if __name__ == "__main__":
    main()