import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='ferreira_guilherme_deva1a_notes_2025'
)

cursor = conn.cursor()

cursor.execute("SHOW TABLES;")
print("Connection successful. Tables listed above.")

cursor.close()
conn.close()
