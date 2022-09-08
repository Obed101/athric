#!/usr/bin/env python
""" Model for handling database requests"""
from datetime import date
import os
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from utils import app, db

login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(id):
    return User.query.get(id)


class User(UserMixin, db.Model):
    """A user instance"""
    id = db.Column(db.Integer, db.Identity(
        start=20, cycle=True), primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(100))
    fullname = db.Column(db.String(100))
    tel = db.Column(db.Integer)
    role = db.Column(db.String(30))
    password = db.Column(db.String(40))

    def get_id(self):
        return self.id

    def set_fullname(self):
        """Creates a fullname for the user"""
        self.fullname = self.firstname + " " + self.lastname
        return self.fullname

    def set_password(self, password):
        """Generates a password hash"""
        return generate_password_hash(password)

    def check_password(self, password):
        """Checks if password is correct"""
        return check_password_hash(self.password, password)
    
    def reset_password(self):
        """Resets the user's password to `pass`"""
        self.password = self.set_password('pass')

    def delete(self):
        """Deletes a User"""
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    """Creates a new article"""
    __searchable__ = ['subject', 'date', 'message', 'cover', 'category']
    id = db.Column(db.Integer(), primary_key=True)
    cover = db.Column(db.String(80), default=os.path.join('static', 'images', 'post_default.jpg'))
    subject = db.Column(db.String(80))
    message = db.Column(db.Text())
    category = db.Column(db.String(50))
    unique_name = db.Column(db.String(100))
    user = db.relationship('User', secondary='user_article')
    date = db.Column(db.String(), default=str(date.today().strftime('%B %d, %Y')))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def delete(self):
        """Deletes an article"""
        db.session.delete(self)
        db.session.commit()


class File(db.Model):
    """
    ### Saves files like images, videos, and documents
    - Saves the file with details provided
    """
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    original_name = db.Column(db.String(110))
    u_name = db.Column(db.String(100))
    message = db.Column(db.Text())
    f_type = db.Column(db.String(15))
    path = db.Column(db.String(110))
    fmt = db.Column(db.String(10))
    date = db.Column(db.String(30), default=str(date.today().strftime('%B %d, %Y')))

    def delete(self):
        """Deletes the file"""
        if os.path.exists(self.path):
            os.remove(self.path)
        db.session.delete(self)
        db.session.commit()


class Notice(db.Model):
    """Notice message saver"""
    id = db.Column(db.Integer(), primary_key=True)
    subject = db.Column(db.String(80))
    message = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.String(), default=str(date.today().strftime('%A, %B %d %Y')))

    def delete(self):
        """Deletes a notice"""
        db.session.delete(self)
        db.session.commit()


"""Creating a relationship between a user and an article"""
user_article = db.Table('user_article', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), 
                     primary_key=True), db.Column('article_id', db.Integer, db.ForeignKey('article.id'), 
                     primary_key=True)
                     )
# db.drop_all()
db.create_all()
