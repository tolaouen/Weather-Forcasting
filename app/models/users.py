from sqlalchemy import Column, Integer, String, DateTime, ReleaseSavepointClause, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import Base
from datetime import datetime


# User Table Models

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String(120), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)  
    hashed_password = Column(String(120), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


    def set_password(self, password: str) -> str:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)
    
    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
        