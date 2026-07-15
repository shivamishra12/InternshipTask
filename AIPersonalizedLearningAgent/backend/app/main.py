from contextlib import asynccontextmanager
from pathlib import Path
import time
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.exceptions import AppException
from app.config.logging_config import setup_logging, get_logger
from app.api.routers.dashboard import router as dashboard_router
from app.api.routers.predict import router as predict_router
from app.api.routers.knowledge import router as knowledge_router
from app.api.routers.weak_topics import router as weak_topics_router
from app.api.routers.recommendations import router as recommendations_router
from app.api.routers.study_plan import router as study_plan_router

# Initialize logging
setup_logging()
logger = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup lifecycle
    logger.info(f"Starting up {settings.APP_NAME} in environment: {settings.ENV}")
    try:
        from app.services.model_loader import ModelLoader
        ModelLoader.load_all_models()
        logger.info("All ML models loaded successfully into memory.")
    except Exception as e:
        logger.critical(f"Critical error: Failed to load ML models at startup: {e}")
        raise e
    yield
    # Shutdown lifecycle
    logger.info(f"Shutting down {settings.APP_NAME}")

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-grade backend for the AI Personalized Learning Agent.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(predict_router, prefix="/api/v1")
app.include_router(knowledge_router, prefix="/api/v1")
app.include_router(weak_topics_router, prefix="/api/v1")
app.include_router(recommendations_router, prefix="/api/v1")
app.include_router(study_plan_router, prefix="/api/v1")

# Enable CORS
if settings.BACKEND_CORS_ORIGINS:
    origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    # Handle wildcard or specific lists
    if "*" in origins:
        origins = ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True if "*" not in origins else False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS middleware added with origins: {origins}")

# --- Exception Handlers ---

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handles custom application exceptions and logs the warning/error"""
    logger.error(f"AppException raised on path {request.url.path}: {exc.message} (status: {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles Pydantic/FastAPI request validation errors"""
    errors = exc.errors()
    logger.warning(f"Validation failure on path {request.url.path}: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Request validation failed", "errors": errors}
    )

@app.exception_handler(Exception)
async def catch_all_exception_handler(request: Request, exc: Exception):
    """Catch-all for unhandled exceptions to prevent leaking stack traces"""
    logger.critical(f"Unhandled exception on path {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."}
    )

# --- Base Middleware ---

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Logs the process time and request status for performance metrics"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"Request: {request.method} {request.url.path} - "
        f"Response Status: {response.status_code} - "
        f"Duration: {process_time:.4f}s"
    )
    response.headers["X-Process-Time"] = str(process_time)
    return response

# --- Health Check Endpoint ---

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    """Simple API status checks"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENV
    }

# --- Frontend ---

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
    logger.info(f"Frontend mounted from: {FRONTEND_DIR}")
else:
    logger.warning(f"Frontend directory not found at: {FRONTEND_DIR}")
