# # from enum import Enum
# # from typing import Optional, Dict, Any

# # # -------------------------------------------------
# # # Error Codes
# # # -------------------------------------------------
# # class ErrorCode(Enum):
# #     DATABASE_ERROR = "ZAP_SQL_005"
# #     VALIDATION_ERROR = "ZAP_VAL_022"
# #     NOT_FOUND = "ZAP_GEN_030"
# #     UNAUTHORIZED = "ZAP_AUTH_018"
# #     FORBIDDEN = "ZAP_AUTH_026"
# #     INTERNAL_SERVER_ERROR = "ZAP_SRV_006"

# # # -------------------------------------------------
# # # HTTP Status Mapping
# # # -------------------------------------------------
# # HTTP_STATUS_MAP = {
# #     ErrorCode.DATABASE_ERROR: 500,
# #     ErrorCode.VALIDATION_ERROR: 400,
# #     ErrorCode.NOT_FOUND: 404,
# #     ErrorCode.UNAUTHORIZED: 401,
# #     ErrorCode.FORBIDDEN: 403,
# #     ErrorCode.INTERNAL_SERVER_ERROR: 500,
# # }

# # # -------------------------------------------------
# # # Custom Application Exception
# # # -------------------------------------------------
# # class ApplicationError(Exception):
# #     def __init__(
# #         self,
# #         error_code: ErrorCode,
# #         message: str,
# #         details: Optional[Dict[str, Any]] = None
# #     ):
# #         self.code = error_code.value
# #         self.http_status = HTTP_STATUS_MAP.get(error_code, 500)
# #         self.message = message
# #         self.details = details or {}
# #         super().__init__(self.message)

# #     def to_dict(self) -> Dict[str, Any]:
# #         return {
# #             "error": {
# #                 "code": self.code,
# #                 "message": self.message,
# #                 "details": self.details
# #             }
# #         }

# # # -------------------------------------------------
# # # Helper Functions
# # # -------------------------------------------------
# # def validation_error(field: str, reason: str) -> ApplicationError:
# #     return ApplicationError(
# #         ErrorCode.VALIDATION_ERROR,
# #         message=f"Invalid value for '{field}'",
# #         details={"reason": reason}
# #     )

# # def not_found_error(resource: str) -> ApplicationError:
# #     return ApplicationError(
# #         ErrorCode.NOT_FOUND,
# #         message=f"{resource} not found"
# #     )

# # def database_error(operation: str) -> ApplicationError:
# #     return ApplicationError(
# #         ErrorCode.DATABASE_ERROR,
# #         message=f"Database {operation} failed"
# #     )

# # def unauthorized_error() -> ApplicationError:
# #     return ApplicationError(
# #         ErrorCode.UNAUTHORIZED,
# #         message="User is not authenticated"
# #     )

# # def forbidden_error() -> ApplicationError:
# #     return ApplicationError(
# #         ErrorCode.FORBIDDEN,
# #         message="Access denied"
# #     )
# # error_codes/error_codes.py
# from enum import Enum
# from typing import Optional, Dict, Any

# # -------------------------------------------------
# # Error Codes
# # -------------------------------------------------
# class ErrorCode(Enum):
#     DATABASE_ERROR = "ZAP_SQL_005"
#     VALIDATION_ERROR = "ZAP_VAL_022"
#     NOT_FOUND = "ZAP_GEN_030"
#     UNAUTHORIZED = "ZAP_AUTH_018"
#     FORBIDDEN = "ZAP_AUTH_026"
#     INTERNAL_SERVER_ERROR = "ZAP_SRV_006"

#     # Added new app-specific codes (feel free to change codes if you have a naming scheme)
#     VECTOR_DB_CONNECTION = "ZAP_VEC_101"
#     EMBEDDED_MODEL_CONNECTION = "ZAP_EMB_102"
#     VECTOR_GENERATION = "ZAP_VEC_103"
#     JSON_MALFORMED = "ZAP_REQ_104"
#     EMPTY_BODY = "ZAP_REQ_105"
#     TYPE_VALUE_ERROR = "ZAP_CTL_106"
#     APPLICATION_ERROR = "ZAP_APP_107"

# # -------------------------------------------------
# # HTTP Status Mapping
# # -------------------------------------------------
# HTTP_STATUS_MAP = {
#     ErrorCode.DATABASE_ERROR: 500,
#     ErrorCode.VALIDATION_ERROR: 400,
#     ErrorCode.NOT_FOUND: 404,
#     ErrorCode.UNAUTHORIZED: 401,
#     ErrorCode.FORBIDDEN: 403,
#     ErrorCode.INTERNAL_SERVER_ERROR: 500,

