from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_required, login_user, logout_user
from app.models.role import Role
from app.models.user import User
from app.services.user_service import UserService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash("Your account is inactive. Please contact administrator", "warning")
                return redirect(url_for("auth.login"))
            
            login_user(user)
            flash("Logged in successfully", "success")
            # Redirect to user table index

            return redirect(url_for("users.index"))
        
        flash("Invalid username or password", "danger")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        full_name = request.form.get("full_name", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        errors = []

        if not username:
            errors.append("Username is required.")
        if not email:
            errors.append("Email is required.")
        if not full_name:
            errors.append("Full Name is required.")
        if not password:
            errors.append("Password is required.")
        if password and password != confirm_password:
            errors.append("Passwords do not match.")

        if username and User.query.filter_by(username=username).first():
            errors.append("This username is already taken.")
        if email and User.query.filter_by(email=email).first():
            errors.append("This email is already taken.")

        if errors:
            for msg in errors:
                flash(msg, "danger")

            return render_template(
                "auth/register.html",
                username=username,
                email=email,
                full_name=full_name
            )
        
        default_role = Role.query.filter_by(name="User").first()
        default_role_id = default_role.id if default_role else None
        

        data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "is_active": True
        }

        new_user = UserService.create(
            data=data,
            password=password,
            role_id=default_role_id
        )

        login_user(new_user)
        flash("Account created successfully. You are logged in now", "success")
        return redirect(url_for("users.index"))
    
    return render_template("auth/register.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("auth.login"))
