from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    Field
)
from functools import lru_cache
from typing import Optional
from dotenv import load_dotenv
import os
import urllib

load_dotenv()

class Settings(BaseSettings):
    mongodb_url: str = Field(default="")
    db_name: str = Field(default="podium_db")

    aws_access_key_id: str = Field(default=os.getenv("AWS_ACCESS_KEY_ID", None))
    aws_secret_access_key: str = Field(default=os.getenv("AWS_SECRET_ACCESS_KEY", None))
    aws_region: str = Field(default=os.getenv("AWS_REGION", None))
    s3_bucket_name: str = Field(default=os.getenv("S3_BUCKET_NAME", None))

    model_config = SettingsConfigDict(
        extra = "allow",
        env_file = ".env",
        env_file_encoding = 'utf-8'
    )

@lru_cache()
def get_settings():
    return Settings()

