"""Module to access AWS client"""

import json
import boto3
from botocore.exceptions import ClientError
from settings import get_settings


AWS_SECRETS_ACCESS_KEY_ID = get_settings().AWS_SECRETS_ACCESS_KEY_ID
AWS_SECRETS_ACCESS_KEY = get_settings().AWS_SECRETS_ACCESS_KEY


class AWS():
    """Class AWS client"""

    @staticmethod
    def create_session_secretsmanager():
        """Function for create session secret-manager"""
        region_name = "us-east-1"
        # Create a Secrets Manager client
        session = boto3.Session(
            region_name=region_name,
            aws_access_key_id=AWS_SECRETS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRETS_ACCESS_KEY
        )
        client = session.client(service_name='secretsmanager')
        return client

    @staticmethod
    def get_secret(client, secret_name):
        """Function for get secret"""

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response['SecretString']

        # Your code goes here.
        return secret


def get_secret_from_str(secret_name: str):
    """Function for get secret from secret name"""
    secrets = json.loads(AWS.get_secret(
        AWS.create_session_secretsmanager(),
        secret_name)
    )
    return secrets
