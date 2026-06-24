from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://rag:rag@localhost:5432/ragdb"
    arxiv_download_dir: str = "./data/pdfs"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    min_score: float = 3.0
    arxiv_download_delay_seconds: float = 5.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
