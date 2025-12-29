from typing import List, Optional
from app.models.role import Role 
from app.models.permission import Permission
from extensions import db

class ServiceRole:

# Get All Of User
    @staticmethod
    def get_role() -> List[Role]:
        return Role.query.order_by(Role.id).all()

#  Get Role user by Id

    @staticmethod
    def get_role_id(role_id: int) -> Optional[Role]:
        return Role.query.get(role_id)
    
#  Create role for user management

    @staticmethod
    def create_role(data: dict, permission_id: Optional[List[int]] = None) -> Role:
        role = Role (
            name=data["name"],
            description=data.get("description") or ""
        )

        if permission_id:
            permissions = db.session.scalars (
                db.select(Permission).filter(Permission.id.in_(permission_id))
            )
            role.permissions = list(permissions)

        db.session.add(role)
        db.session.commit()
        return role
    
# Updata Role for user

    @staticmethod
    def update_role(role: Role, data: dict, permission_id: Optional[List[int]] = None) -> Role:
        role.name = data["name"]
        role.description = data.get("description") or ""

        if permission_id:
            perms: List[Permission] = []
            if permission_id:
                perms = db.session.scalars(

                    db.select(Permission).filter(Permission.id.in_(permission_id))
                )
            role.permissions = list(perms)

        db.session.commit()
        return role
    
    # Delete Role for user

    @staticmethod
    def delete_role(role: Role) -> None:
        db.session.delete(role)
        db.session.commit()



