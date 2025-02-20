from models import db
from flask import Blueprint, render_template, request, redirect, url_for , flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user , logout_user , login_required , current_user
from models import User , Book

app_routes = Blueprint('main', __name__)

@app_routes.route('/')
def home():
    return render_template('index.html')

@app_routes.route('/about')
def about():
    return render_template('about.html')

@app_routes.route('/register' , methods = ['Get' , 'Post'])
def register():
    if request.method == 'Post':
        username = request.form.get('username')
        password =  request.form.get('password')
        
        if not username or not password:
            flash('กรอกครบอ้ะยางง','danger ')
            return redirect(url_for('main.register'))
        
        user = User.query.filter_by(username = username).first()
        if user :
            flash('ชื่อนี้ถูกใช้แล้ว', 'danger')
            return redirect(url_for('main.register'))
        
        check_password  = generate_password_hash(password , methood = 'pbkdf2:sha256')
        new_password = User(username = username,password = hashed_password)

        try :
            
