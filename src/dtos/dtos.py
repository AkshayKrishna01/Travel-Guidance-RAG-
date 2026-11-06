from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime

from typing import Optional, Any, List, Dict

class APIResponse(BaseModel):
    code: int
    status: str  # "success" | "error"
    message: str
    data: Optional[Any] = None
    errors: Optional[List[Dict]] = None
    request_id: str
    timestamp: str

# Input DTOs
class CreateKnowledgeBaseResponse(APIResponse):
    pass


class KnowledgeBaseCreate(BaseModel):
    place_details:str

class TravelGuidanceQuery(BaseModel):
    user_query:str
    

class TravelGuidanceResponse(APIResponse):
    pass