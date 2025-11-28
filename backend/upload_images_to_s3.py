"""
Upload user profile and cover images to S3 bucket
"""
import sys
import os
from pathlib import Path
import boto3
from botocore.exceptions import NoCredentialsError

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import get_settings

settings = get_settings()

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region
)

bucket_name = settings.s3_bucket_name

def upload_file_to_s3(file_path, s3_key, content_type='image/png'):
    """Upload a file to S3"""
    try:
        with open(file_path, 'rb') as file:
            s3_client.upload_fileobj(
                file,
                bucket_name,
                s3_key,
                ExtraArgs={'ContentType': content_type}
            )
        url = f"https://{bucket_name}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"
        print(f"✓ Uploaded: {s3_key}")
        return url
    except FileNotFoundError:
        print(f"✗ File not found: {file_path}")
        return None
    except NoCredentialsError:
        print("✗ AWS credentials not found")
        return None
    except Exception as e:
        print(f"✗ Error uploading {s3_key}: {e}")
        return None

def main():
    print("\n" + "="*70)
    print("UPLOADING USER IMAGES TO S3")
    print("="*70 + "\n")
    
    # Define image mappings: (local_file, s3_key, user_id, type)
    # Generated images from artifacts directory
    artifacts_dir = Path("C:/Users/ADMIN/.gemini/antigravity/brain/2966c4f7-bb7e-441e-a599-c9b38304b4a1")
    
    images = [
        # PV Sindhu
        (artifacts_dir / "pv_sindhu_profile_1764322380683.png", "profiles/athlete1_profile.png", "athlete1", "profile"),
        (artifacts_dir / "pv_sindhu_cover_1764322399284.png", "covers/athlete1_cover.png", "athlete1", "cover"),
        
        # Kento Momota
        (artifacts_dir / "kento_momota_profile_1764322414451.png", "profiles/athlete2_profile.png", "athlete2", "profile"),
        (artifacts_dir / "kento_momota_cover_1764322432460.png", "covers/athlete2_cover.png", "athlete2", "cover"),
        
        # An Se Young
        (artifacts_dir / "an_seyoung_profile_1764322449095.png", "profiles/athlete3_profile.png", "athlete3", "profile"),
    ]
    
    uploaded_urls = {}
    
    for file_path, s3_key, user_id, img_type in images:
        if file_path.exists():
            url = upload_file_to_s3(str(file_path), s3_key)
            if url:
                if user_id not in uploaded_urls:
                    uploaded_urls[user_id] = {}
                uploaded_urls[user_id][img_type] = url
        else:
            print(f"✗ Skipping {file_path.name} - file not found")
    
    print("\n" + "="*70)
    print("UPLOADED URLS")
    print("="*70 + "\n")
    
    for user_id, urls in uploaded_urls.items():
        print(f"{user_id}:")
        for img_type, url in urls.items():
            print(f"  {img_type}: {url}")
        print()
    
    print("\n✅ Upload process complete!")
    print(f"\nTotal images uploaded: {sum(len(urls) for urls in uploaded_urls.values())}")
    
    return uploaded_urls

if __name__ == "__main__":
    if not settings.aws_access_key_id or not settings.aws_secret_access_key:
        print("❌ ERROR: AWS credentials not configured!")
        print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in your .env file")
        sys.exit(1)
    
    main()
