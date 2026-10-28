from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Enable CORS for Vite frontend development (supporting ports 5173, 5174, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount endpoints at root (/health, /leads, /workflows, /approvals)
app.include_router(health_router)
app.include_router(leads_router)
app.include_router(workflows_router)
app.include_router(approvals_router)

# Also mount endpoints with /api prefix for Vite frontend proxy
app.include_router(health_router, prefix="/api")
app.include_router(leads_router, prefix="/api")
app.include_router(workflows_router, prefix="/api")
app.include_router(approvals_router, prefix="/api")

@app.get("/")
def root():
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
    uvicorn.run("backend.app.main:app", host=settings.host, port=settings.port, reload=True)
