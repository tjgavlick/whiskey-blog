import re

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



# admin - reviews
####################

@app.route('/admin/review/')
def admin_list_reviews():
    reviews = Review.query.order_by(Review.date_posted.desc())
    return render_template('admin_list_reviews.html', reviews=reviews)


@app.route('/admin/review/new/')
def admin_new_review():
    origins = Origin.query.order_by(Origin.name)
    distillers = Distiller.query.order_by(Distiller.name)
    drink_types = DrinkType.query.order_by(DrinkType.name)
    return render_template('admin_edit_review.html', review=None,
                           origins=origins, distillers=distillers,
                           drink_types=drink_types)


@app.route('/admin/review/<int:review_id>')
def admin_edit_review(review_id):
    review = Review.query.get(review_id)
    origins = Origin.query.order_by(Origin.name)
    distillers = Distiller.query.order_by(Distiller.name)
    drink_types = DrinkType.query.order_by(DrinkType.name)
    return render_template('admin_edit_review.html', review=review,
                           origins=origins, distillers=distillers,
                           drink_types=drink_types)


@app.route('/admin/review/save/', methods=['POST'])
def admin_save_review():
    review_id = int(request.form['id'])

    if request.form['url']:
        tmp_url = request.form['url']
    else:
        tmp_url = '_'.join(request.form['title'].split(' ') + request.form['subtitle'].split(' '))
        tmp_url = re.sub(r'[^a-zA-Z0-9_]', '', tmp_url).lower()
    tmp_is_published = True if request.form.get('is_published') else False
    tmp_rating_low = request.form['rating_low'] if request.form['rating_low'] else 0
    tmp_rating_high = request.form['rating_high'] if request.form['rating_high'] else None
    tmp_age_low = request.form['age_low'] if request.form['age_low'] else 0
    tmp_age_high = request.form['age_high'] if request.form['age_high'] else None
    tmp_proof_low = request.form['proof_low'] if request.form['proof_low'] else 0
    tmp_proof_high = request.form['proof_high'] if request.form['proof_high'] else None
    tmp_price_low = request.form['price_low'] if request.form['price_low'] else 0
    tmp_price_high = request.form['price_high'] if request.form['price_high'] else None

    # if we're editing an existing entry
    if review_id > 0:
        review = Review.query.get(review_id)
        review.url = tmp_url
        review.is_published = tmp_is_published
        review.title = request.form['title']
        review.subtitle = request.form['subtitle']
        review.image_main = request.form['image_main']
        review.image_list = request.form['image_list']
        review.rating_low = tmp_rating_low
        review.rating_high = tmp_rating_high
        review.age_low = tmp_age_low
        review.age_high = tmp_age_high
        review.proof_low = tmp_proof_low
        review.proof_high = tmp_proof_high
        review.price_low = tmp_price_low
        review.price_high = tmp_price_high
        review.mashbill = request.form['mashbill']
        review.mashbill_description = request.form['mashbill_description']
        review.rarity = request.form['rarity']
        review.color = request.form['color']
        review.body = request.form['body']
        review.abstract = request.form['abstract']
        review.drink_type_id = request.form['drink_type_id']
        review.distiller_id = request.form['distiller_id']
        review.origin_id = request.form['origin_id']

    # if we're adding a new entry
    else:
        review = Review(url=tmp_url,
                        is_published=tmp_is_published,
                        title=request.form['title'],
                        subtitle=request.form['subtitle'],
                        image_main=request.form['image_main'],
                        image_list=request.form['image_list'],
                        rating_low=tmp_rating_low,
                        rating_high=tmp_rating_high,
                        age_low=tmp_age_low,
                        age_high=tmp_age_high,
                        proof_low=tmp_proof_low,
                        proof_high=tmp_proof_high,
                        price_low=tmp_price_low,
                        price_high=tmp_price_high,
                        mashbill=request.form['mashbill'],
                        mashbill_description=request.form['mashbill_description'],
                        rarity=request.form['rarity'],
                        color=request.form['color'],
                        body=request.form['body'],
                        abstract=request.form['abstract'],
                        drink_type_id=request.form['drink_type_id'],
                        distiller_id=request.form['distiller_id'],
                        origin_id=request.form['origin_id']
                        )


    db.session.add(review)
    db.session.commit()

    return redirect(url_for('admin_list_reviews'))


