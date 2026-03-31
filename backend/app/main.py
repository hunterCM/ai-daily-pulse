import logging
from contextlib import asynccontextmanager
from pathlib import Path
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

BASE_DIR = Path(__file__).resolve().parent.parent


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

pdf_dir = BASE_DIR / "pdfs"
pdf_dir.mkdir(exist_ok=True)
app.mount("/pdfs", StaticFiles(directory=str(pdf_dir)), name="pdfs")

STATIC_DIR = BASE_DIR / "static"
INDEX_FILE = STATIC_DIR / "index.html"
ASSETS_DIR = STATIC_DIR / "assets"


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.environment,
    }


if ASSETS_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


@app.get("/{full_path:path}")
async def serve_spa(request: Request, full_path: str):
    if not INDEX_FILE.is_file():
        return {
            "app": "AI Daily Pulse",
            "status": "running",
            "message": "API is live. Frontend not built yet — visit /api/health or /docs",
        }
    if full_path:
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
    return FileResponse(str(INDEX_FILE))
