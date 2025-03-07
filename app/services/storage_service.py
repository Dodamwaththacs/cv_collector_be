import boto3
from app.config import Config

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=Config.AWS_ACCESS_KEY,
    aws_secret_access_key=Config.AWS_SECRET_KEY,
    region_name=Config.S3_REGION
)

def upload_file_to_s3(file_path, s3_key):
    """Uploads a file to S3."""
    try:
        with open(file_path, "rb") as file:
            s3.upload_fileobj(
                file,
                Config.S3_BUCKET,
                s3_key
            )
        print(f"File uploaded to S3: {s3_key}")
        return f"https://{Config.S3_BUCKET}.s3.{Config.S3_REGION}.amazonaws.com/{s3_key}"
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None