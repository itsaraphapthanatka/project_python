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
destination_path = "dospaces:/alist-spaces/Update3"
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




def set_public_permission(file_key):
    try:
        # Set the ACL of the object to public-read
        s3.put_object_acl(
            Bucket=space_name,
            Key=file_key,
            ACL='public-read'
        )
        print(f"File {file_key} is now publicly accessible.")
    except Exception as e:
        print(f"Error setting public permission for {file_key}: {e}")

# Function to list folders and images from DigitalOcean Spaces path Update3
def list_folders_and_images_from_update3():
    folder_images = {}
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=space_name, Prefix='Update3/'):
            if 'Contents' in page:
                for item in page['Contents']:
                    key = item['Key']
                    print(f"find---{key}")
                    if key.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.JPG', '.PNG')):
                        folder_name = key.split('/')[-2]  # Extract folder name
                        if folder_name not in folder_images:
                            folder_images[folder_name] = []
                        folder_images[folder_name].append(f"{Origin_Endpoint}/{key}")
                        set_public_permission(key)
    except s3.exceptions.ClientError as e:
        print(f"Client error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    return folder_images

list_folders_and_images_from_update3();