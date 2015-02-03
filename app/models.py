#!flask/bin/python3
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from app import db
import datetime


class sel_resturant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120))
    resturant = db.Column(db.String(120))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, email, resturant, date):
        self.name = name
        self.email = email
        self.resturant = resturant
        self.date = date

#    def __repr__(self):
#        return '%r' % (self.name)


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
      self.firstname = firstname.title()
      self.lastname = lastname.title()
      self.email = email.lower()
      self.set_password(password)

    def set_password(self, password):
      self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.pwdhash, password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
            return '<User %r>' % (self.name)


class Resturant(db.Model):
    __tablename__ = 'resturant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, name):
        self.name = name


    def __repr__(self):
        return '%r' % (self.name)

class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    resturant = db.Column(db.String(64))
    food = db.Column(db.String(64))

    def __init__(self, resturant, food):
        self.resturant = resturant
        self.food = food

    def __repr__(self):
        return '%r' % (self.food)

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120))
    resturant = db.Column(db.String(64))
    food = db.Column(db.String(64))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, email, resturant, food, date):
        self.name = name
        self.email = email
        self.resturant = resturant
        self.food = food
        self.date = date


    def __repr__(self):
        return '%r' % (self.name)

class SelectResturant(db.Model):
    __tablename__ = 'selectresturant'
    id = db.Column(db.Integer, primary_key=True)
    resturant = db.Column(db.String(64))

    def __init__(self, resturant):
        self.resturant=resturant

    def __repr__(self):
        return '%r' % (self.resturant)


class TempOrders(db.Model):
    __tablename__ = 'temporders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120))
    resturant = db.Column(db.String(64))
    food = db.Column(db.String(64))

    def __init__(self, name, email, resturant, food):
        self.name = name
        self.email = email
        self.resturant = resturant
        self.food = food


    def __repr__(self):
        return '%r ::: %r' % (self.name, self.food)


class Tempsel_resturant(db.Model):
    __tablename__ = 'tempsel_resturant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True)
    resturant = db.Column(db.String(120))

    def __init__(self, name, email, resturant):
        self.name = name
        self.email = email
        self.resturant = resturant

    def __repr__(self):
        return '%r' % (self.email)
