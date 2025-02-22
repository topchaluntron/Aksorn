from aksorn import app , db
from aksorn.models import User


with app.app_context():
    db.create_all

user = User.query.first()

if user :
    print(f"User found: {user.username}")
else:
    print("No users found in the database.")
