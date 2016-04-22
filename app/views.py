from app import app
from flask import render_template, request


@app.route('/')
def index():
    posts = [
        {
            'id': 28,
            'published': False,
            'category': "Article",
            'url': "review.htm",
            'title': "Article in progress",
            'subtitle': "",
            'description': "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
            'list_image': "http://lorempixel.com/280/266"
        },
        {
            'id': 27,
            'published': True,
            'category': "Article",
            'url': "review.htm",
            'title': "On the Consumption of Alcohol",
            'subtitle': "And the Oddity of the Hobby",
            'description': "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
            'list_image': "http://lorempixel.com/280/266"
        },
        {
            'id': 26,
            'published': True,
            'category': "Review",
            'url': "review.htm",
            'title': "Rittenhouse",
            'subtitle': "25-year Rye",
            'description': "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
            'list_image': "http://lorempixel.com/270/266"
        },
        {
            'id': 26,
            'published': False,
            'category': "Review",
            'url': "review.htm",
            'title': "Rittenhouse",
            'subtitle': "25-year Rye",
            'description': "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
            'list_image': "http://lorempixel.com/270/266"
        },
        {
            'id': 25,
            'published': True,
            'category': "Review",
            'url': "review.htm",
            'title': "Elijah Craig",
            'subtitle': "18-year Bourbon",
            'description': "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
            'list_image': "http://lorempixel.com/260/266"
        }
    ]
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
