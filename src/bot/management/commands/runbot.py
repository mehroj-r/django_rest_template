import asyncio

from django.core.management import BaseCommand, CommandError

from bot.config import get_bot_settings
from bot.main import shutdown, start_polling


class Command(BaseCommand):
    help = "Run Telegram bot in long-polling mode"

    def handle(self, *args, **options):
        settings = get_bot_settings()
        if not settings.token:
            raise CommandError("BOT_TOKEN is required")
        if settings.mode != "polling":
            self.stdout.write(
                self.style.WARNING(
                    f"BOT_MODE is '{settings.mode}'. runbot will still start polling explicitly."
                )
            )

        self.stdout.write(self.style.SUCCESS("Starting bot polling..."))
        try:
            asyncio.run(start_polling())
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Bot polling stopped by user"))
        finally:
            asyncio.run(shutdown())
