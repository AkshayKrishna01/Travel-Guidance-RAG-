# # from typing import Optional, Dict
# # import uuid
# # from datetime import datetime, timezone
# # from pydantic import ValidationError
# # from ..error_codes.error_codes import ApplicationError
# # from ..service.service import KnowledgeBaseService
# # from ..dtos.dtos import (
# #     APIResponse,KnowledgeBaseCreate,CreateKnowledgeBaseResponse,TravelGuidanceQuery,TravelGuidanceResponse
# # )
# # from typing import Dict, Any, List, Optional
# # class KnowledgeBaseController:
# #     def __init__(self):
# #         self.service = KnowledgeBaseService()
    
# #     def  create_knowledgebase_controller(self, raw_data) -> CreateKnowledgeBaseResponse:
# #         request_id = str(uuid.uuid4())
# #         try:
# #             if not raw_data:
# #                 print("no data")
# #                 raise ValidationError.from_exception_data("ValidationError", [{"type": "missing", "loc": ("body",), "msg": "Request body cannot be empty"}])
# #             if(isinstance(raw_data,dict)):
# #                 data = KnowledgeBaseCreate(**raw_data)
# #             else:
# #                 data =raw_data
# #             data = self.service.create_knowledgebase_service(data)
# #             return self._success_response(
# #                 201,"knowledge base created successfully",
# #                 {"data":""},request_id
# #             )
# #         except ValidationError as e:
# #             print("Controller Validation data error")
# #             print(e)
# #             return self.validation_error_response(e, request_id)
# #         except (TypeError, ValueError) as e:
# #             print("Controller Type Error and value error data")
# #             return self.validation_error_response(e,request_id)
# #         except ApplicationError as e:
# #             print("Controller Application error")
# #             return self._error_response(e, request_id)
# #         except Exception as e:
# #             print("Controller Exception")
# #             return self.validation_error_response(
# #                 ValidationError.from_exception_data(e,request_id)
# #             )
# #     def create_travelguidance_controller(self,raw_data) ->TravelGuidanceResponse:
# #         request_id = str(uuid.uuid4())
# #         try:
# #             print("Controller called",raw_data)
# #             if not raw_data:
# #                 print("no data")
# #                 raise ValidationError.from_exception_data("ValidationError", [{"type": "missing", "loc": ("body",), "msg": "Request body cannot be empty"}])
# #             if(isinstance(raw_data,dict)):
# #                 data=TravelGuidanceQuery(**raw_data)
# #             else:
# #                 data = raw_data
# #                 print(data)
# #             data = self.service.create_travelguidance_service(data)
# #             return self._success_response(
# #                 201,"Generated the travel guidance successfully",
# #                 {"data":data},request_id
# #             )
# #         except ValidationError as e:
# #             print("Controller Validation data",e)
# #             return self.validation_error_response(e, request_id)
# #         except (TypeError, ValueError) as e:
# #             print("Controller Type Error and value error data",e)
# #             return self.validation_error_response(e, request_id)

# #         except ApplicationError as e:
# #             print("Applcation Error",e)
# #             return self._error_response(e, request_id)
# #         except Exception as e:
# #             print("Other Exception",e)
# #             return self.validation_error_response(e, request_id)

# #     def success_response(code: int, message: str, data: Any, request_id: str) -> APIResponse:
# #         return APIResponse(
# #             code=code,
# #             status="success",
# #             message=message,
# #             data=data,
# #             errors=None,
# #             request_id=request_id,
# #             timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
# #         )

# #     def error_response(
# #         code: int,
# #         message: str,
# #         errors: Optional[List[Dict]] = None,
# #         request_id: Optional[str] = None
# #     ) -> APIResponse:
# #         return APIResponse(
# #             code=code,
# #             status="error",
# #             message=message,
# #             data=None,
# #             errors=errors or [],
# #             request_id=request_id ,
# #             timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
# # ,
# #             )
      
# #     # controller.py snippets

