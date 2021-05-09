import os

user = os.environ.get('DATABASE_USER')
password = os.environ.get('DATABASE_PASSWORD')
host = os.environ.get('DATABASE_HOST')
port = os.environ.get('DATABASE_PORT')
database = os.environ.get('DATABASE_DATABASE')

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION_URI = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True