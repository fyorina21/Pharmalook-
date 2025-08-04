
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# In-memory user storage (replace with file/database in real implementation)
users = {
    "test@example.com": {
        "password": "password123",  # In real implementation, store hashed passwords
        "phone": "1234567890"
    }
}

# In-memory session storage
sessions = {}

class LoginHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/dashboard':
            # Check for valid session cookie
            cookies = self.parse_cookies()
            if 'session_id' in cookies and cookies['session_id'] in sessions:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"""
                    <html>
                    <body>
                        <h1>Welcome to your dashboard!</h1>
                        <p>You are logged in as: """ + 
                        sessions[cookies['session_id']]['email'].encode() + b"""</p>
                        <a href="/logout">Logout</a>
                    </body>
                    </html>
                """)
            else:
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
        elif self.path == '/logout':
            # Clear session
            cookies = self.parse_cookies()
            if 'session_id' in cookies and cookies['session_id'] in sessions:
                del sessions[cookies['session_id']]
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)
            
            email = data.get('email', [''])[0]
            password = data.get('password', [''])[0]
            
            if email in users and users[email]['password'] == password:
                # Create simple session
                session_id = str(hash(email + str(time.time())))
                sessions[session_id] = {'email': email}
                
                self.send_response(302)
                self.send_header('Location', '/dashboard')
                self.send_header('Set-Cookie', f'session_id={session_id}')
                self.end_headers()
            else:
                self.send_response(302)
                self.send_header('Location', '/login?error=1')
                self.end_headers()

    def parse_cookies(self):
        cookies = {}
        if 'Cookie' in self.headers:
            for cookie in self.headers['Cookie'].split(';'):
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    cookies[key] = value
        return cookies

def run(server_class=HTTPServer, handler_class=LoginHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    import time  # Only used for session ID generation
    run()

import traceback

26fa45e (Finished backend of admin and linked icon with accept reject page)
from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
import bcrypt
import jwt
import mysql.connector
from datetime import datetime, timedelta
from PIL import Image

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "2478"  # Change this to a strong secret key

# Database connection function
def get_db_connection():
    try:
        return mysql.connector.connect (
            host="127.0.0.1",
            user="root",
            password="@n1meweebinthehouse",
            database="pharmalook",
            port="3306",
            auth_plugin='mysql_native_password'     
        )
            
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None


@app.route('/')
def landing():
    return render_template("index.html")


@app.route('/who_are_you')
def who_are_you():
    return render_template("who_are_you.html")

# Signup Route
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
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

    if request.method == 'GET':
        return render_template('signup.html')

# Login Route
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        remember_me = data.get('rememberMe', False)


        

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400


        hardcoded_admin_email = "admin@example.com"
        hardcoded_admin_password = b'$2b$12$0L1MHC4WB60X2D5QavfRE.OUwTNpsB/vnT9ZPaiXL56CQsRdHDysq'


        if email == hardcoded_admin_email and bcrypt.checkpw(password.encode('utf-8'), hardcoded_admin_password):
            expires_in = timedelta(days=7) if remember_me else timedelta(hours=1)

            token_payload = {
                "user_id": 0,
                "email": hardcoded_admin_email,
                "role": "admin",
                "exp": datetime.utcnow() + expires_in
            }
            token = jwt.encode(token_payload, app.config["SECRET_KEY"], algorithm="HS256")
            print("Admin login successful")
            return jsonify({
                "success": True,
                "token": token,
                "role": "admin",
                "expires_in": expires_in.total_seconds()
            }), 200



        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500

        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()


            if user is None:
                return jsonify({"error": "User not found"}), 404

            stored_password = user['password_hash'] 
            password_bytes = password.encode('utf-8')

            

            if isinstance(stored_password, str):
                stored_password_bytes = stored_password.encode('utf-8')
            else:
                stored_password_bytes = stored_password

            if bcrypt.checkpw(password_bytes, stored_password_bytes ):

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
            traceback.print_exc()
            return jsonify({"error": "Login failed"}), 500
            
        finally:
            cursor.close()
            db.close()
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/admin-dashboard')
def pharmacies():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pharmacies WHERE admin_approved = TRUE")
    pharmacies = cursor.fetchall()
    return render_template("admin-dashboard.html", pharmacies=pharmacies)


@app.route('/accRej')
def accept_reject():
    return render_template("accRej.html")


if __name__ == '__main__':
    app.run(debug=True)
    
    

led85f2 (Backened for admin dashboard and linking pages)
