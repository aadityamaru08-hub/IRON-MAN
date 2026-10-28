"""Database gateway providing transparent access to Supabase or Mock Database fallback."""
from backend.app.config import settings
from backend.app.db.mock_db import mock_db

def get_db():
    """Return database client. Defaults to mock_db for hackathon speed and reliability."""
    if settings.has_supabase_config:
        try:
            # Placeholder for supabase-py client if user provides credentials
            pass
        except Exception:
            pass
    return mock_db
