import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.config import get_settings
from app.database import init_db
from app.routes import subscribers, briefs, news
from app.services.scheduler import start_scheduler, stop_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.app_name}...")
    init_db()
    start_scheduler()
    yield
    stop_scheduler()
    logger.info(f"{settings.app_name} shutting down.")


app = FastAPI(
    title=settings.app_name,
    description="AI news aggregation and daily brief service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subscribers.router)
app.include_router(briefs.router)
app.include_router(news.router)

pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pdfs")
os.makedirs(pdf_dir, exist_ok=True)
app.mount("/pdfs", StaticFiles(directory=pdf_dir), name="pdfs")


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.environment,
    }


# Serve React frontend in production
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        """Serve the React SPA for any non-API route."""
        file_path = os.path.join(STATIC_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))
