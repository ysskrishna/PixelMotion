from typing import BinaryIO
import boto3
from botocore.exceptions import ClientError
from pm_common.core.config import BaseConfig

class S3Client:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
            cls._config = BaseConfig()
        return cls._instance

    def __init__(self):
        if not self._initialized:
            # Validate s3 config variables
            self._config.validate_s3_config()

            self.client = boto3.client(
                's3',
                endpoint_url=self._config.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=self._config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self._config.AWS_SECRET_ACCESS_KEY,
                region_name=self._config.AWS_REGION
            )
            self.bucket_name = self._config.AWS_S3_BUCKET_NAME
            self.endpoint_url = self._config.AWS_S3_ENDPOINT_URL
            self.public_endpoint_url = self._config.AWS_S3_PUBLIC_ENDPOINT_URL
            self._ensure_bucket_exists()
            self._initialized = True

    def _ensure_bucket_exists(self) -> None:
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            self.client.create_bucket(Bucket=self.bucket_name)
    

    def upload_fileobj(self, file_obj: BinaryIO, object_name: str, extra_args: dict = {}) -> str:
        """
        Upload a file to S3/MinIO
        
        Args:
            file_obj: File object to upload
            object_name: Name to give the file in the bucket
            extra_args: Extra arguments to pass to the upload_fileobj method
        
        Returns:
            str: URL of the uploaded file
        """
        self.client.upload_fileobj(
            file_obj,
            self.bucket_name,
            object_name,
            ExtraArgs=extra_args
        )
        
        return object_name

    def get_object(self, object_name: str) -> dict:
        """
        Get an object from S3/MinIO
        
        Args:
            object_name: Name of the file in the bucket
            
        Returns:
            dict: Response containing the object data and metadata
        """
        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=object_name
        )
        return response

    def download_file(self, object_name: str, file_path: str) -> bool:
        """
        Download a file from S3/MinIO to a local path
        
        Args:
            object_name: Name of the file in the bucket
            file_path: Local path where the file should be saved
        """
        self.client.download_file(
            self.bucket_name,
            object_name,
            file_path
        )

    def get_file_url(self, object_name: str, expires_in: int = 3600) -> str:
        """
        Get a presigned URL for an object
        
        Args:
            object_name: Name of the file in the bucket
            expires_in: URL expiration time in seconds (default: 1 hour)
        
        Returns:
            str: Presigned URL for the file
        """
        url = self.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': object_name
            },
            ExpiresIn=expires_in
        )
        url = url.replace(self.endpoint_url, self.public_endpoint_url)
        return url

    def delete_file(self, object_name: str) -> bool:
        """
        Delete a file from the bucket
        
        Args:
            object_name: Name of the file to delete
            
        Returns:
            bool: True if deletion was successful
        """
        self.client.delete_object(
            Bucket=self.bucket_name,
            Key=object_name
        )
        return True

    def check_file_exists(self, object_name: str) -> bool:
        """
        Check if a file exists in the bucket
        
        Args:
            object_name: Name of the file to check
            
        Returns:
            bool: True if file exists
        """
        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=object_name
            )
            return True
        except ClientError:
            return False

    def upload_file(self, file_path: str, object_name: str, extra_args: dict = {}) -> str:
        """
        Upload a file from a local path to S3/MinIO
        
        Args:
            file_path: Local path of the file to upload
            object_name: Name to give the file in the bucket
            extra_args: Extra arguments to pass to the upload_file method
        
        Returns:
            str: URL of the uploaded file
        """        
        try:
            self.client.upload_file(
                file_path,
                self.bucket_name,
                object_name,
                ExtraArgs=extra_args
            )
            return object_name
        except ClientError as e:
            raise Exception(f"Failed to upload file {file_path} to {object_name}: {str(e)}")