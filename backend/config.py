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
    mongodb_username: str = Field(default="")
    mongodb_password: str = Field(default="")
    mongodb_host: str = Field(default="localhost")
    mongodb_port: int = Field(default=27017)
    db_name: str = Field(default="podium_db")

    aws_access_key_id: str = Field(default=os.getenv("AWS_ACCESS_KEY_ID", None))
    aws_secret_access_key: str = Field(default=os.getenv("AWS_SECRET_ACCESS_KEY", None))
    aws_region: str = Field(default=os.getenv("AWS_REGION", None))
    s3_bucket_name: str = Field(default=os.getenv("S3_BUCKET_NAME", None))

    @property
    def mongodb_url(self) -> str:
        """Construct MongoDB URL with properly encoded credentials"""
        if self.mongodb_username and self.mongodb_password:
            encoded_username = urllib.parse.quote_plus(self.mongodb_username)
            encoded_password = urllib.parse.quote_plus(self.mongodb_password)
            url = f"mongodb://{encoded_username}:{encoded_password}@{self.mongodb_host}:{self.mongodb_port}"
        else:
            url = f"mongodb://{self.mongodb_host}:{self.mongodb_port}"
        print(f"MongoDB URL: {url}")
        return url

    model_config = SettingsConfigDict(
        extra = "allow",
        env_file = ".env",
        env_file_encoding = 'utf-8'
    )

@lru_cache()
def get_settings():
    return Settings()

