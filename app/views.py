from flask import render_template, request, redirect, url_for

from app import app, db
from app.models import Review, DrinkType, Distiller, Origin


@app.route('/')
def index():
    posts = Review.query.all()
    return render_template('index.html', posts=posts)


# main nav items

@app.route('/reviews/')
def review_list():
    return render_template('review_list.html')


@app.route('/articles/')
def article_list():
    return render_template('article_list.html')


@app.route('/colophon/')
def colophon():
    return render_template('colophon.html')


# admin

@app.route('/admin/posts/')
def admin_post_list():
    return '<p>post list</p>'


@app.route('/admin/drinktype/')
def admin_list_drinktypes():
    drink_types = DrinkType.query.all()
    return render_template('admin_list_drinktypes.html', drink_types=drink_types)

@app.route('/admin/drinktype/new/')
def admin_new_drinktype():
    return render_template('admin_edit_drinktype.html', drink=None)

@app.route('/admin/drinktype/<drink_type>')
def admin_edit_drinktype(drink_type):
    return render_template('admin_edit_drinktype.html', drink_type=drink_type)

@app.route('/admin/save/drinktype/', methods=['POST'])
def save_drinktype():
    drink_type = DrinkType(request.form['name'])
    db.session.add(drink_type)
    db.session.commit()
    return redirect(url_for('admin_list_drinktypes'))
