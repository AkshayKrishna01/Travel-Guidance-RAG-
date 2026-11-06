
#utils.py
from datetime import datetime
from ..dtos.dtos import APIResponse


def create_api_response(
    code: int, status: str, message: str, 
    data: dict = None, error: dict = None, request_id: str = None
) -> APIResponse:
    return APIResponse(
        code=code, status=status, message=message, 
        data=data, error=error, request_id=request_id,
        timestamp=datetime.utcnow().isoformat()
    )