
import os

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('AI_DEMO_DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True