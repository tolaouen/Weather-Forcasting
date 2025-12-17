from typing import Optional, Dict, Any
from app.models.users import User
from extensions import db

class UserService:

    @staticmethod
    def get_all() -> list[User]:
        return db.session.query(User).all()
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return db.session.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create(data: Dict[str, Any], password: str) -> User:
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            full_name=data.get('full_name'),
            is_active=data.get('is_active', True)
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        return new_user
    
    @staticmethod
    def update(user: User, data: Dict[str, Any], password: Optional[str] = None) -> User:
        for key, value in data.items():
            setattr(user, key, value)
        
        if password:
            user.set_password(password)
        
        db.session.commit()
        db.session.refresh(user)
        return user

    @staticmethod
    def delete(user: User) -> bool:
        db.session.delete(user)
        db.session.commit()
        return True