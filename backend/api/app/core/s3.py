from typing import Optional, BinaryIO
import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from app.core.config import Config

class S3Client:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.s3_client = boto3.client(
                's3',
                endpoint_url=Config.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                region_name=Config.AWS_REGION
            )
            self.bucket_name = Config.AWS_S3_BUCKET_NAME
            self._ensure_bucket_exists()
            self._initialized = True

    def _ensure_bucket_exists(self) -> None:
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            self.s3_client.create_bucket(Bucket=self.bucket_name)

    def upload_file(self, file_obj: BinaryIO, object_name: str, content_type: Optional[str] = None) -> str:
        """
        Upload a file to S3/MinIO
        
        Args:
            file_obj: File object to upload
            object_name: Name to give the file in the bucket
            content_type: Optional MIME type of the file
        
        Returns:
            str: URL of the uploaded file
        """
        try:
            extra_args = {'ContentType': content_type} if content_type else {}
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                object_name,
                ExtraArgs=extra_args
            )
            
            # Generate URL for the uploaded file
            url = self.get_file_url(object_name)
            return url
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

    def get_file_url(self, object_name: str, expires_in: int = 3600) -> str:
        """
        Get a presigned URL for an object
        
        Args:
            object_name: Name of the file in the bucket
            expires_in: URL expiration time in seconds (default: 1 hour)
        
        Returns:
            str: Presigned URL for the file
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")

    def delete_file(self, object_name: str) -> bool:
        """
        Delete a file from the bucket
        
        Args:
            object_name: Name of the file to delete
            
        Returns:
            bool: True if deletion was successful
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_name
            )
            return True
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

    def check_file_exists(self, object_name: str) -> bool:
        """
        Check if a file exists in the bucket
        
        Args:
            object_name: Name of the file to check
            
        Returns:
            bool: True if file exists
        """
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=object_name
            )
            return True
        except ClientError:
            return False