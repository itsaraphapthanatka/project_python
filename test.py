import boto3
from botocore.client import Config

# กำหนดค่าการเชื่อมต่อ DigitalOcean Spaces
DO_ENDPOINT = 'https://sfo3.digitaloceanspaces.com'
DO_ACCESS_KEY = 'DO00PUFCPWTG2VABRCY3'  # ตรวจสอบคีย์ที่ถูกต้อง
DO_SECRET_KEY = 'aD8eAQ9mOyiecF/CpRKe4Dl9aKNe+22KrIHMZJPS/2Q'  # ตรวจสอบคีย์ที่ถูกต้อง
DO_SPACE_NAME = 'alist-spaces'
DO_SPACE_REGION = 'sfo3'

# เริ่มต้นเซสชันด้วยข้อมูลรับรอง
session = boto3.session.Session()
client = session.client('s3',
                        region_name=DO_SPACE_REGION,
                        endpoint_url=DO_ENDPOINT,
                        aws_access_key_id=DO_ACCESS_KEY,
                        aws_secret_access_key=DO_SECRET_KEY,
                        config=Config(signature_version='s3v4'))  # ใช้ signature v4

# ฟังก์ชันในการแสดงรายการไฟล์ทั้งหมด
def list_all_files():
    try:
        paginator = client.get_paginator('list_objects_v2')
        files = []  # เก็บรายการไฟล์ทั้งหมด
        for page in paginator.paginate(Bucket=DO_SPACE_NAME):
            if 'Contents' in page:
                for obj in page['Contents']:
                    files.append(obj['Key'])
            else:
                print("ไม่พบไฟล์ใน Space นี้.")
    except client.exceptions.ClientError as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    return files

# เรียกใช้ฟังก์ชันเพื่อแสดงรายการไฟล์ทั้งหมด
files = list_all_files()

if files:
    print("รายการไฟล์ทั้งหมด:")
    for file in files:
        print(file)
else:
    print("ไม่พบไฟล์ใด ๆ.")
