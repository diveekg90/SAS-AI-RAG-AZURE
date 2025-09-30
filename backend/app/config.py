from pydantic import BaseSettings

class Settings(BaseSettings):
    search_endpoint: str
    search_index: str
    blob_account_url: str
    blob_container: str
    vision_endpoint: str
    vision_key: str
    aoai_endpoint: str
    aoai_key: str
    aoai_api_version: str = "2024-08-01-preview"
    aoai_chat_deployment: str = "gpt-35-turbo"
    aoai_embed_deployment: str = "text-embedding-3-small"

    class Config:
        env_file = ".env"

settings = Settings()
