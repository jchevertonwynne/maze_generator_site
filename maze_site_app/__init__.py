from flask import Flask, make_response, render_template, redirect, request, session
from flask_login import login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = "lmao i am secret"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from maze_site_app.routes import routes

git s