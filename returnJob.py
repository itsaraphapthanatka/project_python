import mysql.connector
from mysql.connector import Error
# import time

# Function to fetch data from a table
def select_from_table():
    try:
        connection = mysql.connector.connect(
            host='localhost',           # e.g., 'localhost'
            database='essilor',   # e.g., 'test_db'
            user='root',       # e.g., 'root'
            password=''    # e.g., 'password123'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT * FROM jobtask WHERE DATE_FORMAT(callJabdate, '%Y-%m-%d %H:%i') <= DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i') - INTERVAL 10 MINUTE AND jobStatus = 2"  # Replace with your actual table name
            try:
                cursor.execute(query)
                records = cursor.fetchall()
                for task in records:
                    # ทำการคืนงานหรืออัปเดตสถานะที่ต้องการ
                    update_query = "UPDATE jobtask SET jobStatus = 1, calljob = NULL, calluser = NULL WHERE id = %s"
                    cursor.execute(update_query, (task[0],))
                    connection.commit()
                    # บันทึกการคืนงานลงใน log
                    print(f"Returned job ID: {task[0]}")  # เพิ่มบันทึก log
            except Error as e:
                print(f"เกิดข้อผิดพลาดขณะดำเนินการคืนงาน: {e}")
                connection.rollback()  # ถอยกลับหากเกิดข้อผิดพลาด

            # Print the fetched records
            print("Total number of rows:", cursor.rowcount)
            for row in records:
                print(row)

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# # Call the function to run the select query
# while True:
#     select_from_table()
#     time.sleep(10)  # รอ 10 วินาที ก่อนที่จะทำซ้ำ
