from rest_framework.response import Response


class CustomAPIExceptionHandler:
    """
    Custom exception handler for DRF that formats error responses in a consistent way.
    It extracts error messages from the default DRF response and constructs a new response with:
        - success: False
        - message: A concatenated string of all error messages
        - error: An error code derived from the exception (if available)
    """

    def __call__(self, exc, context):
        return self.handle(exc, context)

    def handle(self, exc: Exception, context: dict | list) -> Response | None:

        # Use DRF's default exception handler to get the standard error response
        from rest_framework.views import exception_handler

        response = exception_handler(exc, context)

        if response is None:
            return response

        # Extract and format error messages from the response data
        error_messages = []

        if isinstance(response.data, dict):
            error_messages.extend(self._get_dict_errors(response))

        elif isinstance(response.data, list):
            error_messages.extend(self._get_list_errors(response))

        final_message = "; ".join(error_messages).strip()

        response.data = {
            "success": False,
            "message": final_message or "An unexpected error occurred.",
            "error": self._get_error_code(exc),
        }

        return response

    def _get_dict_errors(self, response: Response) -> list[str]:
        error_messages = []

        for field, messages in response.data.items():
            if isinstance(messages, list):
                # Simple field errors
                joined = ", ".join(str(msg) for msg in messages)
                error_messages.append(f"{field}: {joined}")
            elif isinstance(messages, dict):
                # Nested serializer errors
                for sub_field, sub_messages in messages.items():
                    joined = ", ".join(str(msg) for msg in sub_messages)
                    error_messages.append(f"{field}.{sub_field}: {joined}")
            else:
                # General (non-field) errors, e.g. 'detail'
                error_messages.append(str(error_messages))

        return error_messages

    def _get_list_errors(self, response: Response) -> list[str]:
        error_messages = []

        # Non-field errors as a list
        for message in response.data:
            error_messages.append(str(message))

        return error_messages

    def _get_error_code(self, exc: Exception) -> str:
        return getattr(exc, "code", getattr(exc, "default_code", "error"))
