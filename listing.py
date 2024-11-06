import boto3
from botocore.client import Config

# กำหนดค่าการเชื่อมต่อ DigitalOcean Spaces
DO_ENDPOINT = 'https://sfo3.digitaloceanspaces.com'  # ใส่ endpoint ที่ถูกต้อง
DO_ACCESS_KEY = 'DO00PUFCPWTG2VABRCY3'  # ใส่ access key ของคุณ
DO_SECRET_KEY = 'aD8eAQ9mOyiecF/CpRKe4Dl9aKNe+22KrIHMZJPS/2Q'  # ใส่ secret key ของคุณ
DO_SPACE_NAME = 'alist-spaces'  # ใส่ชื่อ space ของคุณ
DO_SPACE_REGION = 'sfo3'  # ใส่ region ของ space

# เริ่มต้นเซสชันด้วยข้อมูลรับรอง
session = boto3.session.Session()
client = session.client('s3',
                        region_name=DO_SPACE_REGION,
                        endpoint_url=DO_ENDPOINT,
                        aws_access_key_id=DO_ACCESS_KEY,
                        aws_secret_access_key=DO_SECRET_KEY,
                        config=Config(signature_version='s3v4'))

# ฟังก์ชันในการแสดงรายการโฟลเดอร์ทั้งหมดภายใต้โฟลเดอร์ Listing
def list_all_objects():
    try:
        response = client.list_objects_v2(Bucket=DO_SPACE_NAME, Prefix='Listing/')
        if 'Contents' in response:
            for obj in response['Contents']:
                print(obj['Key'])
        else:
            print("ไม่พบวัตถุใด ๆ ภายใต้โฟลเดอร์ Listing.")
    except client.exceptions.ClientError as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")




# เรียกใช้ฟังก์ชันเพื่อแสดงรายการโฟลเดอร์
folders = list_all_objects()

if folders:
    print("รายการโฟลเดอร์ทั้งหมดภายใต้ Listing:")
    for folder in folders:
        print(folder)
else:
    print("ไม่พบโฟลเดอร์ใด ๆ.")
