"""Models for Blogly."""

from cgitb import text
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
    primary_key = True,
    autoincrement = True)

    first_name = db.Column(db.String(50),
    nullable = False)

    last_name = db.Column(db.String(50),
    nullable = False)

    image_url = db.Column(db.String(250),
    nullable = True)
    
    def __repr__(self):
        p=self
        return f"<I am first_name={p.first_name} last_name={p.last_name}>"

    
    
