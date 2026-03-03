from abc import ABC, abstractmethod


class AbstractMiddleware(ABC):
    """
    Abstract Django middleware class that replicates the legacy
    process_* hook behavior without using MiddlewareMixin.

    You can subclass this to implement only the hooks you need.
    """

    def __init__(self, get_response):
        """
        Called once when the server starts.

        `get_response` is the next middleware or the Django view.
        """
        self.get_response = get_response
        super().__init__()

    # -----------------------------
    # HOOK METHODS TO OVERRIDE
    # -----------------------------

    def process_request(self, request):
        """
        Runs BEFORE Django selects a view.
        - Authentication / blocking / pre-validation
        - Setting request attributes
        Return:
            - None → continue processing
            - HttpResponse → short-circuit and return immediately
        """
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Runs RIGHT BEFORE the view is executed.
        Good for:
        - Inspecting/modifying view arguments
        - Cancelling execution by returning a response
        """
        return None

    def process_exception(self, request, exception):
        """
        Runs ONLY if the view raises an exception.
        Good for:
        - Logging
        - Returning a custom error response
        """
        return None

    def process_template_response(self, request, response):
        """
        Runs ONLY for TemplateResponse objects.
        Good for:
        - Modifying template context before rendering
        """
        return response

    def process_response(self, request, response):
        """
        Runs for ALL responses.
        Good for:
        - Adding headers
        - Adjusting cookies
        - Modifying response body
        """
        return response

    # --------------------------------------
    # CORE DJANGO MIDDLEWARE EXECUTION FLOW
    # --------------------------------------

    def __call__(self, request):
        """
        The core entry point for the middleware.
        Manually triggers process_* hooks in the correct order.
        """

        # 1. process_request
        result = self.process_request(request)
        if result:
            return self.process_response(request, result)

        # 2. process_view — but Django normally calls this *before* the view,
        #    not here. We emulate it inside a wrapper.
        response = None

        def wrapped_view(*view_args, **view_kwargs):
            nonlocal response
            result = self.process_view(request, view, view_args, view_kwargs)
            if result:
                response = result
                return result
            return view(*view_args, **view_kwargs)

        # Trick: replace the view temporarily
        view = self.get_response

        try:
            # Execute the view
            if response is None:
                response = wrapped_view(request)
        except Exception as exc:
            # 3. process_exception
            exception_result = self.process_exception(request, exc)
            if exception_result:
                response = exception_result
            else:
                raise  # no handler → Django handles it

        # 4. process_template_response
        if hasattr(response, "render"):
            response = self.process_template_response(request, response)

        # 5. process_response
        return self.process_response(request, response)
