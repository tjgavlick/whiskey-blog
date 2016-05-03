from functools import wraps

from flask import request, abort, redirect, url_for, render_template, flash
from flask.ext.login import LoginManager, login_user, logout_user, login_required
from flask_wtf import Form
from wtforms import validators, StringField, PasswordField

from app import app, db
from app.models import User


login_manager = LoginManager()
login_manager.init_app(app)

# required function for flask-login to function
@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            u = User.query.filter_by(handle=form.username.data).first()
            if u and u.check_password(form.password.data):
                login_user(u)
                return redirect(url_for('admin_index'))
            flash("Bad login data. Type better")
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))
