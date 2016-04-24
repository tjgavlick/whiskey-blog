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


@app.route('/admin/drinktype/<int:drink_type_id>')
def admin_edit_drinktype(drink_type_id):
    drink_type = DrinkType.query.filter_by(id=drink_type_id).one()
    return render_template('admin_edit_drinktype.html', drink_type=drink_type)


@app.route('/admin/drinktype/save/', methods=['POST'])
def save_drinktype():
    drink_type_id = int(request.form['id'])
    drink_type_name = request.form['name']

    # if we're editing an existing entry
    if drink_type_id > 0:
        drink_type = DrinkType.query.filter_by(id=drink_type_id).one()
        drink_type.name = drink_type_name
    # if we're adding a new entry
    else:
        drink_type = DrinkType(drink_type_name)

    db.session.add(drink_type)
    db.session.commit()
    return redirect(url_for('admin_list_drinktypes'))


@app.route('/admin/drinktype/remove/<int:drink_type_id>')
def admin_remove_drinktype(drink_type_id):
    drink_type = DrinkType.query.filter_by(id=int(drink_type_id)).first()
    if not drink_type is None:
        db.session.delete(drink_type)
        db.session.commit()
    return redirect(url_for('admin_list_drinktypes'))


# admin - distillers
####################

@app.route('/admin/distiller/')
def admin_list_distillers():
    distillers = Distiller.query.all()
    return render_template('admin_list_distillers.html', distillers=distillers)


@app.route('/admin/distiller/new/')
def admin_new_distiller():
    origins = Origin.query.all()
    return render_template('admin_edit_distiller.html', distiller=None, origins=origins)


@app.route('/admin/distiller/<int:distiller_id>')
def admin_edit_distiller(distiller_id):
    distiller = Distiller.query.filter_by(id=distiller_id).one()
    origins = Origin.query.all()
    return render_template('admin_edit_distiller.html', distiller=distiller, origins=origins)


@app.route('/admin/distiller/save/', methods=['POST'])
def save_distiller():
    distiller_id = int(request.form['id'])
    distiller_name = request.form['name']
    distiller_origin = int(request.form['origin'])

    # if we're editing an existing entry
    if distiller_id > 0:
        distiller = Distiller.query.filter_by(id=distiller_id).one()
        distiller.name = distiller_name
        distiller.origin_id = distiller_origin
    # if we're adding a new entry
    else:
        distiller = Distiller(distiller_name, distiller_origin)

    db.session.add(distiller)
    db.session.commit()
    return redirect(url_for('admin_list_distillers'))


@app.route('/admin/distiller/remove/<int:distiller_id>')
def admin_remove_distiller(distiller_id):
    distiller = Distiller.query.filter_by(id=int(distiller_id)).first()
    if not distiller is None:
        db.session.delete(distiller)
        db.session.commit()
    return redirect(url_for('admin_list_distillers'))


# admin - origins
#################

@app.route('/admin/origin/')
def admin_list_origins():
    origins = Origin.query.all()
    return render_template('admin_list_origins.html', origins=origins)


@app.route('/admin/origin/new/')
def admin_new_origin():
    return render_template('admin_edit_origin.html', origin=None)


@app.route('/admin/origin/<int:origin_id>')
def admin_edit_origin(origin_id):
    origin = Origin.query.filter_by(id=origin_id).one()
    return render_template('admin_edit_origin.html', origin=origin)


@app.route('/admin/origin/save/', methods=['POST'])
def save_origin():
    origin_id = int(request.form['id'])
    origin_name = request.form['name']

    # if we're editing an existing entry
    if origin_id > 0:
        origin = Origin.query.filter_by(id=origin_id).one()
        origin.name = origin_name
    # if we're adding a new entry
    else:
        origin = Origin(origin_name)

    db.session.add(origin)
    db.session.commit()
    return redirect(url_for('admin_list_origins'))


@app.route('/admin/origin/remove/<int:origin_id>')
def admin_remove_origin(origin_id):
    origin = Origin.query.filter_by(id=int(origin_id)).first()
    if not origin is None:
        db.session.delete(origin)
        db.session.commit()
    return redirect(url_for('admin_list_origins'))
