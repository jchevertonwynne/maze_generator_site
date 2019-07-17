from datetime import datetime
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256

from maze_site_app import db, login


class User(UserMixin, db.Model):
    username = db.Column(db.String, primary_key=True, unique=True)
    password = db.Column(db.String(128), nullable=False)
    mazes = db.relationship('Maze', backref='maze_list', lazy=True)

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return f"User: {self.username}"

    def get_id(self) -> str:
        return self.username

    def set_password(self, password: str):
        hashed_password = pbkdf2_sha256.hash(password, rounds=200000, salt_size=16)
        self.password = hashed_password

    def check_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)


class Maze(db.Model):
    maze_id = db.Column(db.Integer, primary_key=True)
    date_made = db.Column(db.Date, nullable=False, default=datetime.now())
    creator = db.Column(db.String, db.ForeignKey('user.username'))
    private = db.Column(db.Boolean, nullable=False)

    def __repr__(self) -> str:
        return f"Maze #{self.maze_id}"


@login.user_loader
def load_user(username: str) -> User:
    return User.query.get(username)
