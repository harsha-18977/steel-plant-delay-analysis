import mysql.connector

connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password="vardhansql@004",
    database="steel_delay_analysis"
)

cursor=connection.cursor()

cursor.execute("SELECT COUNT(*) FROM delay_records")

result=cursor.fetchone()

print(result)

connection.close()