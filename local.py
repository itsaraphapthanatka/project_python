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
source_path = "alistgdrive:/UPDATE3"
destination_path = "dospaces:/alist-spaces/UPDATE3"
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

# Convert image to .webp format
def convert_image_to_webp(source_image_path, webp_image_path):
    try:
        with Image.open(source_image_path) as img:
            img.save(webp_image_path, 'webp')
            print(f"Converted {source_image_path} to {webp_image_path}")
    except Exception as e:
        print(f"Failed to convert {source_image_path} to .webp: {e}")
local_file_path = f"./temp"  # Temporary local path


result = subprocess.run(["rclone", "lsf", f"{local_file_path}", "--files-only", "--recursive", '--progress'], capture_output=True, encoding="utf-8", text=True, shell=True)

# List files in the source path on Google Drive
# result = subprocess.run(["rclone", "lsf", source_path, "--files-only", "--recursive", '--progress'], capture_output=True, encoding="utf-8", text=True, shell=True)
# # download_result = subprocess.run(["rclone", "copy", f"{source_path}", local_file_path, '--progress'])
print(f"{result}\n")
# files = result.stdout.splitlines()

#     # Loop through each file
# for file_path in files:
#     if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
#         process = subprocess.Popen(
#             ["rclone", "copy", f"{source_path}", f"{local_file_path}", "--ignore-existing", "--progress"],
#             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", shell=True
#         )
#         try:
#         # Read output incrementally
#             for stdout_line in iter(process.stdout.readline, ""):
#                 print(stdout_line.strip())
#         except UnicodeDecodeError as e:
#             print(f"Error decoding output: {e}")
#         # Wait for the process to finish and get the return code
#         process.stdout.close()
#         return_code = process.wait()

#         if return_code == 0:
#             print("Copy operation successful.")
#         else:
#             print("Copy operation failed:", process.stderr.read())



if result.returncode != 0:
    print(f"Error: {result.stderr}")
else:
    files = result.stdout.splitlines()

    # Loop through each file
    for file_path in files:
        if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp','.JPG','.PNG')):  # Filter for image files
            folder_name = os.path.dirname(file_path)
            local_file_name = os.path.join("./temp", folder_name, os.path.basename(file_path))
            local_file_namen = os.path.basename(file_path)
            webp_file_name = os.path.splitext(local_file_namen)[0] + ".webp"
            webp_file_path = os.path.join("./web", folder_name, webp_file_name)
            os.makedirs(os.path.join("./web", folder_name), exist_ok=True)
            print(f"{webp_file_path}")
            
            # Convert to .webp
            convert_image_to_webp(local_file_name, webp_file_path)

            # Upload the .webp file to DigitalOcean Spaces
            destination_file_path = os.path.join(destination_path, folder_name)
          
            print(f"{destination_file_path}")
            copy_result = subprocess.run(["rclone", "copy", webp_file_path, destination_file_path,"--fast-list", "--ignore-existing",'--log-file=rclone.log', '--progress'],capture_output=True, encoding="utf-8", text=True, shell=True)

            if copy_result.returncode == 0:
                try:
                    # Generate a signed URL for the .webp file in DigitalOcean Spaces
                    signed_url = s3.generate_presigned_url('get_object',
                                                           Params={'Bucket': space_name, 'Key': f'API/{folder_name}/{webp_file_name}'},
                                                           ExpiresIn=94608000)  # Link expires in 3 years
                    data.append([folder_name, signed_url])
                except NoCredentialsError:
                    print("Credentials not available for DigitalOcean Spaces.")
            else:
                print(f"Failed to copy {webp_file_name} to DigitalOcean Spaces: {copy_result.stderr}")
            
            # Remove local files after processing
            if os.path.isfile(local_file_name):
                os.remove(local_file_name)
            else:
                print(f"Skipping removal: {local_file_name} is a directory")

            if os.path.isfile(webp_file_path):
                os.remove(webp_file_path)
            else:
                print(f"Skipping removal: {webp_file_path} is a directory")


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

# Function to list folders and images from DigitalOcean Spaces
def list_folders_and_images():
    folder_images = {}
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=space_name):
            if 'Contents' in page:
                for item in page['Contents']:
                    key = item['Key']
                    print(f"find---{key}")
                    # if key.lower().endswith('.webp'):  # Only process .webp files
                    if key.lower().endswith(('.png', '.jpg', '.jpeg', '.gif','.JPG','.PNG')):
                        folder_name = key.split('/')[-2]  # Extract last folder name
                        if folder_name not in folder_images:
                            folder_images[folder_name] = []
                        folder_images[folder_name].append(f"{Origin_Endpoint}/{key}")
                        set_public_permission(key)
    except s3.exceptions.ClientError as e:
        print(f"Client error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    return folder_images

# Export the data to CSV
def export_to_csv(data):
    with open('image_links.csv', 'w', newline='') as csvfile:
        fieldnames = ['Listing', 'Image Link']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        for folder, images in data.items():
            for image in images:
                writer.writerow([folder, image])

# # Main execution
# data = list_folders_and_images()

if data:
    for folder, images in data.items():
        for image in images:
            print(f"{folder}, {image}")
            
    export_to_csv(data)
else:
    print("No image files found in the folder.")
