import os
from dotenv import load_dotenv

# locazione del progetto
basedir = os.path.abspath(os.path.dirname(__file__))

# production
# load_dotenv(os.path.join(basedir, '.env'))
# load_dotenv(os.path.join(basedir, '.flaskenv'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "static/img/posts"