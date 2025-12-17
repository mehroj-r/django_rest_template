import logging
import queue
import threading
import traceback
import requests

class TelegramErrorHandler(logging.Handler):
    """
    A logging handler that sends error logs to a Telegram chat via a bot.
    It uses a background thread and a queue to avoid blocking the main thread.
    """

    def __init__(self, bot_token, chat_id, level=logging.ERROR, max_queue=100):
        super().__init__(level)
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        self.chat_id = chat_id
        self.queue = queue.Queue(maxsize=max_queue)

        self.worker = threading.Thread(target=self._worker, daemon=True)
        self.worker.start()

    def emit(self, record):
        try:
            # Prevent automatic traceback formatting (already in record.traceback via filter)
            original_exc_info = record.exc_info
            record.exc_info = None
            record.exc_text = None

            msg = self.format(record)

            # Restore original exc_info for other handlers
            record.exc_info = original_exc_info

            self.queue.put_nowait(msg)
        except queue.Full:
            pass  # drop or count dropped messages

    def _worker(self):
        session = requests.Session()
        while True:
            msg = self.queue.get()
            try:
                session.post(
                    self.api_url,
                    json={
                        "chat_id": self.chat_id,
                        "text": msg[:4000],
                        "parse_mode": "Markdown",
                    },
                    timeout=5,
                )
            except Exception:
                pass
            finally:
                self.queue.task_done()



class RequestContextFilter(logging.Filter):
    """
    Adds request/user/IP/path/method + traceback info to log records.
    """

    def filter(self, record):
        request = getattr(record, "request", None)

        if request:
            record.user = getattr(request.user, "username", "Anonymous")
            record.method = request.method
            record.path = request.path
            record.ip = request.META.get("REMOTE_ADDR", "-")
        else:
            record.user = "Unknown"
            record.method = "-"
            record.path = "-"
            record.ip = "-"

        if record.exc_info:
            exc_type, exc_value, exc_tb = record.exc_info
            record.traceback = "".join(
                traceback.format_exception(exc_type, exc_value, exc_tb)
            )
        else:
            record.traceback = "No traceback"

        return True
