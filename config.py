import os 


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-123"
    SQLALCHEMY_DATABASE_URI = "sqlite://site.db"

