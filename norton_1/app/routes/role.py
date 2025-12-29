from flask import Blueprint, render_template, url_for, flash, abort, redirect
from app.forms.role_forms import RoleCreateForm, RoleEditForm,RoleConfirmDelete
from flask_login import login_required
from app.services.role import ServiceRole

role_bp = Blueprint("roles", __name__, url_prefix="/roles")

@role_bp.route("/")
@login_required
def index():
    roles = ServiceRole.get_role()
    return render_template("roles/index.html", roles=roles)

@role_bp.route("/<int:role_id>")
@login_required
def detail(role_id:int):
    role = ServiceRole.get_role_id(role_id)
     
    if role is None:
        abort(404)
    return render_template("roles/detail.html", role=role)

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
        flash(f"Role '{role.name}' was created successfully.", "success")
        return redirect(url_for('roles.index'))
    
    return render_template("roles/create.html", form=form)

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

        ServiceRole.update_role(role, data, permission_id)
        flash(f"Roles '{role.name}' was updated successfully.", "success")
        return redirect(url_for('roles.detail', role_id=role.id))
    
    return render_template("roles/edit.html", form=form, role=role)

@role_bp.route("/<int:role_id>/delete_confirm", methods=["GET"])
@login_required
def delete_confirm(role_id):
    role = ServiceRole.get_role_id(role_id)
    if role is None:
        abort(404)

    form = RoleConfirmDelete()
    return render_template("roles/delete_confirm.html", role=role, form=form)

@role_bp.route("/<int:role_id>/delete", methods=["GET", "POST"])
@login_required
def delete(role_id):
    role = ServiceRole.get_role_id(role_id)
    if role is None:
        abort(404)

    ServiceRole.delete_role(role)
    flash(f"Role was deleted successfully.", "success")
    return redirect(url_for('roles.index'))
    







    