# #     # def _success_response(
# #     #     self, 
# #     #     code: int, 
# #     #     message: str, 
# #     #     data: Dict, 
# #     #     request_id: str
# #     # ) -> APIResponse:
# #     #     """Standard success response"""
# #     #     return APIResponse(
# #     #         code=code,
# #     #         status="success",
# #     #         message=message,
# #     #         data=data,
# #     #         request_id=request_id,
# #     #         timestamp=datetime.utcnow().isoformat()
# #     #     )
# #     # def _error_response(self, error: ApplicationError, request_id: str) -> APIResponse:
# #     #     return APIResponse(
# #     #         code=error.http_status,
# #     #         status="error",
# #     #         message=error.message,
# #     #         errors=[error.to_dict().get("error", {})],  # use errors (list)
# #     #         request_id=request_id,
# #     #         timestamp=datetime.utcnow().isoformat()
# #     #     )

# #     # def validation_error_response(self, error: ValidationError, request_id: str) -> APIResponse:
# #     #     errors_list = []
# #     #     for err in error.errors():
# #     #         field_path = " -> ".join(str(loc) for loc in err.get("loc", ()))
# #     #         msg = err.get("msg", "Validation error")
# #     #         errors_list.append({"code": "ZAP_VAL_022", "message": f"{field_path}: {msg}"})
        
# #     #     return APIResponse(
# #     #         code=400,
# #     #         status="error",
# #     #         message="Validation failed",
# #     #         data=None,  # data is set to None when no data is available
# #     #         errors=errors_list,
# #     #         error=None,  # error field is explicitly set to None
# #     #         request_id=request_id,
# #     #         timestamp=datetime.utcnow().isoformat()
# #     #     )
# from typing import Optional, Dict, Any, List
# import uuid
# from datetime import datetime, timezone
# from pydantic import ValidationError

# from ..error_codes.error_codes import ApplicationError
# from ..service.service import KnowledgeBaseService
# from ..dtos.dtos import (
#     APIResponse, KnowledgeBaseCreate, CreateKnowledgeBaseResponse,
#     TravelGuidanceQuery, TravelGuidanceResponse
# )

# def _utc_now_iso_z() -> str:
#     return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# class KnowledgeBaseController:
#     def __init__(self):
#         self.service = KnowledgeBaseService()

#     # ------------- Public controllers -------------

#     def create_knowledgebase_controller(self, raw_data) -> APIResponse:
#         request_id = str(uuid.uuid4())
#         try:
#             print("controller")
#             # Empty body detection (None or empty string/bytes)
#             if raw_data is None or  (isinstance(raw_data, dict) and len(raw_data) == 0):
#                 # build a 400 Validation failed with requested wording
#                 return self._error_response_from_parts(
#                     code=400,
#                     message="Validation failed",
#                     errors=[{"field": "body", "message": "Request body cannot be empty"}],
#                     request_id=request_id,
#                 )

#             if isinstance(raw_data, dict):
#                 data = KnowledgeBaseCreate(**raw_data)
#             else:
#                 data = raw_data

#             result = self.service.create_knowledgebase_service(data)
#             # success 201
#             return self._success_response(``
#                 201,
#                 "knowledge base created successfully",
#                 {"data":""},
#                 request_id
#             )

#         except ValidationError as e:
#             print("Controller ValidationError",e)
#             # Map pydantic validation to uniform error list
#             return self._validation_error_response(e, request_id)

#         except (TypeError, ValueError) as e:
#             print("Controller TypeErro ValueError")
#             # 500 with your “TypeError, ValueError error” message
#             return self._error_response_from_parts(
#                 code=500,
#                 message="TypeError, ValueError error",
#                 errors=[{"message": "Type Error or Value Error Catched in Controller layer"}],
#                 request_id=request_id,
#             )

#         except ApplicationError as e:
#             print("Controller ApplicationError",e)
#             # Map ApplicationError to error response
#             return self._application_error_response(e, request_id)

#         except Exception as e:
#             print("Controller Exeption",e)

#             # Internal server error with empty errors (as per your example #3)
#             return self._error_response_from_parts(
#                 code=500,
#                 message="Internal server error",
#                 errors=[{e}],
#                 request_id=request_id,
#             )

#     def create_travelguidance_controller(self, raw_data) -> APIResponse:
#         request_id = str(uuid.uuid4())
#         try:
#             print("controller called")
#             if raw_data is None or  (isinstance(raw_data, dict) and len(raw_data) == 0):
#                 return self._error_response_from_parts(
#                     code=400,
#                     message="Validation failed",
#                     errors=[{"field": "body", "message": "Request body cannot be empty"}],
#                     request_id=request_id,
#                 )

#             if isinstance(raw_data, dict):
#                 data = TravelGuidanceQuery(**raw_data)
#             else:
#                 data = raw_data

