import re
from flask_wtf import FlaskForm
from wtforms import  BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError

from app.models import User
from extensions import db


def strong_password(form, field):
    """"Require at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character."""
    if len(field.data) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if not re.search(r'[A-Z]', field.data):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r'[a-z]', field.data):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r'[0-9]', field.data):
        raise ValidationError("Password must contain at least one number.")

    if not re.search(r'[!@#$%^&*]', field.data):
        raise ValidationError("Password must contain at least one special character.")

class UserCreateForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=20)],
        render_kw={"placeholder": "Enter your username"}
    ), 
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter your email"}
    ),
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=3, max=120)],
        render_kw={"placeholder": "Enter your full name"}
    ),
    is_active = BooleanField(
        "Is Active",
        default=True
    ),
    password = PasswordField(
        "Password",
        validators=[DataRequired(), strong_password],
        render_kw={"placeholder": "Enter your password"}
    ),
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"placeholder": "Confirm your password"}
    ),
    submit = SubmitField("Save")

    def validate_username(self, field):
        exists = db.session.scalar(
            db.select(User).filter(User.username == field.data)
        )
        if exists:
            raise ValidationError("This username is already taken.")
    
    def validate_email(self, field):
        exists = db.session.scalar(
            db.select(User).filter(User.email == field.data)
        )
        if exists:
            raise ValidationError("This email is already registered.")


class UserEditForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    full_name = StringField(
        "Full name",
        validators=[DataRequired(), Length(min=3, max=120)]
    )

    is_active = BooleanField("Active")

    password = PasswordField(
        "Password",
        validators=[strong_password],
        render_kw="placeholder: New strong password (option1)"
    )

    comfirm_password = PasswordField(
        "Comfirm Password",
        validators=[EqualTo("Password", message="Passwords must match.")]
    )
    submit = SubmitField("Update")

    def __init__(self, original_user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_user = original_user

    def validate_username(self, field):
        q = db.select(User).filter(User.username == field.data, User.id != self.original_user.id)
        exists = db.session.scalar(q)
        if exists:
            raise ValidationError("This username is already taken.")

    def validate_email(self, field):
        q = db.select(User).filter(User.email == field.data, User.id != self.original_user.id)
        exists = db.session.scalar(q)
        if exists:
            raise ValidationError("This email is already registered")

class ComfirmDeleteForm(FlaskForm):
    submit = SubmitField("Comfirm Delete")
    



        