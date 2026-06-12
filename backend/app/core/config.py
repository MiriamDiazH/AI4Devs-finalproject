from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://auditcare:auditcare@localhost:5432/auditcare"
    statewave_url: str = "http://localhost:8100"
    statewave_timeout_seconds: float = 20.0
    statewave_episode_path: str = "/v1/episodes"
    statewave_compile_path: str = "/v1/memories/compile"
    statewave_context_path: str = "/v1/context"
    statewave_llm_complete_path: str = "/v1/llm/complete"
    statewave_subject_prefix: str = "patient"
    statewave_context_max_tokens: int = 1800
    statewave_extraction_temperature: float = 0.2
    statewave_extraction_max_tokens: int = 1200

    class Config:
        env_file = ".env"


settings = Settings()
