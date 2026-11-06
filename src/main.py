from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from json import JSONDecodeError
import uvicorn
import os
import logging
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
from .config.config_manager import config
from .routes.routes import router
from .database.database_connection import Database

# Global variables
load_dotenv()
db_connection = None
app=None
logger = logging.getLogger(__name__)

# ---------- Helpers to build your uniform response ----------
def _utc_now_iso_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _new_req_id() -> str:
    return str(uuid.uuid4())

def _error_json(code: int, message: str, errors):
    return {
        "code": code,
        "status": "error",
        "message": message,
        "errors": errors or [],
        "request_id": _new_req_id(),
        "timestamp": _utc_now_iso_z(),
    }

# ---------- Global handlers/middleware ----------

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic/FastAPI request-layer validation errors with your shape.
    Maps empty body and general validation to 400 "Validation failed".
    """
    # Inspect errors to differentiate empty body vs field validation
    errs = []
    empty_body_detected = False

    for e in exc.errors():
        loc = " -> ".join(str(p) for p in e.get("loc", [])) or "body"
        msg = e.get("msg", "Validation error")

        # Heuristics: mark empty body; tweak as needed for your schema
        if "body" in loc.lower() and ("none" in msg.lower() or "empty" in msg.lower()):
            empty_body_detected = True

        errs.append({"field": loc, "message": msg})

    if empty_body_detected:
        payload = _error_json(
            400,
            "Validation failed",
            [{"field": "body", "message": "Request body cannot be empty"}],
        )
        return JSONResponse(status_code=400, content=payload)

    # Generic validation failed
    payload = _error_json(400, "Validation failed", errs)
    return JSONResponse(status_code=400, content=payload)

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Converts Starlette/FastAPI HTTP exceptions to your JSON shape.
    Customize messages per status as needed.
    """
    code = exc.status_code
    if code == 404:
        payload = _error_json(404, "Application error", [{"message": "Not found"}])
        return JSONResponse(status_code=404, content=payload)
    if code == 403:
        payload = _error_json(403, "Application error", [{"message": "Access denied"}])
        return JSONResponse(status_code=403, content=payload)
    if code == 401:
        payload = _error_json(401, "Application error", [{"message": "User is not authenticated"}])
        return JSONResponse(status_code=401, content=payload)

    # Fallback: show the detail if provided
    payload = _error_json(code, "Application error", [{"message": exc.detail or "Error"}])
    return JSONResponse(status_code=code, content=payload)

# Malformed JSON (occurs before controller if body isn’t valid JSON)
async def malformed_json_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except JSONDecodeError:
        payload = _error_json(
            400,
            "Invalid JSON format",
            [{"field": "body", "message": "Request body contains invalid JSON"}],
        )
        return JSONResponse(status_code=400, content=payload)

# Catch-all handler for any other unhandled exceptions → your #3
async def unhandled_exception_handler(request: Request, exc: Exception):
    payload = _error_json(500, "Internal server error", [])
    return JSONResponse(status_code=500, content=payload)

# ---------- Config / app creation ----------

def initialize_config():
    """Initialize configuration from AWS Secrets Manager or environment variables"""
    global app_config, db_connection
    try:
        app_config = config

        # Initialize database connection with the config
        db_connection = Database()

        # Set logging level from config
        log_level = getattr(logging, app_config.log_level.upper(), logging.INFO)
        logging.getLogger().setLevel(log_level)

        logger.info("Configuration initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize configuration: {e}")
        return False

def create_app():
    """Create and configure the FastAPI app"""
    # Determine root path for API Gateway
    root_path = ""
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        stage = os.getenv("API_GATEWAY_STAGE", "Prod")
        root_path = f"/{stage}"

    app = FastAPI(
        title="Travel Guidance Backend Service",
        description="Travel Guidance API for creating the knowledge base and get LLM response on travel query",
        version="1.0.0",
        root_path=root_path
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
        allow_headers=[
            "Accept",
            "Accept-Language",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "accessToken",
            "deviceIdentifier",
            "X-RequestID",
            "X-Requested-With",
            "Origin",
            "Cache-Control",
            "Pragma"
        ],
        expose_headers=["*"],
        max_age=3600,
    )

    # Add middleware & exception handlers
    app.middleware("http")(malformed_json_middleware)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Register routers
    app.include_router(router)

    return app

def run_local_server():
    """Run the server locally with uvicorn"""
    logger.info("Starting in local development mode...")

    # Initialize configuration
    if not initialize_config():
        logger.error("Failed to initialize configuration")
        exit(1)

    # Test database connection
    if not db_connection.test_connection():
        logger.error("Database connection test failed")
        exit(1)

    # Run migrations and seeder
    try:
        from .migration.migration import Migration
        from .migration.seeder import Seeder

        migration = Migration()
        migration.create_tables()
        logger.info("Database tables created successfully")

        seeder = Seeder()
        seeder.seed_data()
        logger.info("Database seeded successfully")
    except Exception as e:
        logger.warning(f"Migration/Seeding failed: {e}")

    # Start uvicorn server using config
    port = int(app_config.port)
    host = app_config.host

    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"Database: {app_config.db_host}:{app_config.db_port}/{app_config.db_name}")
    logger.info(f"Config source: {'AWS Secrets Manager' if os.getenv('SECRET_NAME') else 'Environment Variables'}")

    app = create_app()

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False,
        log_level=app_config.log_level.lower(),
        access_log=True
    )

# Entry point for local development
if __name__ == "__main__":
    try:
        run_local_server()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        exit(1)