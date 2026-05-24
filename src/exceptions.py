from litestar import Request, Response
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)


class AppError(Exception):
    status_code: int = HTTP_400_BAD_REQUEST

    def __init__(self, message: str) -> None:
        self.message = message


class NotFoundError(AppError):
    status_code = HTTP_404_NOT_FOUND


class UnauthorizedError(AppError):
    status_code = HTTP_401_UNAUTHORIZED


class ConflictError(AppError):
    status_code = HTTP_409_CONFLICT


def app_exception_handler(request: Request, exc: AppError) -> Response:
    return Response({"detail": exc.message}, status_code=exc.status_code)
