import pandas as pd  # เพิ่มการนำเข้า pandas
import xlsxwriter  # เพิ่มการนำเข้า xlsxwriter

# บันทึกข้อมูลที่กรองแล้วลงในชีตใหม่

output_path = 'alist_.xlsx'
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    # สร้าง DataFrame ตัวอย่าง
    df = pd.DataFrame({
        'Column1': [1, 2, 3],
        'Image URL': ['url1', '', 'url3']
    })

    # กรองข้อมูลที่ Image URL ไม่ว่าง
    df_non_empty_image_url = df[df['Image URL'] != '']

    # เขียนข้อมูลต้นฉบับลงในชีตแรก
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    # เขียนข้อมูลที่กรองแล้ว (Image URL ที่ไม่ว่าง) ลงในชีตใหม่
    df_non_empty_image_url.to_excel(writer, sheet_name='Non_Empty_Image_URL', index=False)

print(output_path)  # เพิ่มการพิมพ์ output_path เพื่อแสดงผล
