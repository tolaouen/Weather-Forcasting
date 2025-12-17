from typing import Optional
from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate
from app.database import get_db

class UserService:

    @staticmethod
    def get_all(db: Session = get_db()) -> list[User]:
        return db.query(User).all()
    
    @staticmethod
    def get_by_id(user_id: int, db: Session = get_db()) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create(data: UserCreate, db: Session = get_db()) -> User:
        new_user = User(
            username=data.username,
            email=data.email,
            full_name=data.full_name,
            is_active=data.get('is_active', True)
        )
        new_user.set_password(data.password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def update(user_id: int, data: UserUpdate, db: Session = get_db()) -> Optional[User]:
        user_update = db.query(User).filter(User.id == user_id).first()

        if not user_update:
            return None
        
        for key, value in data.dict(exclude_unset=True).items():
            if key == "password":
                user_update.set_password(value)
            else:
                setattr(user_update, key, value)
        db.commit()
        db.refresh(user_update)
        return user_update

    @staticmethod
    def delete(user_id: int, db: Session = get_db()) -> bool:
        user_delete = db.query(User).filter(User.id == user_id).first()

        if not user_delete:
            return False
        
        db.delete(user_delete)
        db.commit()
        return True