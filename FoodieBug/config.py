import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-change-me'
    # Use MySQL using PyMySQL driver. Make sure the database 'foodiebug' is created before running.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:2202@localhost/foodiebug'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
