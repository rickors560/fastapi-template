import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from .events import register_event_pollers
from .exceptions.global_handler import register_global_exception_handlers
from .jobs import scheduler
from .middlewares.request_logger_middleware import add_request_logger_middleware
from .routes import hello_world_router, sample_router
from .db.context import DbContext
from . import entities


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger(__name__)
    poller_task = None

    try:
        # Startup
        logger.info("Starting application services...")
        poller_task = asyncio.create_task(register_event_pollers())

        if not scheduler.running:
            scheduler.start()
            logger.info("Scheduler started successfully")

        logger.info("Application startup complete")

        yield

    finally:
        # Shutdown
        logger.info("Shutting down application services...")

        if poller_task and not poller_task.done():
            poller_task.cancel()
            try:
                await poller_task
            except asyncio.CancelledError:
                logger.info("Event poller cancelled successfully")

        if scheduler.running:
            scheduler.shutdown(wait=True)
            logger.info("Scheduler shutdown complete")

        # Close database connections
        await DbContext.dispose_engine()
        logger.info("Database connections closed")

        logger.info("Application shutdown complete")


def setup_application():
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        title="FastAPI Template",
        description="Production-ready FastAPI template with database, jobs, and event processing",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS Configuration - Configure allowed origins from environment variables
    from . import settings
    allowed_origins = getattr(settings, 'cors_allowed_origins', '*')
    if allowed_origins == '*':
        allowed_origins = ["*"]
    elif isinstance(allowed_origins, str):
        allowed_origins = [origin.strip() for origin in allowed_origins.split(',')]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        max_age=600,  # Cache preflight requests for 10 minutes
    )

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "healthy", "service": "fastapi-template"}

    # Register routers
    app.include_router(hello_world_router, prefix="/api/v1/hello-world", tags=["Hello World"])
    app.include_router(sample_router, prefix="/api/v1/samples", tags=["Samples"])

    register_global_exception_handlers(app)
    add_request_logger_middleware(app)

    return app


application = setup_application()
