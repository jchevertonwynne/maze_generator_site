from string import ascii_letters
from random import choice
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "".join(choice(ascii_letters) for _ in range(32))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}/maze_site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
