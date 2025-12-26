import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///app.db"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "i_love_you"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


