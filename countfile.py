import subprocess

def count_local_files(local_path):
    try:
        result = subprocess.run(["rclone", "lsf", local_path, "--files-only", "--recursive"], capture_output=True, encoding="utf-8", text=True, shell=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return 0
        files = result.stdout.splitlines()
        image_files = [file for file in files if file.endswith(('.jpg', '.png','.JPG'))]
        # print(image_files)
        import json
        # print(json.dumps({"file_count": len(image_files)}))
        return len(image_files)
    except Exception as e:
        print(f"Error counting local files: {e}")
        return 0

# Example usage
local_file_path = "./temp"
file_count = count_local_files(local_file_path)
import time

while file_count > 0:
    print(f"Remaining files: {file_count}")
    file_count = count_local_files(local_file_path)
    time.sleep(10)  # รอ 10 วินาทีก่อนตรวจสอบไฟล์อีกครั้ง
print("All files have been processed.")

