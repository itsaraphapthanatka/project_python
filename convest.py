from PIL import Image
import os

def convert_png_to_webp(png_file_path, webp_file_path):
    # เปิดไฟล์ภาพ PNG
    img = Image.open(png_file_path)

    # แปลงและบันทึกเป็นไฟล์ WebP
    img.save(webp_file_path, 'webp')

    print(f"ไฟล์ถูกแปลงจาก {png_file_path} เป็น {webp_file_path} เรียบร้อยแล้ว.")

# ตัวอย่างการใช้งาน
png_file = 'a.png'  # ชื่อไฟล์ PNG
webp_file = 'a.webp'  # ชื่อไฟล์ที่ต้องการบันทึกเป็น WebP
convert_png_to_webp(png_file, webp_file)