#             result = self.service.create_travelguidance_service(data)
#             print(result)
#             return self._success_response(
#                 201,
#                 "Generated the travel guidance successfully",
#                 {"data": result},
#                 request_id
#             )

#         except ValidationError as e:
#             print("Controller ValidationError",e)
#             return self._validation_error_response(e, request_id)

#         except (TypeError, ValueError):
#             print("Controller TypeErro ValueError")
#             return self._error_response_from_parts(
#                 code=500,
#                 message="TypeError, ValueError error",
#                 errors=[{"message": "Type Error or Value Error Catched in Controller layer"}],
#                 request_id=request_id,
#             )

#         except ApplicationError as e:
#             print("Controller ApplicationError",e)
#             return self._application_error_response(e, request_id)

#         except Exception as e:
#             print("Controller Exeption",e)
#             return self._error_response_from_parts(
#                 code=500,
#                 message="Internal server error",
#                 errors=[{e}],
#                 request_id=request_id,
#             )

#     # ------------- Private helpers -------------

#     def _success_response(self, code: int, message: str, data: Any, request_id: str) -> APIResponse:
#         return APIResponse(
#             code=code,
#             status="success",
#             message=message,
#             data=data,
#             errors=None,
#             request_id=request_id,
#             timestamp=_utc_now_iso_z(),
#         )

#     def _error_response_from_parts(
#         self,
#         code: int,
#         message: str,
#         errors: Optional[List[Dict]],
#         request_id: str
#     ) -> APIResponse:
#         return APIResponse(
#             code=code,
#             status="error",
#             message=message,
#             data=None,
#             errors=errors or [],
#             request_id=request_id,
#             timestamp=_utc_now_iso_z(),
#         )

#     def _application_error_response(self, error: ApplicationError, request_id: str) -> APIResponse:
#         """
#         Converts your ApplicationError to the response shape:
#         - If you need very specific messages (Vector DB, Embedded Model, etc.),
#           you can inspect error.code and choose message strings accordingly.
#         - Here, we default to “Application error” with the inner message as an entry.
#         """
#         # If you want to map specific codes to specific messages:
#         # from ..error_codes.error_codes import ErrorCode
#         # if error.code == ErrorCode.VECTOR_DB_CONNECTION.value:
#         #     return self._error_response_from_parts(500, "Vector Database Connection failed",
#         #         [{"message": "Cannot connect to the Vector Database"}], request_id)

#         return self._error_response_from_parts(
#             code=error.http_status,
#             message="Application error" if error.http_status >= 500 else error.message,
#             errors=[{"message": error.message}],
#             request_id=request_id,
#         )

#     def _validation_error_response(self, error: ValidationError, request_id: str) -> APIResponse:
#         """
#         Produces a 400 response like your example #2 and #7
#         using a list of {field, message}.
#         """
#         errors_list: List[Dict[str, str]] = []
#         for err in error.errors():
#             field_path = " -> ".join(str(loc) for loc in err.get("loc", ())) or "body"
#             msg = err.get("msg", "Validation error")
#             errors_list.append({"field": field_path, "message": msg})

#         return self._error_response_from_parts(
#             code=400,
#             message="Validation failed",
#             errors=errors_list,
#             request_id=request_id,
#         )
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime, timezone
from pydantic import ValidationError

from ..error_codes.error_codes import ApplicationError


from ..service.service import KnowledgeBaseService
from ..dtos.dtos import (
    APIResponse, KnowledgeBaseCreate, CreateKnowledgeBaseResponse,
    TravelGuidanceQuery, TravelGuidanceResponse
)


def _utc_now_iso_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


_LOCAL_TOP_MESSAGE_MAP: Dict[str, str] = {
    "ZAP_VEC_101": "Vector Database Connection failed",
    "ZAP_EMB_102": "Embedded Model Connection failed",
    "ZAP_VEC_103": "Vector Generation failed",
    "ZAP_REQ_104": "Malformed JSON in request",
    "ZAP_REQ_105": "Request body is empty",
    "ZAP_CTL_106": "Controller type/value error",
    "ZAP_APP_107": "Application error",
    "ZAP_SQL_005": "Database error",
    "ZAP_VAL_022": "Validation failed",
    "ZAP_GEN_030": "Resource not found",
    "ZAP_AUTH_018": "Unauthorized",
    "ZAP_AUTH_026": "Forbidden",
    "ZAP_SRV_006": "Internal server error",
}


