from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path

from config import Config


app = Flask(__name__, instance_path=str(Path('maze_site_app/protected').absolute()))
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = '/login'

from maze_site_app import models, routes
