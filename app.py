from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from routes import app_routes
from flask_migrate import Migrate
from models import db, User
from flask_login import LoginManager



app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'
login_manager.login_message = 'เข้าสู่ระบบ'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(app_routes)
migrate = Migrate(app, db)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)


