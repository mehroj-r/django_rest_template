import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Manage bot i18n workflow: extract, init, update, compile"
    domain = "bot"

    @property
    def project_root(self) -> Path:
        return settings.BASE_DIR.parent

    @property
    def locales_dir(self) -> Path:
        return settings.BASE_DIR / "bot" / "etc" / "locales"

    @property
    def pot_file(self) -> Path:
        return self.locales_dir / f"{self.domain}.pot"

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=["extract", "init", "update", "compile"],
            help="i18n action",
        )
        parser.add_argument("--locale", help="Locale code, required for init")

    def run_command(self, command: list[str]) -> None:
        try:
            subprocess.run(command, cwd=self.project_root, check=True)
        except FileNotFoundError as exc:
            raise CommandError(
                "pybabel is not installed. Run `uv sync` first."
            ) from exc
        except subprocess.CalledProcessError as exc:
            raise CommandError(f"Command failed: {' '.join(command)}") from exc

    def handle(self, *args, **options):
        action = options["action"]
        locale = options.get("locale")

        self.locales_dir.mkdir(parents=True, exist_ok=True)

        if action == "extract":
            self.run_command(
                [
                    "pybabel",
                    "extract",
                    "-F",
                    "babel.cfg",
                    "-o",
                    str(self.pot_file),
                    "src",
                ]
            )
            self.stdout.write(
                self.style.SUCCESS(f"Extracted messages to {self.pot_file}")
            )
            return

        if action == "init":
            if not locale:
                raise CommandError("--locale is required when action is 'init'")
            self.run_command(
                [
                    "pybabel",
                    "init",
                    "-i",
                    str(self.pot_file),
                    "-d",
                    str(self.locales_dir),
                    "-D",
                    self.domain,
                    "-l",
                    locale,
                ]
            )
            self.stdout.write(self.style.SUCCESS(f"Initialized locale: {locale}"))
            return

        if action == "update":
            self.run_command(
                [
                    "pybabel",
                    "update",
                    "-i",
                    str(self.pot_file),
                    "-d",
                    str(self.locales_dir),
                    "-D",
                    self.domain,
                ]
            )
            self.stdout.write(self.style.SUCCESS("Updated bot locale files"))
            return

        self.run_command(
            [
                "pybabel",
                "compile",
                "-d",
                str(self.locales_dir),
                "-D",
                self.domain,
            ]
        )
        self.stdout.write(self.style.SUCCESS("Compiled bot locales"))
