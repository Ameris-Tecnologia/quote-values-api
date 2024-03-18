"""Module to access AWS client"""

import os

import boto3
from botocore.exceptions import ClientError


AWS_SECRETS_ACCESS_KEY_ID = os.environ.get("AWS_SECRETS_ACCESS_KEY_ID")
AWS_SECRETS_ACCESS_KEY = os.environ.get("AWS_SECRETS_ACCESS_KEY")


class AWS():
    """Class AWS client"""

    @staticmethod
    def create_session_secretsmanager():
        """Function for create session secret-manager"""
        region_name = "us-east-1"
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
            aws_access_key_id=AWS_SECRETS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRETS_ACCESS_KEY
        )
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

    @staticmethod
    def update_secret(client, secret_name, updated_secret):
        """Function for update secret"""

        response = client.update_secret(
            SecretId=secret_name,
            SecretString=updated_secret
        )

        print(response)
