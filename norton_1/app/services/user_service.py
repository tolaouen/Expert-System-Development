from typing import List, Optional

from click import Option
from app.models.user import User
from app.models.role import Role
from extensions import db

class UserService:
    @staticmethod
    def get_all() -> List[User]:
        return User.query.order_by(User.id.desc()).all()
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return User.query.get(user_id)
    
    @staticmethod
    def create(data: dict, password: str, role_id: Option[int] = None) -> User:
        user = User(
            username=data["username"],
            email = data["email"],
            full_name = data["full_name"],
            is_active = data.get("is_active", True)
        )

        user.set_password(password)

        if role_id:
            role = db.session.get(Role, role_id)
            if role:
                user.roles = [role]

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user: User, data: dict, password: Optional[str] = None, role_id: Optional[int] = None) -> User:
        user.username = data["username"]
        user.email = data["email"]
        user.full_name = data["full_name"]
        user.is_active = data.get("is_active", True)

        if password:
            user.set_password(password)

        if role_id:
            role = db.session.get(Role, role_id)
            if role:
                user.roles = [role]


        db.session.commit()
        return user

    @staticmethod
    def delete(user:User) -> None:
        db.session.delete(user)
        db.session.commit()
    