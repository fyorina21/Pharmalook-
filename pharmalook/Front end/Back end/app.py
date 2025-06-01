from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import jwt
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "your_strong_secret_key_here"  # Change this to a strong secret key

# Database connection function
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pharmalook",
            auth_plugin='mysql_native_password'  # Add this if using MySQL 8.0+
        )
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

# Signup Route
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password', '').encode('utf-8')
    role = data.get('role', 'pharmacist')  # Default role is pharmacist

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "User already exists"}), 409

        # Hash password and create user
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
            (email, hashed_password, role)
        )
        db.commit()
        
        return jsonify({
            "success": True,
            "message": "User registered successfully!",
            "role": role
        }), 201

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return jsonify({"error": "Registration failed"}), 500
        
    finally:
        cursor.close()
        db.close()

# Login Route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password', '').encode('utf-8')
    remember_me = data.get('rememberMe', False)

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, email, password, role FROM users WHERE email = %s", 
            (email,)
        )
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if bcrypt.checkpw(password, user['password'].encode('utf-8')):
            # Set token expiration (longer if remember_me is True)
            expires_in = timedelta(days=7) if remember_me else timedelta(hours=1)
            
            # Create JWT token
            token_payload = {
                "user_id": user['id'],
                "email": user['email'],
                "role": user['role'],
                "exp": datetime.utcnow() + expires_in
            }
            token = jwt.encode(
                token_payload,
                app.config["SECRET_KEY"],
                algorithm="HS256"
            )

            return jsonify({
                "success": True,
                "token": token,
                "role": user['role'],
                "expires_in": expires_in.total_seconds()
            }), 200
        else:
            return jsonify({"error": "Invalid password"}), 401

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Login failed"}), 500
        
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    

