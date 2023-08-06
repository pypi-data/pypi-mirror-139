# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/

import base64
import botocore
import os
import logging
import boto3
import re
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


# from settings import AWS_SECRETS_IMPLY_DRUID_CERTIFICATE, REGION_NAME
def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret


RE_S3PATH = re.compile('s3://([^/]+)/(.*)', re.IGNORECASE)


def split_s3_path(s3_path):
    """Split an S3 path in bucket and object

    :type s3_path: string
    :param s3_path: S3 path with bucket and key, e.g. 's3://bucket/key'

    :rtype: tuple of string
    :returns: The bucket and object as a tuple: (bucket, object)
    """
    # try to get components
    s3_match = RE_S3PATH.match(s3_path)

    # alert if the pattern did not match
    assert s3_match is not None, 'S3 path should be like: s3://bucket/object'

    # return
    bucket, key = s3_match.groups()
    return bucket, key


def download_from_s3(s3_path):
    bucket, key = split_s3_path(s3_path)
    try:
        if not os.path.exists('download'):
            os.makedirs('download')
        op_file_path = 'download/' + key.rsplit('/', 1)[1]
        boto3.resource('s3').Bucket(bucket).download_file(key, op_file_path)
        logger.info("file '" + s3_path + "' downloaded successfully at: " + op_file_path)
        return op_file_path
    except botocore.exceptions.ClientError as error:
        logger.error(error, exc_info=True)
        raise error
