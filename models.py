import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="@n1meweebinthehouse",
    database="pharmalook"
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS pharmalook")
cursor.execute("USE pharmalook")

cursor.execute("""
               CREATE TABLE IF NOT EXISTS pharmacies (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   name VARCHAR(255) NOT NULL,
                   location VARCHAR(255),
                   admin_approved BOOLEAN DEFAULT FALsE,
               )
           """)



conn.commit()
conn.close()

