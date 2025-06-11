import mysql.connector
from datetime import datetime

def create_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="@n1meweebinthehouse"
    )
    cursor = conn.cursor()
    
    # Create database if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS pharmalook")
    cursor.execute("USE pharmalook")
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('admin', 'pharmacist', 'user') DEFAULT 'user',
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            phone_number VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)

    # Create pharmacies table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pharmacies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            address TEXT NOT NULL,
            city VARCHAR(100),
            state VARCHAR(100),
            zip_code VARCHAR(20),
            phone_number VARCHAR(20),
            email VARCHAR(255),
            license_number VARCHAR(100),
            admin_approved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)

    # Create medications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            generic_name VARCHAR(255),
            manufacturer VARCHAR(255),
            description TEXT,
            dosage_form VARCHAR(100),
            strength VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)

    # Create pharmacy_medications table (for inventory)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pharmacy_medications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pharmacy_id INT,
            medication_id INT,
            quantity INT NOT NULL DEFAULT 0,
            price DECIMAL(10,2),
            expiry_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id),
            FOREIGN KEY (medication_id) REFERENCES medications(id)
        )
    """)

    # Create prescriptions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            pharmacy_id INT,
            medication_id INT,
            dosage VARCHAR(100),
            frequency VARCHAR(100),
            duration VARCHAR(100),
            status ENUM('pending', 'approved', 'rejected', 'completed') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id),
            FOREIGN KEY (medication_id) REFERENCES medications(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database and tables created successfully!")

