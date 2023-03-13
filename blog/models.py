from blog import db, app, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    posts = db.relationship("Post", backref="user", lazy=True)

    def __init__(self, name, surname, email, password, confirmed,
                 paid=False, admin=False, confirmed_on=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.registered_on = datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def __repr__(self, name):
        return f'{self.name}({self.email})'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, title, subtitle, content, user):
        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.user = user
    
    def __repr__(self):
        return f'Post: {self.title}'
