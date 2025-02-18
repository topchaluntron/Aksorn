from models import db
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

app_routes = Blueprint('main', __name__)

@app_routes.route('/')
def home():
    return render_template('index.html')

# @app_routes.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')


# @app_routes.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')

#         hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

#         new_user = User(username=username, email=email, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()

#         return redirect(url_for('auth.login'))
#     return render_template('register.html')

# @app_routes.route('/login', methods=['GET', 'POST'])
# def login():
#     return render_template('login.html')
