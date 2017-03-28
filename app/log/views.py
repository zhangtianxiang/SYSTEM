from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
#本层目录的__init__.py中找
from . import log
#上层目录的__init__.py中找
from .. import db
#上层目录app的models.py中找
from ..models import User
from .forms import LoginForm,RegistrationForm


@log.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(urpid=form.urpid.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('错误的用户名或密码！')
    return render_template('log/login.html', form=form)


@log.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出登陆！')
    return redirect(url_for('main.index'))

@log.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(urpid=form.urpid.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('注册成功！')
        return redirect(url_for('log.login'))
    return render_template('log/register.html', form=form)
