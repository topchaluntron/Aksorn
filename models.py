from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login  import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin , db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    book = db.relationship('Book',backref = 'reader' , lazy = True)
    create_at = db.Coloumn(db.DateTime , default = 'reader' , default = datetime.utcnow)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    current_page = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer, nullable=True)  # ให้คะแนน 1-3ดาว
    review = db.Column(db.Text, nullable=True)
    user_id  =db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    create_id  = db.Column(db.DateTime , default = datetime.utcnow)
    completed_at = db.Column(db.DateTime , nullable = True) 

    def update_progress(self , current_page):
        self.current_page = current_page
        if current_page >= self.total_pages:
            self.is_completed = True
            self.completed_at = datetime.utcnow()

    def add_review(self ,rating , review_text):
        if 1<=rating <=3:
            self.rating = rating
            self.review = review_text
            






class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
