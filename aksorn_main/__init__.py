from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aksorn.db'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # กำหนดให้ต้องล็อกอินก่อนเข้าบางหน้า

from aksorn import routes  # นำเข้า routes เพื่อให้ Flask รู้จัก
