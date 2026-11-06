from fastapi import APIRouter, Query, Request, HTTPException, Response
from typing import Optional
import json
from ..dtos.dtos import (
    APIResponse,KnowledgeBaseCreate,CreateKnowledgeBaseResponse,TravelGuidanceQuery,TravelGuidanceResponse
)
from ..controller.controller import KnowledgeBaseController
from ..error_codes.error_codes import ApplicationError
from ..utils.utils import create_api_response

router = APIRouter(prefix="/api/v1/Travel_guidance", tags=["KnowledgeBase"])


def handle_application_error(e: ApplicationError, request_id: str) -> APIResponse:
    """Handle standardized ApplicationError"""
    return create_api_response(
        code=e.http_status,
        status="error",
        message=e.message,
        error=e.to_dict()["error"],
        request_id=request_id
    )

@router.post("/kb_creation/preprocessing", response_model=CreateKnowledgeBaseResponse,response_model_exclude_none=False, status_code=201)
async def create_knowledgebase_route(request: Request, response: Response):
    controller = KnowledgeBaseController()
    print("route called")
    try:
        print("route called")
        raw_data = await request.json()
        print("route raw data",raw_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request body")
    result = controller.create_knowledgebase_controller(raw_data)
    response.status_code = result.code
    return result

@router.post("/get_guidance",response_model=TravelGuidanceResponse,response_model_exclude_none=False,status_code=201)
async def create_knowledgebase_route(request:Request,response:Response):
    controller=KnowledgeBaseController()
    try:
        print("route called")
        raw_data = await request.json()
        print("route raw data",raw_data)
      
    except json.JSONDecodeError:
        print("router Invalid JSON format")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception:
        print("router Invalid request body")
        raise HTTPException(status_code=400, detail="Invalid request body")
    result = controller.create_travelguidance_controller(raw_data)
    response.status_code = result.code
    return result
