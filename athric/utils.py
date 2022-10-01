"""
This file contains all local utilities such as functions
and variables to be imported for use in other files
"""
from flask import Flask
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from flask_msearch import Search
from werkzeug.security import check_password_hash
import os
from flask_mail import Mail

app = Flask(__name__)

app.config['CKEDITOR_PKG_TYPE'] = 'basic'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'If you\'re able to guess this key, then...'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
## Mail configurations ##
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
# app.config['TESTING'] = True
app.config['SECURITY_EMAIL_SENDER'] = os.getenv('ansah_gmail')
app.config['MAIL_USERNAME'] = os.getenv('ansah_gmail')
app.config['MAIL_PASSWORD'] = os.getenv('gmail_password')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
ckeditor = CKEditor(app)
search = Search()
search.init_app(app)
mail = Mail(app)


def change_in_db(old, new):
    """
    Modifies old data in database effectively
    if only there has been a change  
    Handles passwords differently
    """
    if old == current_user.password:
        """Handling password differently"""
        old = current_user.set_password(new) if new and not check_password_hash(old, new) else old
    else:
        old = new if not new == old else old
        current_user.fullname = current_user.set_fullname()
    db.session.commit()
    return old

template = {}
admins = ['director', 'manager', 'superviser', 'ceo']
template['categories'] = ['general_information', 'project_report', 'other_information']
template['homes'] = [
    {'name': 'Athric',
        'description': 'Leading Ghana\'s Agriculture (Entomology/crops)',
        'bg': '/static/images/1.jpg'},
    {'name': 'Since 2008',
        'description': 'Providing Domestic And Industrial Satisfaction',
        'bg': '/static/images/3.jpg'},
    {'name': 'Award Winning Team',
        'description': 'Won 8 Awards Since 2010',
        'bg': '/static/images/2.jpg'},
]
