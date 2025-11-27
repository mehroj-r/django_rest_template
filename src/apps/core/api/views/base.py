from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.utils.translation import gettext_lazy as _
from logging import getLogger

from core.utils.pagination import CustomPagination

logger = getLogger(__name__)


class PaginatedListMixin:

    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())  # noqa
        if qs:
            result = self.paginated_queryset(qs, request)  # noqa
            serializer = self.get_serializer(result, many=True)  # noqa
            response = self.paginated_response(data=serializer.data)  # noqa
            return Response(response)
        return Response({"success": True, "message": "OK", "results": []})


class CustomResponseMixin:
    """
    Mixin to customize API responses with a standard structure.
    It provides methods to format successful and error responses.
    The response structure is as follows:
    - For success:
        {
            "success": true,
            "message": <SUCCESS_MESSAGE>,
            "data": <response_data>
        }
    - For error:
        {
            "success": false,
            "message": <ERROR_MESSAGE>",
            "error": <error_data>
        }
    CAUTION: This mixin is only functional for the exceptions handled by DRF.
             It does not handle exceptions raised outside the DRF scope.
             For the rest, you should use a custom exception handler.
    """

    SUCCESS_MESSAGE = "OK"
    ERROR_MESSAGE = "NOT OK"

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)  # noqa

        if self._is_structured_response(response):
            return response

        if response.status_code < 400:
            response = self._success_response(response=response)
        else:
            response = self._error_response(response=response)

        return response

    def _success_response(self, response: Response):
        response_data = {
            "success": True,
            "message": self.SUCCESS_MESSAGE,
            "data": response.data,
        }
        response.data = response_data
        return response

    def _error_response(self, response: Response):
        response_data = {
            "success": False,
            "message": self.ERROR_MESSAGE,
            "error": response.data,
        }
        response.data = response_data
        return response

    @staticmethod
    def _is_structured_response(response: Response) -> bool:
        is_already_structured: bool = (
            isinstance(response.data, dict) and "success" in response.data and "message" in response.data
        )
        return is_already_structured


class BaseAPIView(CustomResponseMixin, generics.GenericAPIView):
    ...

    def _parse_error_message(self, errors):
        message = None
        _errors = {}
        logger.error(errors)
        try:
            items = errors.items()
        except AttributeError:
            if isinstance(errors, list):
                return {"errors": {"detail": errors}, "message": message}
            return {"errors": errors, "message": message}
        for key, error in items:
            _error = []
            if isinstance(error, str):
                _error = [error]
            elif isinstance(error, (list, tuple)):
                _error = error
            elif isinstance(error, dict):
                _parsed_error = self._parse_error_message(error)
                _error = _parsed_error.get("errors")
                message = _parsed_error.get("message")
            else:
                logger.error("Error occurred while parsing error message")
                logger.error(error)
                raise ValueError(_("Error message is invalid"))
            _errors[key] = _error
            if message is None:
                message = _error[0]
        return {"errors": _errors, "message": message}


class ListAPIView(mixins.ListModelMixin, PaginatedListMixin, BaseAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CreateAPIView(mixins.CreateModelMixin, BaseAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveAPIView(mixins.RetrieveModelMixin, BaseAPIView):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateAPIView(mixins.UpdateModelMixin, BaseAPIView):

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DestroyAPIView(mixins.DestroyModelMixin, BaseAPIView):
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
