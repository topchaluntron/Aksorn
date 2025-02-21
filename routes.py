from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for , flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user , logout_user , login_required , current_user
from models import User , Book ,db

app_routes = Blueprint('main', __name__)

@app_routes.route('/')
def home():
    return render_template('index.html')

@app_routes.route('/about')
def about():
    return render_template('about.html')

@app_routes.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password =  request.form.get('password')
        
        if not username or not password:
            flash('กรอกครบอ้ะยางง','danger ')
            return redirect(url_for('main.register'))
        
        user = User.query.filter_by(username = username).first()
        if user :
            flash('ชื่อนี้ถูกใช้แล้ว', 'danger')
            return redirect(url_for('main.register'))
        
        hashed_password  = generate_password_hash(password , methood = 'pbkdf2:sha256')
        new_user = User(username = username,password = hashed_password)

        try :
            db.session.add(new_user)
            db.session.commit()
            flash('สมัครสมาชิกสำเร็จ!!!! Please Login', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('เกิดข้อผิดพลาด Pls re login','danger')

    return render_template('register.html')

@app_routes.route('login',method = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        psssword = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user and check_password_hash(user.password ,password):
            login_user(user)
            flash('เข้าสู่ระบบแล้ว!!' , 'success')
            return redirect(url_for('main.dashboard'))

        flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    return render_template('login.html')








