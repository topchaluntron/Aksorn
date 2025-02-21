import os 


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-123"
    SQLALCHEMY_DATABASE_URI = "sqlite://site.db"
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'aksorn.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    