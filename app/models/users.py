
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime


# User Table Models

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    username = db.Column(db.String(120), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    full_name = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)  
    hashed_password = db.Column(db.String(120), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


    def set_password(self, password: str) -> str:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)
    
    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
        