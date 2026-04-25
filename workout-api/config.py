import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-workout-app'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///workout_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
