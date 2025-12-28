from flask import Blueprint, redirect, render_template, flash,abort, url_for
from flask_login import login_required
from app.services.permission import ServicePermission
from app.forms.permission_forms import PermissionCreateForm, PermissionEditForm, PermissionConfirmDelete


permission_bp = Blueprint("permissions", __name__, url_prefix="/permissions")

@permission_bp.route("/")
@login_required
def index():
    permission = ServicePermission.get_permission()
    return render_template("permissions/index.html", permission=permission)

@permission_bp.route("/<int:permission_id>")
@login_required
def detail(permission_id: int):
    permission = ServicePermission.get_permission_id(permission_id)

    if permission is None:
        abort(404)

    return render_template("permissions/detail.html")

@permission_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():

    form = PermissionCreateForm()

    if form.validate_on_submit():
        data = {
            "code": form.code.data,
            "name": form.name.data,
            "module": form.module.data,
            "description": form.description.data,
        }
    
        permission = ServicePermission.create_permission(data)

        flash(f"Permission '{permission.code}' was created succesfully.", "success")
        return redirect(url_for('permissions.index'))
    return render_template("permissions/create.html", form=form)

@permission_bp.route("/<int:permission_id>/edit", methods=["GET", "POST"])
@login_required
def edit(permission_id: int):
    permission = ServicePermission.get_permission_id(permission_id)

    if permission is None:
        abort(404)
    
    form = PermissionEditForm(original_permission=permission, obj=permission)

    if form.validate_on_submit():
        data = {
            "code": form.code.data,
            "name": form.name.data,
            "module": form.module.data,
            "description": form.description.data,
        }

        ServicePermission.update_permission(permission, data)
        flash(f"Permission '{permission.code}' was updated succesfully.", "succes")
        return redirect(url_for('permissions.detail', permission_id = permission.id))
    
    return render_template("permissions/edit.html", form=form, permission=permission)

@permission_bp.route("/<int:permission_id>/delete_confirm", methods=["GET"])
@login_required
def delete_confirm(permission_id: int):
    permission = ServicePermission.get_permission_id(permission_id)

    if permission is None:
        abort(404)
    
    form = PermissionConfirmDelete()
    return render_template("permissions/delete_confirm.html", form=form, permission=permission)

@permission_bp.route("/<int:permission_id>/delete", methods=["POST"])
@login_required
def delete(permission_id: int):
    permission = ServicePermission.get_permission_id(permission_id)

    if permission is None:
        abort(404)
    
    ServicePermission.delete_permission(permission)
    flash("Permis was deleted succesfully.", "success")
    return redirect(url_for('permissions.index'))


