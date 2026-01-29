import pymysql

try:
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="grademate_db"
    )

    print("Database connection successful")

    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        db = cursor.fetchone()
        print("Connected to:", db[0])

except Exception as e:
    print(f"Connection failed: {e}")