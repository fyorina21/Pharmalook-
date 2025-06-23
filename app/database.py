from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    
    def set_password(self, passwords):
        self.password = generate_password_hash(passwords)

    def check_password(self, passwords):
        return check_password_hash(self.password, passwords)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Medicinename= db.Column(db.String(100),nullable=False)
    price= db.Column(db.Float, nullable=False)
    Dosage = db.Column(db.String(100), nullable=False)
    medicinedescription= db.Column(db.String(255), nullable=False)


class Pharmacist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin_approved = db.Column(db.Boolean, default=False, nullable=False)
    
    status = db.Column(db.String(20), default='pending') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)