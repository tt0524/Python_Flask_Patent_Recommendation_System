from flask_login import UserMixin
from application import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def __str__(self):
        return '<User {0} password: {1}>'.format(self.username, self.password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def verify_password(self, password):
        if self.password is None:
            return False
        return password == self.get_password()

    def get_password(self):
        try:
            res = db.query.filter_by(username=self.username).first().password
        except Exception:
            return False
        return res


class ClickHistory(db.Model):
    __tablename__ = 'click'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('user.username'))
    patent_id = db.Column(db.String)

    def __init__(self, username, patent_id):
        self.username = username
        self.patent_id = patent_id
