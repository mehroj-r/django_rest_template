import os
from django.conf import settings
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create versioned API app with project structure"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str, help="Name of the new app")
        parser.add_argument("--ver", type=str, default="v1", help="API version folder to generate (default: v1)")

    def handle(self, *args, **options):
        app_name = options["app_name"]
        version = options["ver"]

        # -----------------------------------------------------
        # 1. Create API structure
        # -----------------------------------------------------
        api_root = os.path.join(settings.BASE_DIR, "api", version, app_name)
        api_files = {
            "serializers.py": "",
            "views.py": "",
            "urls.py": f"from django.urls import path\n\n" f'app_name = "{app_name}"\n\n' f"urlpatterns = []\n",
            "__init__.py": "",
        }

        self.create_files(api_root, api_files)
        self.stdout.write(self.style.SUCCESS(f"Created API module: {api_root}"))

        # -----------------------------------------------------
        # 2. Create App structure
        # -----------------------------------------------------
        app_root = os.path.join(settings.BASE_DIR, "apps", app_name)
        app_files = {
            "__init__.py": "",
            "models.py": "",
            "apps.py": (
                f"from django.apps import AppConfig\n\n\n"
                f"class {app_name.capitalize()}Config(AppConfig):\n"
                f'    default_auto_field = "django.db.models.BigAutoField"\n'
                f'    name = "{app_name}"\n'
            ),
            "admin/__init__.py": "",
            "admin/admins.py": "",
            "migrations/__init__.py": "",
        }

        self.create_files(app_root, app_files)
        self.stdout.write(self.style.SUCCESS(f"Created Django app: {app_root}"))

        # -----------------------------------------------------
        # 3. Add to LOCAL_APPS
        # -----------------------------------------------------
        settings_file = self.get_settings_file()
        self.add_to_local_apps(settings_file, app_name)

        self.stdout.write(self.style.SUCCESS("App generation complete!"))

    # ---------------------------------------------------------
    # Utility Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _write_file(path, content=""):
        """Write file and ensure folders exist."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)

    def create_files(self, base_path, files: dict):
        """Create multiple files under a base directory."""
        for relative_path, content in files.items():
            full_path = os.path.join(base_path, relative_path)
            self._write_file(full_path, content)

    @staticmethod
    def get_settings_file():
        """Resolve correct settings/base.py path."""
        settings_path = settings.SETTINGS_MODULE.replace(".", "/")

        # Remove environment suffixes (dev.py, prod.py)
        for suffix in ["dev", "prod", "base"]:
            if settings_path.endswith(suffix):
                settings_path = settings_path[: -len(suffix)]

        return os.path.join(settings.BASE_DIR, f"{settings_path}base.py")

    def add_to_local_apps(self, settings_file, app_name):
        """Append the app to LOCAL_APPS before its closing bracket."""
        try:
            with open(settings_file, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise CommandError(f"Settings file not found: {settings_file}")

        start, end = None, None

        # Locate LOCAL_APPS = [
        for i, line in enumerate(lines):
            if "LOCAL_APPS" in line and "[" in line:
                start = i
                break

        if start is None:
            raise CommandError("LOCAL_APPS not found inside settings.py")

        # Find closing bracket ]
        for i in range(start + 1, len(lines)):
            if "]" in lines[i]:
                end = i
                break

        if end is None:
            raise CommandError("LOCAL_APPS closing bracket not found")

        # Already exists?
        existing = any(f'"{app_name}"' in line for line in lines[start:end])
        if existing:
            self.stdout.write(self.style.WARNING(f"{app_name} already in LOCAL_APPS"))
            return

        # Insert before closing ]
        lines.insert(end, f'    "{app_name}",\n')

        # Write back
        with open(settings_file, "w") as f:
            f.writelines(lines)

        self.stdout.write(self.style.SUCCESS(f"Added {app_name} to LOCAL_APPS"))
