import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "BizForce AI"
    version: str = "0.1.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    use_mock_db: bool = os.getenv("USE_MOCK_DB", "true").lower() in ("true", "1", "yes")

    @property
    def has_anthropic_key(self) -> bool:
        return bool(self.anthropic_api_key and self.anthropic_api_key.startswith("sk-"))

    @property
    def has_supabase_config(self) -> bool:
        return bool(self.supabase_url and self.supabase_key and not self.use_mock_db)

settings = Settings()
