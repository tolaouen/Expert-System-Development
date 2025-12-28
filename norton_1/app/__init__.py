from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from extensions import db, csrf

def create_app(config_class: type[Config] = Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login if not authenticated

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    from app.routes.user_routes import user_bp
    from app.routes.auth import auth_bp
    from app.routes.permission import permission_bp
    from app.routes.role import role_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(permission_bp)
    app.register_blueprint(role_bp)

    @app.route("/")
    def home():
        return redirect(url_for("users.index"))
    
    with app.app_context():
        from app.models import User, Role, Permission  # Import all models
        db.create_all()
    
    return app
