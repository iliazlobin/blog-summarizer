import base64
import os

import boto3


def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name="us-east-1")

    response = client.get_secret_value(SecretId=secret_name)

    secret = None
    if "SecretString" in response:
        secret = response["SecretString"]
    else:
        secret = base64.b64decode(response["SecretBinary"])

    return secret


def get_secret_or_env(env):
    value = os.environ.get(env)

    if value.startswith("sm:"):
        secret_name = value[3:]
        secret_value = get_secret(secret_name)
        return secret_value

    return value
