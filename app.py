from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from routes import app_routes
from flask_migrate import Migrate
from models import db
app = Flask(__name__)
app.config.from_object(Config)

# db.init_app(app)
# app.register_blueprint(app_routes)
# migrate = Migrate(app,db)


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)


