import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile, HTTPException
from backend.app.core.config import get_settings
import uuid
import os

settings = get_settings()

class Storage:
    def __init__(self):
        # Only initialize S3 client if credentials are provided
        if settings.aws_access_key_id and settings.aws_secret_access_key:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region
            )
            self.bucket_name = settings.s3_bucket_name
            self.enabled = True
        else:
            self.s3_client = None
            self.bucket_name = None
            self.enabled = False

    def upload_file(self, file: UploadFile, folder: str = "uploads", custom_filename: str = None) -> str:
        if not self.enabled:
            raise HTTPException(
                status_code=503,
                detail="S3 storage is not configured. Please set AWS credentials in .env file."
            )
        
        try:
            # Use custom filename if provided, otherwise generate UUID
            if custom_filename:
                filename = f"{folder}/{custom_filename}"
            else:
                file_extension = os.path.splitext(file.filename)[1]
                filename = f"{folder}/{uuid.uuid4()}{file_extension}"
            
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                filename,
                ExtraArgs={'ContentType': file.content_type}
            )
            
            # Construct public URL
            url = f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{filename}"
            return url
        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="AWS Credentials not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

storage = Storage()
