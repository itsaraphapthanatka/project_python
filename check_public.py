import subprocess
import csv
import os
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.client import Config
from PIL import Image

# Configurations
google_drive_remote = "alistgdrive"
digitalocean_remote = "dospaces"
source_path = "alistgdrive:/UPDATE"
destination_path = "dospaces:/alist-spaces/UPDATE"
Origin_Endpoint = 'https://alist-spaces.sfo3.digitaloceanspaces.com'
csv_file = "output.csv"
space_name = "alist-spaces"
space_region = "sfo3"
access_key = "DO00PUFCPWTG2VABRCY3"
secret_key = "aD8eAQ9mOyiecF/CpRKe4Dl9aKNe+22KrIHMZJPS/2Q"

# Create a list to store data
data = []

# Initialize the S3 client for DigitalOcean Spaces
s3 = boto3.client(
    's3',
    region_name=space_region,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url=f'https://{space_region}.digitaloceanspaces.com',
    config=Config(signature_version='s3v4')
)

def check_public_private_count():
    public_count = 0
    private_count = 0

    try:
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=space_name, Prefix='UPDATE/'):
            if 'Contents' in page:
                for item in page['Contents']:
                    key = item['Key']
                    acl = s3.get_object_acl(Bucket=space_name, Key=key)
                    for grant in acl['Grants']:
                        if 'URI' in grant['Grantee'] and 'public-read' in grant['Permission']:
                            public_count += 1
                            break
                    else:
                        private_count += 1
    except s3.exceptions.ClientError as e:
        print(f"Client error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

    print(f"Public-read count: {public_count}")
    print(f"Private-read count: {private_count}")

# Call the function to check counts
check_public_private_count()