from flask import Flask, redirect, url_for
from config import Config
from extensions import db,csrf

def create_app(config_class: type[Config] = Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    @app.route("/")
    def home():
        return redirect(url_for("users.index"))
    
    with app.app_context():
        from app.models import User
        db.create_all()
    
    return app
