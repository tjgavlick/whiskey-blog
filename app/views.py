from flask import render_template, request

from app import app
from app.models import Review


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
