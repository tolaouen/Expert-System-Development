from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models.permission import Permission
from extensions import db

MODULE_CHOICE = [
    ("Users", "Users"),
    ("Roles", "Roles"),
    ("Permission", "Permission"),
    ("System", "System"),
    ("Audit", "Audit"),
    ("General", "General")
]

class PermissionCreateForm(FlaskForm):
    code = StringField(
        "code", 
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"placeholder": "e.g user view"},
    )

    name = StringField(
        "name",
        validators=[DataRequired(), Length(min=3, max=30)],
        render_kw={"placeholder": "Enter your name"},
    )

    module = SelectField(
        "module",
        choices=MODULE_CHOICE,
        default="General",
    )

    description = TextAreaField(
        "description",
        render_kw={"placeholder": "Enter your description"}
    )

    submit = SubmitField("Save")

    def validate_code(self, field):
        exists = db.session.scalar(
            db.select(Permission).filter(Permission.code == field.data)
        )

        if exists:
            raise ValidationError("This permission code is already use.")
        

    def validate_name(self, field):
        exists = db.session.scalar(
            db.select(Permission).filter(Permission.name == field.data)
        )

        if exists:
            raise ValidationError("This permission code is already use.")
        
class PermissionEditForm(FlaskForm):

    code = StringField(
        "code",
        validators=[DataRequired(), Length(min=3, max=80)]
    )

    name = StringField(
        "name",
        validators=[DataRequired(), Length(min=3, max=30)]
    )

    module = SelectField(
        "module",
        choices=MODULE_CHOICE,
        default="General"
    )

    description = TextAreaField("description")

    submit = SubmitField("Save")

    def __init__(self, original_permission: Permission, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_permission = original_permission
        
        if not self.is_submitted():
            self.module.data =  original_permission.module

    def validate_code(self, field):
        q = db.select(Permission).filter(Permission.code == field.data, Permission.id != self.original_role.id)

        exists = db.session.scalar(q)
        if exists:
            raise ValidationError("This permission code is already use.")
        
    def validate_name(self, field):
        q = db.select(Permission).filter(Permission.name == field.data, Permission.id != self.original_permission.id)

        exists = db.session.scalar(q)
        if exists:
            raise ValidationError("This permission code is already use.")
        

class PermissionConfirmDelete(FlaskForm):
    submit = SubmitField("Confirm Delete")