class KnowledgeBaseController:
    def __init__(self):
        self.service = KnowledgeBaseService()


    def create_knowledgebase_controller(self, raw_data) -> APIResponse:
        request_id = str(uuid.uuid4())
        try:
            if raw_data is None or (isinstance(raw_data, dict) and len(raw_data) == 0):
                return self._error_response_from_parts(
                    code=400,
                    message="Validation failed",
                    errors=[{"field": "body", "message": "Request body cannot be empty"}],
                    request_id=request_id,
                )

            if isinstance(raw_data, dict):
                data = KnowledgeBaseCreate(**raw_data)
            else:
                data = raw_data

            result = self.service.create_knowledgebase_service(data)

            return self._success_response(
                201,
                "Knowledge base created successfully",
                {"data": ""}, 
                request_id
            )

        except ValidationError as e:
            return self._validation_error_response(e, request_id)

        except (TypeError, ValueError) as e:

            return self._error_response_from_parts(
                code=500,
                message=_LOCAL_TOP_MESSAGE_MAP.get("ZAP_CTL_106", "Application error"),
                errors=[{"message": "Type Error or Value Error caught in Controller layer"}],
                request_id=request_id,
            )

        except ApplicationError as e:
            return self._application_error_response(e, request_id)

        except Exception as e:
            return self._error_response_from_parts(
                code=500,
                message="Internal server error",
                errors=[{"message": str(e)}],
                request_id=request_id,
            )

    def create_travelguidance_controller(self, raw_data) -> APIResponse:
        request_id = str(uuid.uuid4())
        try:
            if raw_data is None or (isinstance(raw_data, dict) and len(raw_data) == 0):
                return self._error_response_from_parts(
                    code=400,
                    message="Validation failed",
                    errors=[{"field": "body", "message": "Request body cannot be empty"}],
                    request_id=request_id,
                )

            if isinstance(raw_data, dict):
                data = TravelGuidanceQuery(**raw_data)
            else:
                data = raw_data

            result = self.service.create_travelguidance_service(data)
            return self._success_response(
                201,
                "Generated the travel guidance successfully",
                {"data": result},
                request_id
            )

        except ValidationError as e:
            return self._validation_error_response(e, request_id)

        except (TypeError, ValueError):
            return self._error_response_from_parts(
                code=500,
                message=_LOCAL_TOP_MESSAGE_MAP.get("ZAP_CTL_106", "Application error"),
                errors=[{"message": "Type Error or Value Error caught in Controller layer"}],
                request_id=request_id,
            )

        except ApplicationError as e:
            return self._application_error_response(e, request_id)

        except Exception as e:
            return self._error_response_from_parts(
                code=500,
                message="Internal server error",
                errors=[{"message": str(e)}],
                request_id=request_id,
            )


    def _success_response(self, code: int, message: str, data: Any, request_id: str) -> APIResponse:
        return APIResponse(
            code=code,
            status="success",
            message=message,
            data=data,
            errors=None,
            request_id=request_id,
            timestamp=_utc_now_iso_z(),
        )

    def _error_response_from_parts(
        self,
        code: int,
        message: str,
        errors: Optional[List[Dict]],
        request_id: str
    ) -> APIResponse:
        return APIResponse(
            code=code,
            status="error",
            message=message,
            data=None,
            errors=errors or [],
            request_id=request_id,
            timestamp=_utc_now_iso_z(),
        )

    def _application_error_response(self, error: ApplicationError, request_id: str) -> APIResponse:

        top_message = _LOCAL_TOP_MESSAGE_MAP.get(
            getattr(error, "error_code", None).value if getattr(error, "error_code", None) else getattr(error, "code", None),
            "Application error"
        )

        return self._error_response_from_parts(
            code=error.http_status,
            message=top_message,
            errors=[{"message": error.message}],
            request_id=request_id,
        )

    def _validation_error_response(self, error: ValidationError, request_id: str) -> APIResponse:
        errors_list: List[Dict[str, str]] = []
        for err in error.errors():
            field_path = " -> ".join(str(loc) for loc in err.get("loc", ())) or "body"
            msg = err.get("msg", "Validation error")
            errors_list.append({"field": field_path, "message": msg})

        return self._error_response_from_parts(
            code=400,
            message="Validation failed",
            errors=errors_list,
            request_id=request_id,
        )