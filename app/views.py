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


# admin - posts
###############

@app.route('/admin/posts/')
def admin_post_list():
    return '<p>post list</p>'


# admin - drink types
#####################

@app.route('/admin/drinktype/')
def admin_list_drinktypes():
    drink_types = DrinkType.query.all()
    return render_template('admin_list_drinktypes.html', drink_types=drink_types)


@app.route('/admin/drinktype/new/')
def admin_new_drinktype():
    return render_template('admin_edit_drinktype.html', drink_type=None)


@app.route('/admin/drinktype/<drink_type_id>')
def admin_edit_drinktype(drink_type_id):
    drink_type = DrinkType.query.filter_by(id=drink_type_id).one()
    return render_template('admin_edit_drinktype.html', drink_type=drink_type)


@app.route('/admin/save/drinktype/', methods=['POST'])
def save_drinktype():
    drink_type_id = int(request.form['id'])
    drink_type_name = request.form['name']

    # if we're editing an existing entry
    if drink_type_id > 0:
        drink_type = DrinkType.query.filter_by(id=drink_type_id).one()
        drink_type.name = drink_type_name
    # if we're adding a new entry
    else:
        drink_type = DrinkType(request.form['name'])

    db.session.add(drink_type)
    db.session.commit()
    return redirect(url_for('admin_list_drinktypes'))


@app.route('/admin/remove/drinktype/<drink_type_id>')
def admin_remove_drinktype(drink_type_id):
    drink_type = DrinkType.query.filter_by(id=int(drink_type_id)).first()
    if not drink_type is None:
        db.session.delete(drink_type)
        db.session.commit()
    return redirect(url_for('admin_list_drinktypes'))
