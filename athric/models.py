#!/usr/bin/env python
""" Model for handling database requests"""
from datetime import date
import os
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from utils import app, db

###########
# Lines 8 to 122 under gitignore
###########
