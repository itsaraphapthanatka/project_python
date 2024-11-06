import csv
import boto3
from botocore.client import Config
import pandas as pd

# Configurations
google_drive_remote = "alistgdrive"
digitalocean_remote = "dospaces"
source_path = "alistgdrive:/API"
destination_path = "dospaces:/alist-spaces/API"
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

def read_csv_and_match_links(csv_file_path):
    matched_links = []

    try:
        if csv_file_path.endswith('.xlsx'):
            df = pd.read_excel(csv_file_path)
            for index, row in df.iterrows():
                listing_code = row['Content']
                fave_property_id = row['fave_property_id']
                # Check if the link exists in DigitalOcean Spaces
                folder_images = {}
                error_folders = []
                try:
                    paginator = s3.get_paginator('list_objects_v2')
                    for page in paginator.paginate(Bucket=space_name):
                        if 'Contents' in page:
                            for item in page['Contents']:
                                key = item['Key']
                                if key.lower().endswith(('.webp')):
                                    folder_name = key.split('/')[-2]  # Extract folder name
                                    if folder_name == str(fave_property_id):
                                        if folder_name not in folder_images:
                                            folder_images[folder_name] = []
                                        folder_images[folder_name].append(f"{Origin_Endpoint}/{key}")
                except s3.exceptions.ClientError as e:
                    print(f"เกิดข้อผิดพลาดของลูกค้า: {e}")
                    error_folders.append(folder_name)
                except Exception as e:
                    print(f"เกิดข้อผิดพลาด: {e}")
                    error_folders.append(folder_name)
                matched_links.append((listing_code, folder_images))
                print(matched_links)
    except FileNotFoundError:
        print(f"File {csv_file_path} not found.")
    except Exception as e:
        print(f"Error reading file {csv_file_path}: {e}")

    return matched_links

def update_excel_with_links(excel_file_path, matched_links):
    try:
        df = pd.read_excel(excel_file_path)
        for index, row in df.iterrows():
            for listing_code, image_links in matched_links:
                if row['Content'] == listing_code:
                    # Combine all image links into a single string
                    image_url = ', '.join([link for links in image_links.values() for link in links])
                    df.at[index, 'Image URL'] = image_url
        df.to_excel(excel_file_path, index=False)
        print(f"Updated {excel_file_path} with image links.")
    except Exception as e:
        print(f"Error updating file {excel_file_path}: {e}")

# Example usage
csv_file_path = 'alist.xlsx'
matched_links = read_csv_and_match_links(csv_file_path)
if matched_links:
    update_excel_with_links(csv_file_path, matched_links)
else:
    print("No matching links found in the file.")