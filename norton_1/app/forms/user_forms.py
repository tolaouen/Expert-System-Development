import re
from flask_wtf import FlaskForm
from wtforms import  BooleanField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError

from app.models import User, Role

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
    

def _role_choice():
    """Retur list a (id, name) turple for all rold, order by name."""
    return [
        (role.id, role.name)
        for role in db.session.scalars(
            db.select(Role).order_by(Role.name)
        )
    ]

class UserCreateForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=20)],
        render_kw={"placeholder": "Enter your username"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter your email"},
    )
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=3, max=120)],
        render_kw={"placeholder": "Enter your full name"},
    )
    is_active = BooleanField(
        "Is Active",
        default=True,
    )

    role_id = SelectField(
        "Role ID",
        coerce=int,
        validators=[DataRequired(), Length(min=3, max=120)],
        render_kw={"placeholder": "Select Role"},
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), strong_password],
        render_kw={"placeholder": "Enter your password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
        render_kw={"placeholder": "Confirm your password"},
    )
    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_id.choices = _role_choice()


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

    role_id = SelectField(
        "role_id",
        coerce=int,
        validators=[DataRequired()],
    )

    password = PasswordField(
        "Password",
        validators=[strong_password],
        render_kw={"placeholder": "New strong password (optional)"},
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("Update")

    def __init__(self, original_user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_user = original_user
        self.role_id.choices = _role_choice()

        if not self.is_submitted():
            if original_user.roles:
                self.original_user.data = original_user.roles[0].id
            else:
                self.role_id.data = None


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

class ConfirmDeleteForm(FlaskForm):
    submit = SubmitField("Comfirm Delete")
    



        