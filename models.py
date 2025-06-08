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
                   admin_approved BOOLEAN DEFAULT FALSE,
               )
           """)


cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
               user_id INT AUTO_INCREMENT PRIMARY KEY,
               email VARCHAR(255) UNIQUE NOT NULL,
               password VARCHAR(255) NOT NULL,
               role ENUM('admin', 'pharmacist', 'user') DEFAULT 'user',
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)



conn.commit()
conn.close()

