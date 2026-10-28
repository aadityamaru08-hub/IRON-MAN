import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.config import settings
from backend.app.api.routes_health import router as health_router
from backend.app.api.routes_leads import router as leads_router
from backend.app.api.routes_workflows import router as workflows_router
from backend.app.api.routes_approvals import router as approvals_router
from backend.app.db.sqlite_db import init_db

# Initialize SQLite database schema and seed data
init_db()

app = FastAPI(
    title="BizForce AI Backend",
    description="Multi-agent AI automation engine for CRM, lead qualification, and outreach workflows.",
    version=settings.version
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount endpoints at root (/health, /leads, /workflows, /approvals)
app.include_router(health_router)
app.include_router(leads_router)
app.include_router(workflows_router)
app.include_router(approvals_router)

# Also mount endpoints with /api prefix for frontend
app.include_router(health_router, prefix="/api")
app.include_router(leads_router, prefix="/api")
app.include_router(workflows_router, prefix="/api")
app.include_router(approvals_router, prefix="/api")

# Serve React frontend if dist directory exists (Render production mode)
# Works whether the app is started from /opt/render/project/src or local project root
_repo_root = os.environ.get("RENDER_PROJECT_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
DIST_DIR = os.path.join(_repo_root, "frontend", "dist")
ASSETS_DIR = os.path.join(DIST_DIR, "assets")

if os.path.exists(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.get("/{full_path:path}")
def serve_spa(full_path: str):
    """Catch-all to serve index.html for SPA routing, or API info if dist not built."""
    index_file = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "message": "BizForce AI Multi-Agent API is running with SQLite storage",
        "endpoints": {
            "health": "/health",
            "leads": "/leads",
            "run_workflow": "/workflows/run",
            "approvals": "/approvals",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", settings.port))
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=port)
