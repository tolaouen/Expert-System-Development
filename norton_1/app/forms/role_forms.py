from flask_wtf import FlaskForm
from collections import defaultdict
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import  DataRequired, Length, ValidationError

from app.models import Role, Permission
from extensions import db

from app.forms.check_forms import MultiCheckBoxField


def _permission_choice():
    """ Flat (id, label) list. used for field blinding only."""
    return [
        (perms.id, f"{perms.code} - {perms.name}") for perms in db.session.scalars(
            db.select(Permission).order_by(Permission.code)
        )
    ]

def _permissions_group_by_module():
    """
    Return permissions group by module:
    {
        "Users": [Permission, ...],
        "Permissions": [Permission, ...],
        ...
    }
    """

    permission = list(
        db.session.scalars(
            db.select(Permission).order_by(Permission.module, Permission.code)
        )
    )

    grouped = defaultdict(list)
    for perm in permission:
        module = perm.module or "General"
        grouped[module].append(perm)
    return dict(grouped)


class RoleCreateForm(FlaskForm):

    name = StringField(
        "name",
        validators=[DataRequired(), Length(min=3, max=20)],
        render_kw={"placeholder": "Enter your name"}
    )

    description = StringField(
        "description",
        render_kw={"placeholder": "Enter your description"}
    )

    permission_id = MultiCheckBoxField(
        "permission_id",
        coerce=int,
        render_kw={"placeholder": "Permission grant to this role."}
    )

    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permission_id.choices = _permission_choice()
        self.permission_by_module = _permissions_group_by_module()

    def validate_name(self, field):
        exists = db.session.scalar(
            db.select(Role).filter(Role.name == field.data)
        )

        if exists:
            raise ValidationError("This role is already taken.")
        

class RoleEditForm(FlaskForm):

    name = StringField(
        "name", 
        validators=[DataRequired(), Length(min=3, max=20)]
    )

    description = TextAreaField("description")

    permission_id = MultiCheckBoxField(
        "permission",
        coerce=int
    )

    submit = SubmitField("Save")

    def __init__(self, original_role: Role, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_role = original_role
        self.permission_id.choices = _permission_choice()
        self.permission_by_module = _permissions_group_by_module()

        if not self.is_submitted():
            self.permission_id.data = [p.id for p in original_role.permissions]

    def validate_name(self, field):
        q = db.select(Role).filter(Role.name == field.data, Role.id != self.original_role.id)
        
        exists = db.session.scalar(q)

        if exists:
            raise ValidationError("This role is already taken.")
        
class RoleConfirmDelete(FlaskForm):
    submit = SubmitField("Confirm Delete")




