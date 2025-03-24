import os

class Config:
    DEBUG = True
    FLASK_ENV = 'development'
    SECRET_KEY = os.urandom(24)