#     # New error status codes
#     ErrorCode.VECTOR_DB_CONNECTION: 500,
#     ErrorCode.EMBEDDED_MODEL_CONNECTION: 500,
#     ErrorCode.VECTOR_GENERATION: 500,
#     ErrorCode.JSON_MALFORMED: 400,
#     ErrorCode.EMPTY_BODY: 400,
#     ErrorCode.TYPE_VALUE_ERROR: 500,
#     ErrorCode.APPLICATION_ERROR: 500,
# }

# # -------------------------------------------------
# # Custom Application Exception
# # -------------------------------------------------
# class ApplicationError(Exception):
#     def __init__(
#         self,
#         error_code: ErrorCode,
#         message: str,
#         details: Optional[Dict[str, Any]] = None
#     ):
#         self.code = error_code.value
#         self.http_status = HTTP_STATUS_MAP.get(error_code, 500)
#         self.message = message
#         self.details = details or {}
#         super().__init__(self.message)

#     def to_dict(self) -> Dict[str, Any]:
#         return {
#             "error": {
#                 "code": self.code,
#                 "message": self.message,
#                 "details": self.details
#             }
#         }

# # -------------------------------------------------
# # Helper Constructors (keep your existing + add new)
# # -------------------------------------------------
# def validation_error(field: str, reason: str) -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.VALIDATION_ERROR,
#         message=f"Invalid value for '{field}'",
#         details={"reason": reason}
#     )

# def not_found_error(resource: str) -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.NOT_FOUND,
#         message=f"{resource} not found"
#     )

# def database_error(operation: str) -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.DATABASE_ERROR,
#         message=f"Database {operation} failed"
#     )

# def unauthorized_error() -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.UNAUTHORIZED,
#         message="User is not authenticated"
#     )

# def forbidden_error() -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.FORBIDDEN,
#         message="Access denied"
#     )

# # ---- New helpers matching your desired shapes ----

# def empty_body_error() -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.EMPTY_BODY,
#         message="Request body cannot be empty",
#         details={"field": "body"}
#     )

# def malformed_json_error() -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.JSON_MALFORMED,
#         message="Request body contains invalid JSON",
#         details={"field": "body"}
#     )

# def vector_db_connection_error() -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.VECTOR_DB_CONNECTION,
#         message="Cannot connect to the Vector Database"
#     )

# def embedded_model_connection_error() -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.EMBEDDED_MODEL_CONNECTION,
#         message="Cannot connect to the Embedded Model"
#     )

# def vector_generation_error() -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.VECTOR_GENERATION,
#         message="Cannot Generate the Vector Points"
#     )

# def type_value_error() -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.TYPE_VALUE_ERROR,
#         message="Type Error or Value Error Catched in Controller layer"
#     )

# def generic_application_error(msg: str = "Application Error Catched in Controller Layer") -> ApplicationError:
#     return ApplicationError(
#         ErrorCode.APPLICATION_ERROR,
#         message=msg
#     )
# error_codes/error_codes.py
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone


class ErrorCode(Enum):
    DATABASE_ERROR = "ZAP_SQL_005"
    VALIDATION_ERROR = "ZAP_VAL_022"
    NOT_FOUND = "ZAP_GEN_030"
    UNAUTHORIZED = "ZAP_AUTH_018"
    FORBIDDEN = "ZAP_AUTH_026"
    INTERNAL_SERVER_ERROR = "ZAP_SRV_006"

    VECTOR_DB_CONNECTION = "ZAP_VEC_101"
    EMBEDDED_MODEL_CONNECTION = "ZAP_EMB_102"
    VECTOR_GENERATION = "ZAP_VEC_103"
    JSON_MALFORMED = "ZAP_REQ_104"
    EMPTY_BODY = "ZAP_REQ_105"
    TYPE_VALUE_ERROR = "ZAP_CTL_106"
    APPLICATION_ERROR = "ZAP_APP_107"
    LLM_MODEL_CONNECTION = "ZAP_LMB_108"

HTTP_STATUS_MAP = {
    ErrorCode.DATABASE_ERROR: 500,
    ErrorCode.VALIDATION_ERROR: 400,
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.UNAUTHORIZED: 401,
    ErrorCode.FORBIDDEN: 403,
    ErrorCode.INTERNAL_SERVER_ERROR: 500,
    ErrorCode.LLM_MODEL_CONNECTION:500,
    ErrorCode.VECTOR_DB_CONNECTION: 500,
    ErrorCode.EMBEDDED_MODEL_CONNECTION: 500,
    ErrorCode.VECTOR_GENERATION: 500,
    ErrorCode.JSON_MALFORMED: 400,
    ErrorCode.EMPTY_BODY: 400,
    ErrorCode.TYPE_VALUE_ERROR: 500,
    ErrorCode.APPLICATION_ERROR: 500,
}

