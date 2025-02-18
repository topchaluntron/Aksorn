from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# สร้าง instance ของ SQLAlchemy และ LoginManager
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ผูก database และ login manager กับแอป
    db.init_app(app)
    login_manager.init_app(app)

    # Import และ register blueprint
    from aksorn.auth import auth_bp
    from aksorn.routes import main_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)

    return app

