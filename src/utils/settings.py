from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .env_utils import EnvUtils


class Settings(BaseSettings):
    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT", ge=1, le=65535)
    workers: int = Field(alias="WORKERS", ge=1)

    database_url: str = Field(alias="DATABASE_URL")
    database_schema: str = Field(alias="DATABASE_SCHEMA", default="public")
    job_store_database_schema: str = Field(alias="JOB_STORE_DATABASE_SCHEMA", default="public_job_store")

    # CORS Configuration - comma-separated list of allowed origins, or "*" for all
    cors_allowed_origins: str = Field(alias="CORS_ALLOWED_ORIGINS", default="*")

    sample_event_polling_backoff_initial_in_seconds: int = Field(
        alias="SAMPLE_EVENT_POLLING_BACKOFF_INITIAL_IN_SECONDS",
        ge=1
    )
    sample_event_polling_backoff_max_in_seconds: int = Field(
        alias="SAMPLE_EVENT_POLLING_BACKOFF_MAX_IN_SECONDS",
        ge=1
    )
    sample_job_frequency: str = Field(alias="SAMPLE_JOB_FREQUENCY")

    @field_validator('database_url')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v:
            raise ValueError('DATABASE_URL cannot be empty')
        if not v.startswith(('postgresql://', 'postgresql+psycopg://', 'postgresql+asyncpg://')):
            raise ValueError('DATABASE_URL must be a valid PostgreSQL connection string')
        return v

    @field_validator('sample_event_polling_backoff_max_in_seconds')
    @classmethod
    def validate_backoff(cls, v: int, info) -> int:
        initial = info.data.get('sample_event_polling_backoff_initial_in_seconds')
        if initial and v < initial:
            raise ValueError('Max backoff must be greater than or equal to initial backoff')
        return v

    model_config = SettingsConfigDict(
        env_file=EnvUtils.get_env_file_path(),
        extra="allow"
    )
