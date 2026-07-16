from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    hf_token: str = ""
    groq_api_key: str = ""
    llm_provider: str = "groq"
    model_name: str = "qwen-2.5-32b"
    temperature: float = 0.2
    max_new_tokens: int = 512
    top_k: int = 5
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
