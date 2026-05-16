import jwt
from json import JSONDecodeError, loads

from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dmr.security.jwt.views import ObtainTokensSyncController, RefreshTokenSyncController


class LoginAPIView(ObtainTokensSyncController):
    def convert_auth_payload(self, request):
        return {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
        }


class RefreshAPIView(RefreshTokenSyncController):
    def convert_refresh_payload(self, request):
        return request.data.get("refresh") or request.data.get("refresh_token")


@method_decorator(csrf_exempt, name="dispatch")
class TokenVerifyAPIView(View):
    def post(self, request, *args, **kwargs):
        token = None
        try:
            payload = loads((request.body or b"{}").decode("utf-8"))
        except (UnicodeDecodeError, JSONDecodeError):
            payload = {}

        if isinstance(payload, dict):
            token = payload.get("token")

        if token is None:
            return JsonResponse({"detail": "Token is invalid"}, status=400)

        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return JsonResponse({"detail": "Token is invalid"}, status=400)

        return JsonResponse({"detail": "Token is valid"}, status=200)
