import os

user = os.environ.get('DATABASE_USER')
password = os.environ.get('DATABASE_PASSWORD')
host = os.environ.get('DATABASE_HOST')
port = os.environ.get('DATABASE_PORT')
database = os.environ.get('DATABASE_DATABASE')

class Config:
    DATABASE_URI = f'postgresql://{user}:{password}@{host}:{port}/{database}'