import boto3
from botocore.client import Config
import csv

# กำหนดค่าการเชื่อมต่อ DigitalOcean Spaces
DO_ENDPOINT = 'https://sfo3.digitaloceanspaces.com'  # เปลี่ยนตามภูมิภาคของคุณ
Origin_Endpoint = 'https://alist-spaces.sfo3.digitaloceanspaces.com'  # Origin_Endpoint
DO_ACCESS_KEY = 'DO00PUFCPWTG2VABRCY3'  # ใส่คีย์ที่ถูกต้องของคุณ
DO_SECRET_KEY = 'aD8eAQ9mOyiecF/CpRKe4Dl9aKNe+22KrIHMZJPS/2Q'  # ใส่คีย์ที่ถูกต้องของคุณ
DO_SPACE_NAME = 'alist-spaces'
DO_SPACE_REGION = 'sfo3'  # ใส่ภูมิภาคของคุณ

# เริ่มต้นเซสชันด้วยข้อมูลรับรอง
session = boto3.session.Session()
client = session.client('s3',
                        region_name=DO_SPACE_REGION,
                        endpoint_url=DO_ENDPOINT,
                        aws_access_key_id=DO_ACCESS_KEY,
                        aws_secret_access_key=DO_SECRET_KEY,
                        config=Config(signature_version='s3v4'))

def set_public_permission(file_key):
    try:
        # Set the ACL of the object to public-read
        client.put_object_acl(
            Bucket=DO_SPACE_NAME,
            Key=file_key,
            ACL='public-read'
        )
        print(f"File {file_key} is now publicly accessible.")
    except Exception as e:
        print(f"Error setting public permission for {file_key}: {e}")


def list_folders_and_images():
    folder_images = {}
    error_folders = []
    try:
        paginator = client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=DO_SPACE_NAME):
            if 'Contents' in page:
                for item in page['Contents']:
                    key = item['Key']
                    if key.lower().endswith(('.webp')):
                        print(key)
                        # Extract folder name
                        folder_name = key.split('/')[1]  # Assuming folder name is the second part
                        if folder_name not in folder_images:
                            folder_images[folder_name] = []
                        folder_images[folder_name].append(f"{Origin_Endpoint}/{key}")
                        set_public_permission(key)
    except client.exceptions.ClientError as e:
        print(f"เกิดข้อผิดพลาดของลูกค้า: {e}")
        error_folders.append(folder_name)
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        error_folders.append(folder_name)
    return folder_images, error_folders

def export_to_csv(data):
    with open('image_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Listing', 'Image Link']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        for folder, images in data.items():
            for image in images:
                writer.writerow([folder, image])

# Get data
data, error_folders = list_folders_and_images()

if data:
    # แสดงลิงก์ของรูปภาพทั้งหมด
    for folder, images in data.items():
        for image in images:
            print(f"{folder}, {image}")

        # Export ข้อมูลเป็น CSV
        export_to_csv(data)
else:
    print("ไม่พบไฟล์รูปภาพในโฟลเดอร์นี้.")

if error_folders:
    print("โฟลเดอร์ที่เกิดข้อผิดพลาด:")
    for folder in error_folders:
        print(folder)