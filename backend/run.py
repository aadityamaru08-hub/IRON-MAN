import sys
import os
import uvicorn

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.config import settings

if __name__ == "__main__":
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "app"))
    print(f"🚀 Starting BizForce AI backend on {settings.host}:{settings.port} (watching {app_dir})...")
    uvicorn.run("backend.app.main:app", host=settings.host, port=settings.port, reload=True, reload_dirs=[app_dir])
