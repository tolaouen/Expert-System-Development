from app.models.associations import role_permissions
from extensions import db
from datetime import datetime


class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))
    module = db.Column(db.String(80), nullable=False, default="General")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    roles = db.relationship("Role", secondary=role_permissions, back_populates="permissions")


    def __repr__(self) -> str:
        return f"<Permission {self.code}>"
