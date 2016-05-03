from functools import wraps

from flask import request, abort, redirect, url_for, render_template
from flask.ext.login import LoginManager, login_user, logout_user, login_required

from app import app, db
from app.models import User


login_manager = LoginManager()
login_manager.init_app(app)

# required function for flask-login to function
@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['user'] and request.form['password']:
            u = User.query.filter_by(handle=request.form['user']).first()
            if u and u.check_password(request.form['password']):
                login_user(u)
                return redirect(url_for('admin_index'))
    return render_template('login.html')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))
