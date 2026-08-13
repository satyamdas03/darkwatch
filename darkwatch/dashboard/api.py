"""FastAPI backend for the Darkwatch analyst dashboard."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from .scanner import DEFAULT_DATA_DIR, find_contact_thumbnail, find_scene, scan_scenes

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

    @app.get("/api/scenes/{scene_id}/contacts/{contact_id}/thumbnail")
    async def get_contact_thumbnail(scene_id: str, contact_id: str) -> FileResponse:
        scene = find_scene(scene_id, data_dir)
        if scene is None:
            raise HTTPException(status_code=404, detail=f"Scene {scene_id} not found")
        if not any(v["contact_id"] == contact_id for v in scene.verdicts):
            raise HTTPException(status_code=404, detail=f"Contact {contact_id} not in scene")
        thumb_path = find_contact_thumbnail(contact_id)
        if thumb_path is None or not thumb_path.exists():
            raise HTTPException(status_code=404, detail=f"Thumbnail for {contact_id} not found")
        return FileResponse(thumb_path, media_type="image/png")

    @app.get("/api/scenes/{scene_id}/export.csv")
    async def export_scene_csv(scene_id: str) -> StreamingResponse:
        import csv
        import io

        scene = find_scene(scene_id, data_dir)
        if scene is None:
            raise HTTPException(status_code=404, detail=f"Scene {scene_id} not found")

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "contact_id", "verdict", "p_artifact", "p_clear", "p_dark", "p_review",
            "center_lon", "center_lat", "width_m", "length_m", "detector_confidence",
            "n_tracks_within_gate", "nearest_mmsi", "nearest_distance_m", "static_object",
            "reasoning",
        ])

        contacts_by_id = {c["contact_id"]: c for c in scene.contacts}
        for v in scene.verdicts:
            c = contacts_by_id.get(v["contact_id"], {})
            assoc = v.get("nearest_association") or v.get("best_association") or {}
            static = v.get("static_object") or {}
            writer.writerow([
                v["contact_id"],
                v["verdict"],
                v["p_artifact"],
                v["p_clear"],
                v["p_dark"],
                v["p_review"],
                c.get("center_lon"),
                c.get("center_lat"),
                c.get("width_m"),
                c.get("length_m"),
                c.get("confidence"),
                v.get("n_tracks_within_gate"),
                assoc.get("mmsi"),
                assoc.get("distance_m"),
                static.get("name"),
                " ".join(v.get("reasoning") or []),
            ])

        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode("utf-8")),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={scene_id}_verdicts.csv"},
        )

    @app.get("/api/health")
    async def health() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    return app
