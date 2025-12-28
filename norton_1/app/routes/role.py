from flask import Blueprint, render_template, url_for, flash, abort, redirect
from app.forms.role_forms import RoleCreateForm, RoleEditForm,RoleConfirmDelete
from flask_login import login_required
from app.services.role import ServiceRole

role_bp = Blueprint("roles", __name__, url_prefix="/roles")

@role_bp.route("/")
@login_required
def index():
    role = ServiceRole.get_role()
    return render_template("roles/index.html")

@role_bp.route("/<int:role_id>")
@login_required
def detail(role_id:int):
    role = ServiceRole.get_role_id(role_id)
     
    if role_id is None:
        abort(404)
    return render_template("roles/detail.html")

@role_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = RoleCreateForm()

    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "description": form.description.data
        }
        permission_id = form.permission_id.data or []

        role = ServiceRole.create_role(data, permission_id)
        flash(f"Role '{role.name}' was created succesfully.", "succes")
        return redirect(url_for('roles.index'))
    
    return render_template("roles/create.html")

@role_bp.route("/<int:role_id>/edit", methods=["GET", "POST"])
@login_required
def edit(role_id: int):
    role = ServiceRole.get_role_id(role_id)

    if role is None:
        abort(404)

    form = RoleEditForm(original_role=role, obj=role)

    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "description": form.description.data
        }
        permission_id = form.permission_id.data or []

        ServiceRole.update_role(data, permission_id)
        flash(f"Roles '{role.name}' was updated succesfully.", "success")
        return redirect(url_for('roles.detail', role_id=role.id))
    
    return render_template("roles/edit.html", form=form, role=role)

@role_bp.route("/<int:role_id>/delete", methods=["GET", "POST"])
@login_required
def delete(role_id):
    role = ServiceRole.get_role_id(role_id)
    if role is None:
        abort(404)

    ServiceRole.delete_role(role)
    flash(f"Role was deleted succesfully.", "success")
    return redirect(url_for('roles.index'))
    







    