@app.route('/admin/review/remove/<int:review_id>')
def admin_remove_review(review_id):
    review = Review.query.get(review_id)
    if not review is None:
        db.session.delete(review)
        db.session.commit()
    return redirect(url_for('admin_list_reviews'))



# admin - drink types
#####################

@app.route('/admin/drinktype/')
def admin_list_drinktypes():
    drink_types = DrinkType.query.order_by(DrinkType.name)
    return render_template('admin_list_drinktypes.html', drink_types=drink_types)


@app.route('/admin/drinktype/new/')
def admin_new_drinktype():
    return render_template('admin_edit_drinktype.html', drink_type=None)


@app.route('/admin/drinktype/<int:drink_type_id>')
def admin_edit_drinktype(drink_type_id):
    drink_type = DrinkType.query.get(drink_type_id)
    return render_template('admin_edit_drinktype.html', drink_type=drink_type)


@app.route('/admin/drinktype/save/', methods=['POST'])
def admin_save_drinktype():
    drink_type_id = int(request.form['id'])
    drink_type_name = request.form['name']

    # if we're editing an existing entry
    if drink_type_id > 0:
        drink_type = DrinkType.query.get(drink_type_id)
        drink_type.name = drink_type_name
    # if we're adding a new entry
    else:
        drink_type = DrinkType(drink_type_name)

    db.session.add(drink_type)
    db.session.commit()
    return redirect(url_for('admin_list_drinktypes'))


@app.route('/admin/drinktype/remove/<int:drink_type_id>')
def admin_remove_drinktype(drink_type_id):
    drink_type = DrinkType.query.get(drink_type_id)
    if not drink_type is None:
        db.session.delete(drink_type)
        db.session.commit()
    return redirect(url_for('admin_list_drinktypes'))


# admin - distillers
####################

@app.route('/admin/distiller/')
def admin_list_distillers():
    distillers = Distiller.query.order_by(Distiller.name)
    return render_template('admin_list_distillers.html', distillers=distillers)


@app.route('/admin/distiller/new/')
def admin_new_distiller():
    origins = Origin.query.order_by(Origin.name)
    return render_template('admin_edit_distiller.html', distiller=None, origins=origins)


@app.route('/admin/distiller/<int:distiller_id>')
def admin_edit_distiller(distiller_id):
    distiller = Distiller.query.get(distiller_id)
    origins = Origin.query.order_by(Origin.name)
    return render_template('admin_edit_distiller.html', distiller=distiller, origins=origins)


@app.route('/admin/distiller/save/', methods=['POST'])
def admin_save_distiller():
    distiller_id = int(request.form['id'])
    distiller_name = request.form['name']
    distiller_origin = int(request.form['origin'])

    # if we're editing an existing entry
    if distiller_id > 0:
        distiller = Distiller.query.get(distiller_id)
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
    distiller = Distiller.query.get(distiller_id)
    if not distiller is None:
        db.session.delete(distiller)
        db.session.commit()
    return redirect(url_for('admin_list_distillers'))


# admin - origins
#################

@app.route('/admin/origin/')
def admin_list_origins():
    origins = Origin.query.order_by(Origin.name)
    return render_template('admin_list_origins.html', origins=origins)


@app.route('/admin/origin/new/')
def admin_new_origin():
    return render_template('admin_edit_origin.html', origin=None)


@app.route('/admin/origin/<int:origin_id>')
def admin_edit_origin(origin_id):
    origin = Origin.query.get(origin_id)
    return render_template('admin_edit_origin.html', origin=origin)


@app.route('/admin/origin/save/', methods=['POST'])
def admin_save_origin():
    origin_id = int(request.form['id'])
    origin_name = request.form['name']

    # if we're editing an existing entry
    if origin_id > 0:
        origin = Origin.query.get(origin_id)
        origin.name = origin_name
    # if we're adding a new entry
    else:
        origin = Origin(origin_name)

    db.session.add(origin)
    db.session.commit()
    return redirect(url_for('admin_list_origins'))


@app.route('/admin/origin/remove/<int:origin_id>')
def admin_remove_origin(origin_id):
    origin = Origin.query.get(origin_id)
    if not origin is None:
        db.session.delete(origin)
        db.session.commit()
    return redirect(url_for('admin_list_origins'))
