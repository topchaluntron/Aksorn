from aksorn import app, db
from aksorn.models import User  # หรือโมเดลอื่น ๆ ที่คุณต้องการตรวจสอบ

# สร้างฐานข้อมูล
with app.app_context():
    db.create_all()

# ตรวจสอบข้อมูลในฐานข้อมูล
user = User.query.first()

if user:
    print(f"User found: {user.username}")
else:
    print("No users found in the database.")
