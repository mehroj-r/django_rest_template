from rest_framework.response import Response


class CustomAPIExceptionHandler:
    """
    Custom exception handler for DRF that formats error responses in a consistent way.
    It extracts error messages from the default DRF response and constructs a new response with:
        - success: False
        - message: A concatenated string of all error messages
        - error: An error code derived from the exception (if available)
    """

    @classmethod
    def handle(cls, exc: Exception, context: dict | list) -> Response | None:
        from rest_framework.views import exception_handler

        response = exception_handler(exc, context)
        if response is None:
            return response

        error_messages = []
        if isinstance(response.data, dict):
            error_messages.extend(cls._get_dict_errors(response))
        elif isinstance(response.data, list):
            error_messages.extend(cls._get_list_errors(response))

        final_message = "; ".join(error_messages).strip()
        response.data = {
            "success": False,
            "message": final_message or "An unexpected error occurred.",
            "error": cls._get_error_code(exc),
        }
        return response

    @staticmethod
    def _get_dict_errors(response: Response) -> list[str]:
        error_messages = []
        for field, messages in response.data.items():
            if isinstance(messages, list):
                joined = ", ".join(str(msg) for msg in messages)
                error_messages.append(f"{field}: {joined}")
            elif isinstance(messages, dict):
                for sub_field, sub_messages in messages.items():
                    joined = ", ".join(str(msg) for msg in sub_messages)
                    error_messages.append(f"{field}.{sub_field}: {joined}")
            else:
                error_messages.append(str(messages))
        return error_messages

    @staticmethod
    def _get_list_errors(response: Response) -> list[str]:
        return [str(message) for message in response.data]

    @staticmethod
    def _get_error_code(exc: Exception) -> str:
        return getattr(exc, "code", getattr(exc, "default_code", "error"))
