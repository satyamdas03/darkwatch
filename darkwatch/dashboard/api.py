"""FastAPI backend for the Darkwatch analyst dashboard."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .scanner import DEFAULT_DATA_DIR, find_scene, scan_scenes

REPO_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"


def create_app(data_dir: Path = DEFAULT_DATA_DIR) -> FastAPI:
    app = FastAPI(
        title="Darkwatch Dashboard",
        description="Analyst view for maritime dark-vessel detection.",
        version="0.1.0",
    )

    # Static frontend files
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def root() -> str:
        index_path = FRONTEND_DIR / "index.html"
        if not index_path.exists():
            raise HTTPException(status_code=404, detail="Dashboard frontend not built")
        return index_path.read_text(encoding="utf-8")

    @app.get("/api/scenes")
    async def list_scenes() -> JSONResponse:
        scenes = [s.to_dict() for s in scan_scenes(data_dir)]
        return JSONResponse({"scenes": scenes})

    @app.get("/api/scenes/{scene_id}")
    async def get_scene(scene_id: str) -> JSONResponse:
        scene = find_scene(scene_id, data_dir)
        if scene is None:
            raise HTTPException(status_code=404, detail=f"Scene {scene_id} not found")
        return JSONResponse(scene.to_dict())

    @app.get("/api/scenes/{scene_id}/map")
    async def get_scene_map(scene_id: str) -> HTMLResponse:
        scene = find_scene(scene_id, data_dir)
        if scene is None or not scene.map_html:
            raise HTTPException(status_code=404, detail=f"Map for {scene_id} not found")
        return HTMLResponse(content=scene.map_html)

    @app.get("/api/health")
    async def health() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    return app
