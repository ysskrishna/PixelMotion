from typing import Set
import os

class BaseConfig:
    # Define required variables for each service type
    REQUIRED_S3_VARS = {
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_S3_BUCKET_NAME',
        'AWS_S3_ENDPOINT_URL',
        'AWS_REGION'
    }
    
    REQUIRED_REDIS_VARS = {
        'REDIS_HOST',
        'REDIS_PORT'
    }

    def __init__(self):
        # Load environment variables during class definition
        for var in self.REQUIRED_S3_VARS | self.REQUIRED_REDIS_VARS:
            setattr(self, var, os.getenv(var))
        
        # Convert REDIS_PORT to int if present
        if self.REDIS_PORT:
            self.REDIS_PORT = int(self.REDIS_PORT)

    def validate_required_vars(self, required_vars: Set[str]):
        """
        Validate that required variables are present
        
        Args:
            required_vars: Set of variable names that must be present
        
        Raises:
            ValueError: If any required variable is missing
        """
        missing_vars = [
            var for var in required_vars
            if getattr(self, var, None) is None
        ]
        if missing_vars:
            raise ValueError(
                f"Missing required configuration variables: {', '.join(missing_vars)}"
            )

    def validate_s3_config(self):
        """Validate S3 configuration"""
        self.validate_required_vars(self.REQUIRED_S3_VARS)

    def validate_redis_config(self):
        """Validate Redis configuration"""
        self.validate_required_vars(self.REQUIRED_REDIS_VARS)