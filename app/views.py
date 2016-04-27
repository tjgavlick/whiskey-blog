import re, random, os, time

from flask import render_template, request, redirect, url_for
from werkzeug import secure_filename
from sqlalchemy import and_
from markupsafe import Markup

from app import app, db, constants, markdown
from app.models import Review, Article, Distiller, Origin
from app.functions import allowed_file


@app.route('/')
def index():
    reviews = list(Review.query.order_by(Review.date_posted.desc()).limit(6))
    articles = list(Article.query.order_by(Article.date_posted.desc()).limit(6))

    # add type attributes to items so we can label the list
    for review in reviews:
        review.type = 'review'
    for article in articles:
        article.type = 'article'

    # combine the two different post types into a single ordered list
    posts = sorted(reviews + articles, key=lambda x: x.date_posted, reverse=True)

    return render_template('index.html', posts=posts)


# reviews
#########

@app.route('/review/<review_name>')
def view_review(review_name):
    review = Review.query.filter_by(url=review_name).first()
    return render_template('review.html', review=review,
                           drink_types=constants.DRINK_TYPES,
                           rarities=constants.RARITIES)


@app.route('/reviews/')
def review_list():
    sort = request.args.get('sort', '')
    if sort:
        if sort == 'best':
            reviews = Review.query.order_by(Review.rating_low.desc())
        else:
            reviews = Review.query.order_by(Review.rating_low)
    else:
        reviews = Review.query.order_by(Review.date_posted.desc())

    origins = Origin.query.all()
    this_origin = None

    drink_type = request.args.get('type', '')
    if drink_type:
        reviews = reviews.filter(Review.drink_type == drink_type)

    age = request.args.get('age', '')
    if age:
        age_min = constants.AGE_RANGES[age]['age_min']
        age_max = constants.AGE_RANGES[age]['age_max']
        reviews = reviews.filter(and_(Review.age_low >= age_min, Review.age_low < age_max))

    proof = request.args.get('proof', '')
    if proof:
        proof_min = constants.PROOF_RANGES[proof]['proof_min']
        proof_max = constants.PROOF_RANGES[proof]['proof_max']
        reviews = reviews.filter(and_(Review.proof_low >= proof_min, Review.proof_low < proof_max))

    price = request.args.get('price', '')
    if price:
        price_min = constants.PRICE_RANGES[price]['price_min']
        price_max = constants.PRICE_RANGES[price]['price_max']
        reviews = reviews.filter(and_(Review.price_low >= price_min, Review.price_low < price_max))

    rarity = request.args.get('rarity', '')
    if rarity:
        reviews = reviews.filter(Review.rarity == rarity)

    origin = request.args.get('origin', '')
    if origin:
        this_origin = Origin.query.get(origin)
        reviews = reviews.filter(Review.origin == this_origin)

    if reviews.count() == 0:
        reviews = None

    return render_template('review_list.html', reviews=reviews,
                           review_sorts=constants.REVIEW_SORTS,
                           origins=origins,
                           this_origin=this_origin,
                           drink_types=constants.DRINK_TYPES,
                           rarities=constants.RARITIES,
                           age_ranges=constants.AGE_RANGES,
                           proof_ranges=constants.PROOF_RANGES,
                           price_ranges=constants.PRICE_RANGES,
                           no_reviews_message=random.choice(constants.NO_REVIEWS_MESSAGES))



# articles
##########

@app.route('/article/<article_name>')
def view_article(article_name):
    article = Article.query.filter_by(url=article_name).first()
    return render_template('article.html', article=article,
                           drink_types=constants.DRINK_TYPES,
                           rarities=constants.RARITIES)


@app.route('/articles/')
def article_list():
    articles = Article.query.order_by(Article.date_posted.desc())
    return render_template('article_list.html', articles=articles)


# static pages
##############

@app.route('/colophon/')
def colophon():
    return render_template('colophon.html')



# admin
#######

@app.route('/admin/')
def admin_index():
    reviews = Review.query.order_by(Review.date_posted.desc()).limit(5)
    articles = Article.query.order_by(Article.date_posted.desc()).limit(5)
    return render_template('admin_index.html', reviews=reviews, articles=articles)


# admin - reviews
####################

@app.route('/admin/review/')
def admin_list_reviews():
    if request.args.get('order', '') == 'alpha':
        reviews = Review.query.order_by(Review.title)
    else:
        reviews = Review.query.order_by(Review.date_posted.desc())
    return render_template('admin_list_reviews.html', reviews=reviews)


@app.route('/admin/review/new/')
def admin_new_review():
    origins = Origin.query.order_by(Origin.name)
    distillers = Distiller.query.order_by(Distiller.name)
    return render_template('admin_edit_review.html', review=None,
                           origins=origins, distillers=distillers,
                           drink_types=constants.DRINK_TYPES,
                           rarities=constants.RARITIES)


