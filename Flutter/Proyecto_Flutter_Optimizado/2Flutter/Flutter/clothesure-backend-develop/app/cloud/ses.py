import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SES_SENDER = os.getenv("SES_SENDER") 

ses_client = boto3.client("ses", region_name=AWS_REGION)

class SESService:
    def __init__(self, sender: str = SES_SENDER, region: str = AWS_REGION):
        self.ses = boto3.client("ses", region_name=region)
        self.sender = sender

    def send_email(self, recipient: str, subject: str, html_body: str, text_body: str = "") -> dict:
        """
        Envía un correo desde SES.
        """
        try:
            response = self.ses.send_email(
                Source=self.sender,
                Destination={
                    "ToAddresses": [recipient],
                },
                Message={
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": {
                        "Text": {"Data": text_body or "Ver este correo en HTML.", "Charset": "UTF-8"},
                        "Html": {"Data": html_body, "Charset": "UTF-8"},
                    },
                },
            )
            return response

        except ClientError as e:
            raise Exception(f"Error enviando correo con SES: {str(e)}")
