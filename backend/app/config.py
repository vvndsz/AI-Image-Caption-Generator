from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    api_title: str = "AI Image Captioner API"
    api_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    
    # Model Settings
    model_name: str = "Salesforce/blip-image-captioning-large"
    device: str = "cuda"  # or "cpu"
    max_length: int = 50
    min_length: int = 10
    
    # OpenAI Settings (for tone adaptation)
    openai_api_key: Optional[str] = None
    use_openai_for_tone: bool = False
    
    # Redis Settings (for caching)
    redis_url: str = "redis://localhost:6379"
    cache_ttl: int = 3600  # 1 hour
    
    # CORS Settings
    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # File Upload Settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: set = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    
    class Config:
        env_file = ".env"

settings = Settings()