@app.route('/admin/review/<int:review_id>')
def admin_edit_review(review_id):
    review = Review.query.get(review_id)
    origins = Origin.query.order_by(Origin.name)
    distillers = Distiller.query.order_by(Distiller.name)
    return render_template('admin_edit_review.html', review=review,
                           origins=origins, distillers=distillers,
                           drink_types=constants.DRINK_TYPES,
                           rarities=constants.RARITIES)


@app.route('/admin/review/save/', methods=['POST'])
def admin_save_review():
    review_id = int(request.form['id'])

    if request.form['url']:
        tmp_url = request.form['url']
    else:
        tmp_url = '-'.join(request.form['title'].split(' ') + request.form['subtitle'].split(' '))
        tmp_url = re.sub(r'[^a-zA-Z0-9\-]', '', tmp_url).lower()
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
        review.drink_type = request.form['drink_type']
        review.mashbill = request.form['mashbill']
        review.mashbill_description = request.form['mashbill_description']
        review.rarity = request.form['rarity']
        review.color = request.form['color']
        review.body = request.form['body']
        review.abstract = request.form['abstract']
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
                        drink_type=request.form['drink_type'],
                        mashbill=request.form['mashbill'],
                        mashbill_description=request.form['mashbill_description'],
                        rarity=request.form['rarity'],
                        color=request.form['color'],
                        body=request.form['body'],
                        abstract=request.form['abstract'],
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


# admin - articles
##################

@app.route('/admin/article/')
def admin_list_articles():
    if request.args.get('order', '') == 'alpha':
        articles = Article.query.order_by(Article.title)
    else:
        articles = Article.query.order_by(Article.date_posted.desc())
    return render_template('admin_list_articles.html', articles=articles)


@app.route('/admin/article/new/')
def admin_new_article():
    return render_template('admin_edit_article.html', article=None)


@app.route('/admin/article/<int:article_id>')
def admin_edit_article(article_id):
    article = Article.query.get(article_id)
    return render_template('admin_edit_article.html', article=article)


@app.route('/admin/article/save/', methods=['POST'])
def admin_save_article():
    article_id = int(request.form['id'])

    if request.form['url']:
        tmp_url = request.form['url']
    else:
        tmp_url = '-'.join(request.form['title'].split(' ') + request.form['subtitle'].split(' '))
        tmp_url = re.sub(r'[^a-zA-Z0-9\-]', '', tmp_url).lower().rstrip('-')
    tmp_is_published = True if request.form.get('is_published') else False

    # if we're editing an existing entry
    if article_id > 0:
        article = Article.query.get(article_id)
        article.url = tmp_url
        article.is_published = tmp_is_published
        article.title = request.form['title']
        article.subtitle = request.form['subtitle']
        article.image_main = request.form['image_main']
        article.image_list = request.form['image_list']
        article.body = request.form['body']
        article.abstract = request.form['abstract']

    # if we're adding a new entry
    else:
        article = Article(url=tmp_url,
                          is_published=tmp_is_published,
                          title=request.form['title'],
                          subtitle=request.form['subtitle'],
                          image_main=request.form['image_main'],
                          image_list=request.form['image_list'],
                          body=request.form['body'],
                          abstract=request.form['abstract']
                          )


    db.session.add(article)
    db.session.commit()

    return redirect(url_for('admin_list_articles'))


@app.route('/admin/article/remove/<int:article_id>')
def admin_remove_article(article_id):
    article = Article.query.get(article_id)
    if not article is None:
        db.session.delete(article)
        db.session.commit()
    return redirect(url_for('admin_list_articles'))



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



# admin - files
###############

@app.route('/admin/files/')
def admin_list_files():
    upload_folder = app.config['UPLOAD_FOLDER']
    files = [(file, \
              os.path.getmtime(os.path.join(upload_folder, file)), \
              time.ctime(os.path.getmtime(os.path.join(upload_folder, file)))) \
             for file in os.listdir(upload_folder) if \
             os.path.isfile(os.path.join(upload_folder, file)) and \
             allowed_file(file)]
    folder = upload_folder.replace('app', '')

    if request.args.get('order', '') == 'time':
        files = sorted(files, key=lambda x: x[1], reverse=True)

    return render_template('admin_list_files.html', files=files, folder=folder)


@app.route('/admin/files/new/')
def admin_new_file():
    return render_template('admin_new_file.html')


@app.route('/admin/files/remove/<file>')
def admin_delete_file(file):
    path = os.path.join(app.config['UPLOAD_FOLDER'], file)
    if file and os.path.isfile(path):
        os.remove(path)

    return redirect(url_for('admin_list_files'))



# utilities
###########

@app.route('/upload/', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # todo: replace with upload success
        return redirect(url_for('admin_list_files'))
    # todo: replace with upload failure
    return redirect(url_for('admin_list_files'))


@app.route('/api/markdown/', methods=['POST'])
def parse_markdown():
    return markdown(request.data.decode('utf-8'))
