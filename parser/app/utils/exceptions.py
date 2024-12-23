from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=404, detail=detail)


class CommonDBException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=400, detail=detail)
