import boto3
import os
from fastapi import UploadFile
from botocore.exceptions import NoCredentialsError, ClientError

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("AWS_S3_BUCKET")

s3_client = boto3.client("s3")

#mover a s3service
def upload_file_to_s3(file: UploadFile, key: str, content_type: str = "image/jpeg") -> str:
    try:
        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET,
            key,
            ExtraArgs={
            "ACL": "public-read",  
            "ContentType": content_type
        }
        )

        return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{key}"

    except NoCredentialsError:
        raise RuntimeError("AWS credentials not found.")
    except ClientError as e:
        raise RuntimeError(f" Failed to upload file to S3: {e}")

def delete_file_from_s3(object_key: str) -> bool:
    try:
        s3_client.delete_object(Bucket=S3_BUCKET, Key=object_key)
        return True
    except Exception as e:
        print(f"Error deleting file from S3: {e}")
        return False

class S3Service:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket_name = S3_BUCKET

    def create_album_folder(self, event_id: int, album_id: int):
        folder_key = ""
        #Crea un folder vacío en S3 para el álbum.
        folder_key = f"events/{event_id}/album/{album_id}/"
        try:
            self.s3.put_object(Bucket=self.bucket_name, Key=folder_key)
            return folder_key
        except ClientError as e:
            raise Exception(f"Error creando carpeta en S3: {str(e)}")

    def upload_photo(self, file, file_key):
        #Sube una foto a S3 y retorna la URL.
        try:
            self.s3.upload_fileobj(file.file, self.bucket_name, file_key, ExtraArgs={"ACL": "public-read", "ContentType": file.content_type})
            return f"https://{self.bucket_name}.s3.amazonaws.com/{file_key}"
        except ClientError as e:
            raise Exception(f"Error subiendo foto: {str(e)}")    
        
    def delete_file_from_s3(self, object_key: str) -> bool:
        try:
            s3_client.delete_object(Bucket=S3_BUCKET, Key=object_key)
            return True
        except Exception as e:
            print(f"Error deleting file from S3: {e}")
            return False
        