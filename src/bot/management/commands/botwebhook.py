import asyncio

from django.core.management import BaseCommand, CommandError

from bot.config import get_bot_settings
from bot.main import remove_webhook, setup_webhook, shutdown


class Command(BaseCommand):
    help = "Manage bot webhook: set or delete"

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=["set", "delete"],
            help="Webhook action",
        )
        parser.add_argument(
            "--drop-pending-updates",
            action="store_true",
            default=False,
            help="Drop pending updates when setting/deleting webhook",
        )

    def handle(self, *args, **options):
        settings = get_bot_settings()
        if not settings.token:
            raise CommandError("BOT_TOKEN is required")

        action = options["action"]
        drop_pending = options["drop_pending_updates"]

        if action == "set":
            if not settings.webhook_base_url:
                raise CommandError("BOT_WEBHOOK_BASE_URL is required")
            asyncio.run(setup_webhook(drop_pending_updates=drop_pending))
            asyncio.run(shutdown())
            self.stdout.write(self.style.SUCCESS(f"Webhook configured at {settings.webhook_url}"))
            return

        asyncio.run(remove_webhook(drop_pending_updates=drop_pending))
        asyncio.run(shutdown())
        self.stdout.write(self.style.SUCCESS("Webhook deleted"))
