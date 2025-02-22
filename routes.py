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
        new_user = User(username = username, password = hashed_password)

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
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user and check_password_hash(user.password , password):
            login_user(user)
            flash('เข้าสู่ระบบแล้ว!!' , 'success')
            return redirect(url_for('main.dashboard'))

        flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    return render_template('login.html')

@app_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ออกจากระบบแล้ว','success')
    return redirect(url_for('main.home'))

@app_routes.route('/dashboard')
@login_required
def dashboard():
    reading_books = Book.query.filter_by(user_id=current_user.id, is_completed=False).all()
    completed_books = Book.query.filter_by(user_id=current_user.id, is_completed=True).all()
    return render_template('dashboard.html', reading_books=reading_books, completed_books=completed_books)

@app_routes.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        total_pages = request.form.get('total_pages')
        
        if not title or not total_pages:
            flash('กรุณากรอกข้อมูลให้ครบถ้วน', 'danger')
            return redirect(url_for('main.add_book'))
            
        try:
            total_pages = int(total_pages)
            if total_pages <= 0:
                raise ValueError
        except ValueError:
            flash('จำนวนหน้าต้องเป็นตัวเลขที่มากกว่า 0', 'danger')
            return redirect(url_for('main.add_book'))
            
        new_book = Book(
            title=title,
            total_pages=total_pages,
            user_id=current_user.id
        )
        
        try:
            db.session.add(new_book)
            db.session.commit()
            flash('เพิ่มหนังสือสำเร็จ!', 'success')
            return redirect(url_for('main.dashboard'))
        except:
            db.session.rollback()
            flash('เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง', 'danger')
            
    return render_template('add_book.html')

@app_routes.route('/book/<int:book_id>')
@login_required
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.id:
        flash('คุณไม่มีสิทธิ์เข้าถึงหนังสือนี้', 'danger')
        return redirect(url_for('main.dashboard'))
    return render_template('book_detail.html', book=book)

@app_routes.route('/book/<int:book_id>/update', methods=['POST'])
@login_required
def update_progress(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.id:
        flash('คุณไม่มีสิทธิ์แก้ไขหนังสือนี้', 'danger')
        return redirect(url_for('main.dashboard'))
        
    current_page = request.form.get('current_page', type=int)
    if not current_page or current_page < 0 or current_page > book.total_pages:
        flash('หน้าที่ระบุไม่ถูกต้อง', 'danger')
        return redirect(url_for('main.book_detail', book_id=book_id))
        
    book.update_progress(current_page)
    db.session.commit()
    
    if book.is_completed:
        flash('ยินดีด้วย! คุณอ่านหนังสือเล่มนี้จบแล้ว', 'success')
        return redirect(url_for('main.review_book', book_id=book_id))
        
    flash('อัพเดตความคืบหน้าสำเร็จ', 'success')
    return redirect(url_for('main.book_detail', book_id=book_id))

@app_routes.route('/book/<int:book_id>/review', methods=['GET', 'POST'])
@login_required
def review_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.id:
        flash('คุณไม่มีสิทธิ์รีวิวหนังสือนี้', 'danger')
        return redirect(url_for('main.dashboard'))
        
    if not book.is_completed:
        flash('คุณต้องอ่านหนังสือให้จบก่อนรีวิว', 'warning')
        return redirect(url_for('main.book_detail', book_id=book_id))
        
    if request.method == 'POST':
        rating = request.form.get('rating', type=int)
        review_text = request.form.get('review')
        
        if not rating or not (1 <= rating <= 3):
            flash('กรุณาให้คะแนน 1-3 ดาว', 'danger')
            return redirect(url_for('main.review_book', book_id=book_id))
            
        book.add_review(rating, review_text)
        db.session.commit()
        flash('บันทึกรีวิวสำเร็จ!', 'success')
        return redirect(url_for('main.book_detail', book_id=book_id))
        
    return render_template('review_book.html', book=book)

@app_routes.route('/search')
@login_required
def search_books():
    query = request.args.get('q', '')
    if query:
        books = Book.query.filter(
            Book.user_id == current_user.id,
            Book.title.ilike(f'%{query}%')
        ).all()
    else:
        books = []
    return render_template('search.html', books=books, query=query)

@app_routes.route('/profile')
@login_required
def profile():
    total_books = Book.query.filter_by(user_id=current_user.id).count()
    completed_books = Book.query.filter_by(user_id=current_user.id, is_completed=True).count()
    reading_books = Book.query.filter_by(user_id=current_user.id, is_completed=False).count()
    
    # Calculate average rating
    books_with_rating = Book.query.filter(
        Book.user_id == current_user.id,
        Book.rating.isnot(None)
    ).all()
    
    avg_rating = 0
    if books_with_rating:
        avg_rating = sum(book.rating for book in books_with_rating) / len(books_with_rating)

    return render_template('profile.html',
                        total_books=total_books,
                        completed_books=completed_books,
                        reading_books=reading_books,
                        avg_rating=round(avg_rating, 1))

