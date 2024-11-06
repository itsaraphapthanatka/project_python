import subprocess
import csv
import os
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.client import Config

# Configurations
google_drive_remote = "alistgdrive"
digitalocean_remote = "dospaces"
source_path = "alistgdrive:API/"
destination_path = "dospaces:/alist-spaces/API"
Origin_Endpoint = 'https://alist-spaces.sfo3.digitaloceanspaces.com'  # Origin_Endpoint
space_name = "alist-spaces"  # Name of your DigitalOcean space
space_region = "sfo3"  # Region of your space
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



# List files in the source path on Google Drive
result = subprocess.run(["rclone", "lsf", source_path, "--files-only", "--recursive"], capture_output=True, encoding="utf-8", text=True, shell=True)
print(f"{result}")
# copy_result = subprocess.run(
#     ["rclone", "copy", f"{source_path}", f"{destination_path}", "-P"],
#     capture_output=True,  # Capture stdout and stderr
#     text=True,            # Return output as string (text mode)
#     shell=True            # Required for Windows
# )
# # Check if the command was successful
# if copy_result.returncode == 0:
#     print("Copy operation successful:")
#     print(copy_result.stdout)  # Print rclone's output
# else:
#     print("Copy operation failed:")
#     print(copy_result.stderr)  # Print the error output

# # Check for errors
# if result.returncode != 0:
#     print(f"Error: {result.stderr}")
# else:
#     files = result.stdout.splitlines()
#     print(f"{files}")
#     # Loop through each file
#     for file_path in files:
#         print(f"{file_path}")
#         if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # Filter for JPG files
#             folder_name = os.path.dirname(file_path).split("/")[-1]
#             destination_file_path = f"{destination_path}/{folder_name}/{os.path.basename(file_path)}"

#         try:
#             # Generate a signed URL for the file in DigitalOcean Spaces
#             signed_url = s3.generate_presigned_url('get_object',
#                                                     Params={'Bucket': space_name, 'Key': f'API/{folder_name}/{os.path.basename(file_path)}'},
#                                                     ExpiresIn=94608000)  # Link expires in 3 year
#             data.append([folder_name, signed_url])
#         except NoCredentialsError:
#             print("Credentials not available for DigitalOcean Spaces.")
            

# def list_folders_and_images():
#     folder_images = {}
#     try:
#         paginator = s3.get_paginator('list_objects_v2')
#         for page in paginator.paginate(Bucket=space_name):
#             if 'Contents' in page:
#                 for item in page['Contents']:
#                     key = item['Key']
#                     if key.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
#                         # Extract folder name
#                         folder_name = key.split('/')[1]  # Assuming folder name is the second part
#                         if folder_name not in folder_images:
#                             folder_images[folder_name] = []
#                         folder_images[folder_name].append(f"{Origin_Endpoint}/{key}")
#     except s3.exceptions.ClientError as e:
#         print(f"เกิดข้อผิดพลาดของลูกค้า: {e}")
#     except Exception as e:
#         print(f"เกิดข้อผิดพลาด: {e}")
#     return folder_images

# def export_to_csv(data):
#     with open('image_links.csv', 'w', newline='') as csvfile:
#         fieldnames = ['Listing', 'Image Link']
#         writer = csv.writer(csvfile)
#         writer.writerow(fieldnames)

#         for folder, images in data.items():
#             for image in images:
#                 writer.writerow([folder, image])

# # Get data
# data = list_folders_and_images()


# if data:
#     # แสดงลิงก์ของรูปภาพทั้งหมด
#     for folder, images in data.items():
#         for image in images:
#             print(f"{folder}, {image}")

#         # Export ข้อมูลเป็น CSV
#         export_to_csv(data)
# else:
#     print("ไม่พบไฟล์รูปภาพในโฟลเดอร์นี้.")
