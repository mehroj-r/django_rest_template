from dmr import Controller
from dmr.plugins.msgspec import MsgspecSerializer
from dmr.security.jwt.auth import JWTSyncAuth


class BaseController(Controller[MsgspecSerializer]):
    SUCCESS_MESSAGE = "OK"
    ERROR_MESSAGE = "NOT OK"
    auth = (JWTSyncAuth(),)

    @staticmethod
    def ok(data):
        return {
            "success": True,
            "message": "OK",
            "data": data,
        }

    @staticmethod
    def fail(error, message: str = "NOT OK"):
        return {
            "success": False,
            "message": message,
            "error": error,
        }


class BaseAPIView(BaseController):
    ...
