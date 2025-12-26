from typing import List, Optional
from app.models.permission import Permission
from extensions import db

class ServicePermission:

# Get all Permission 
    @staticmethod
    def get_permission() -> List[Permission]:
        return Permission.query.order_by(Permission.code.asc()).all()
    
# Get permission by id 
    @staticmethod
    def get_permission_id(permission_id: int) -> Optional[Permission]:
        return Permission.query.get(permission_id)
    
# Create Permission 
    @staticmethod
    def create_permission(data: dict) -> Permission:
        permission = Permission(
            code = data["code"],
            name = data["name"],
            module = data.get("module", "General"),
            description = data.get("description") or ""
        )

        db.session.add(permission)
        db.session.commit()
        return permission
    
#  Update Permission 
    @staticmethod
    def update_permission(permission: Permission, data: dict) -> Permission:
        permission.code = data["code"]
        permission.name = data["name"]
        permission.module = data.get("module", "General")
        permission.description = data.get("description") or ""

        db.session.commit()
        return permission

#  Delete Permission
    @staticmethod
    def delete_permission(permission: Permission) -> None:
        db.session.delete(permission)
        db.session.commit()
