from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger


def create_exception_handler(status_code: int, message: str = None) -> callable:
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(str(exc))
        final_message = str(exc) if message is None else message

        return JSONResponse(
            status_code=status_code,
            content={"message": final_message}
        )
    return exception_handler


common_handler = create_exception_handler(500, "Произошла внутренняя ошибка сервера")
common_db_handler = create_exception_handler(400, "Произошла ошибка при получении данных")
not_found_handler = create_exception_handler(404)
