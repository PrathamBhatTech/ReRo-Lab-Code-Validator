import yaml

import boto3
from botocore.exceptions import NoCredentialsError

# Read AWS credentials from environment variables
with open('../config/config.yaml', 'r') as yaml_file:
    config_data = yaml.safe_load(yaml_file)

# Extract values from the config data
aws_access_key = config_data['aws_credentials']['aws_access_key_id']
aws_secret_key = config_data['aws_credentials']['aws_secret_access_key']

bucket_name = config_data['s3_settings']['aws_bucket_name']
prefix = config_data['s3_settings']['prefix']

local_file_path = config_data['local_settings']['local_file_path']

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)


def get_latest_object():
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
    objects = response.get('Contents', [])
    if objects:
        latest_object = max(objects, key=lambda obj: obj['LastModified'])
        return latest_object
    return None


def download_latest_file():
    latest_object = get_latest_object()

    if latest_object:
        object_key = latest_object['Key']

        try:
            s3.download_file(bucket_name, object_key, local_file_path)
            print(f"Latest file downloaded: {object_key} -> {local_file_path}")
            return f"{local_file_path}/{object_key}"
        except NoCredentialsError:
            print("AWS credentials not available or invalid.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No files found in the specified prefix.")
