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