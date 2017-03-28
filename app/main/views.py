from flask import render_template, abort, flash, redirect,url_for
from flask_login import login_required,current_user
from . import main
from ..models import User,Agreement
from .. import db

@main.route('/')
def index():
    agreements=Agreement.query.all()
    return render_template('index.html',agreements=agreements)


