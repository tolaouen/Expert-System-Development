from datetime import datetime
from werkzeug.security  import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db
from app.models.associations import user_roles


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    password_hash = db.Column(db.String(120), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    roles = db.relationship("Role", secondary=user_roles, back_populates="users")


    def set_password(self, password: str)-> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str)-> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"