TOP_LEVEL_MESSAGE_MAP: Dict[ErrorCode, str] = {
    ErrorCode.VECTOR_DB_CONNECTION: "Vector Database Connection failed",
    ErrorCode.EMBEDDED_MODEL_CONNECTION: "Embedded Model Connection failed",
    ErrorCode.VECTOR_GENERATION: "Vector Generation failed",
    ErrorCode.JSON_MALFORMED: "Malformed JSON in request",
    ErrorCode.EMPTY_BODY: "Request body is empty",
    ErrorCode.TYPE_VALUE_ERROR: "Controller type/value error",
    ErrorCode.APPLICATION_ERROR: "Application error",
    ErrorCode.LLM_MODEL_CONNECTION:"LLM Model Connection failed",
    ErrorCode.DATABASE_ERROR: "Database error",
    ErrorCode.VALIDATION_ERROR: "Validation error",
    ErrorCode.NOT_FOUND: "Resource not found",
    ErrorCode.UNAUTHORIZED: "Unauthorized",
    ErrorCode.FORBIDDEN: "Forbidden",
    ErrorCode.INTERNAL_SERVER_ERROR: "Internal server error",
}


class ApplicationError(Exception):
    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code
        self.code = error_code.value  
        self.http_status = HTTP_STATUS_MAP.get(error_code, 500)
        self.message = message  
        self.details = details or {}
        super().__init__(self.message)

    def to_error_items(self) -> List[Dict[str, Any]]:
  
        base = {"message": self.message}
        if self.details:
            base["details"] = self.details

        return [base]

def build_error_response(
    err: ApplicationError,
    request_id: str,
    timestamp_utc_iso: Optional[str] = None
) -> Dict[str, Any]:

    if timestamp_utc_iso is None:
        timestamp_utc_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    top_message = TOP_LEVEL_MESSAGE_MAP.get(err.error_code, "Application error")

    return {
        "code": err.http_status,
        "status": "error",
        "message": top_message,
        "errors": err.to_error_items(),
        "request_id": request_id,
        "timestamp": timestamp_utc_iso,
    }

def validation_error(field: str, reason: str) -> ApplicationError:
    return ApplicationError(
        ErrorCode.VALIDATION_ERROR,
        message=f"Invalid value for '{field}'",
        details={"reason": reason}
    )

def not_found_error(resource: str) -> ApplicationError:
    return ApplicationError(
        ErrorCode.NOT_FOUND,
        message=f"{resource} not found"
    )

def database_error(operation: str) -> ApplicationError:
    return ApplicationError(
        ErrorCode.DATABASE_ERROR,
        message=f"Database {operation} failed"
    )

def unauthorized_error() -> ApplicationError:
    return ApplicationError(
        ErrorCode.UNAUTHORIZED,
        message="User is not authenticated"
    )

def forbidden_error() -> ApplicationError:
    return ApplicationError(
        ErrorCode.FORBIDDEN,
        message="Access denied"
    )

def empty_body_error() -> ApplicationError:
    return ApplicationError(
        ErrorCode.EMPTY_BODY,
        message="Request body cannot be empty",
        details={"field": "body"}
    )

def malformed_json_error() -> ApplicationError:
    return ApplicationError(
        ErrorCode.JSON_MALFORMED,
        message="Request body contains invalid JSON",
        details={"field": "body"}
    )

def vector_db_connection_error() -> ApplicationError:
    return ApplicationError(
        ErrorCode.VECTOR_DB_CONNECTION,
        message="Cannot connect to the Vector Database"
    )

def embedded_model_connection_error() -> ApplicationError:
    return ApplicationError(
        ErrorCode.EMBEDDED_MODEL_CONNECTION,
        message="Cannot connect to the Embedded Model"
    )

def llm_model_connection_error() -> ApplicationError:
    return ApplicationError(
        ErrorCode.LLM_MODEL_CONNECTION,
        message="Cannot connect to the LLM Model"
    )
def vector_generation_error() -> ApplicationError:
    return ApplicationError(
        ErrorCode.VECTOR_GENERATION,
        message="Cannot generate vector points"
    )

def type_value_error() -> ApplicationError:
    return ApplicationError(
        ErrorCode.TYPE_VALUE_ERROR,
        message="TypeError or ValueError caught in controller layer"
    )

def generic_application_error(msg: str = "Application error caught in controller layer") -> ApplicationError:
    return ApplicationError(
        ErrorCode.APPLICATION_ERROR,
        message=msg
    )