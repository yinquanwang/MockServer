import os

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:lcc123456@127.0.0.1/MockServer'
SQLALCHEMY_TRACK_MODIFICATIONS = False
