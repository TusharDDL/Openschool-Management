import os
import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status
from app.core.config import settings

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

async def upload_file_to_s3(file_path: str, bucket: str, object_name: str = None) -> str:
    """Upload a file to an S3 bucket

    :param file_path: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_path is used
    :return: URL of the uploaded file
    """
    # If S3 object_name was not specified, use file_path
    if object_name is None:
        object_name = os.path.basename(file_path)

    # Upload the file
    s3_client = get_s3_client()
    try:
        s3_client.upload_file(file_path, bucket, object_name)
    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file to S3: {str(e)}"
        )

    # Generate the URL for the uploaded file
    url = f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{object_name}"
    return url

async def delete_file_from_s3(bucket: str, object_name: str) -> None:
    """Delete a file from an S3 bucket

    :param bucket: Bucket name
    :param object_name: S3 object name
    """
    s3_client = get_s3_client()
    try:
        s3_client.delete_object(Bucket=bucket, Key=object_name)
    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file from S3: {str(e)}"
        )

async def generate_presigned_url(bucket: str, object_name: str, expiration=3600) -> str:
    """Generate a presigned URL to share an S3 object

    :param bucket: Bucket name
    :param object_name: S3 object name
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': object_name},
            ExpiresIn=expiration
        )
    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate presigned URL: {str(e)}"
        )

    return response