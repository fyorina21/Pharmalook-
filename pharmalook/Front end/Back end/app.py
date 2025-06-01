from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import jwt
import mysql.connector

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "your_secret_key"

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pharmalook"
    )

# Signup Route
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password').encode('utf-8')

    db = get_db_connection()
    cursor = db.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    if user:
        return jsonify({"error": "User already exists"}), 409

    # Hash password and store
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)

    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"success": True, "message": "User registered successfully!"}), 201

# Login Route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password').encode('utf-8')
    remember_me = data.get('rememberMe', False)
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}),

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database error"}),

    try:
        cursor = db.cursor()
        cursor.execute("SELECT email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        stored_password = user[1].encode('utf-8')
        if bcrypt.checkpw(password, stored_password):
            # expiration = 7 * 24 * 60 * 60 if remember_me else 24 * 60 * 60 
            # expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
            token = jwt.encode({"email": email}, app.config["SECRET_KEY"], algorithm="HS256")
            return jsonify({"success": True, "token": token}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}),
    finally:
        cursor.close()
        db.close()

@app.route('/api/password-recovery', methods=['POST'])
def password_recovery():
    data = request.get_json()
    email = data.get('email')

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Email not registered"}), 404

    # Simulate sending a reset link (real implementation would send an email)
    return jsonify({"message": "Password reset link sent to your email!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    

