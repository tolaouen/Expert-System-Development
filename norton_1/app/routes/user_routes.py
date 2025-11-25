from flask import url_for, Blueprint, render_template, redirect, flash, abort
from app.services.user_service import UserService
from app.forms.user_forms import UserCreateForm, UserEditForm, ComfirmDeleteForm

user_bp = Blueprint("users", __name__, url_prefix="/users")

@user_bp.route("/")
def index():
    users = UserService.get_all()
    return render_template("users/index.html", users = users)

@user_bp.route("/<int:user_id>")
def detail(user_id: int):
    users = UserService.get_by_id(user_id)
    if users is None:
        abort(404)

    return render_template(url_for("users/detail.html", users = users))

@user_bp.route("/create", methods=["GET", "POST"])
def create():
    form = UserCreateForm()
    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data ,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data
        }
        password  = form.password.data
        user = UserService.create(data, password)
        flash(f"User '{user.username}' was created successfully.", "success")
        return redirect(url_for("user.html"))
    return render_template(url_for("users/create.html", form=form))

@user_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
def edit(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None :
        abort(404)
    
    form = UserEditForm(original_user=user, obj=user)
    
    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data
        }
        password = form.password.data or None
        UserService.update(user, data, password)
        flash(f"User '{user.username}' was updated succesfully.", "success")
        return redirect(url_for("users.detail", user_id = user.id))
        
    return render_template(url_for("users/edit.html", form=form, user=user))

@user_bp.route("/<int:user_id>/delete", methods=["GET"])
def delete_confirm(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)
    
    form = ComfirmDeleteForm()
    return render_template(url_for("users/delete_form.html", user=user, form=form))

@user_bp.router("/<int:user_id>/delete", methods=["POST"])
def deletd(user_id):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)
    
    UserService.delete(user)
    flash("User was delete succesfully", "success")
    return redirect(url_for("users.index"))


