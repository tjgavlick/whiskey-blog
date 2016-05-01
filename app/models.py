import re
from datetime import datetime

from app import db


review_rels = db.Table('reviewrels',
    db.Column('id', db.Integer, db.ForeignKey('review.id')),
    db.Column('related_id', db.Integer, db.ForeignKey('review.id'))
)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True)
    is_published = db.Column(db.Boolean)
    date_posted = db.Column(db.DateTime)
    title = db.Column(db.String(200))
    subtitle = db.Column(db.String(200))
    image_main = db.Column(db.String(255))
    image_list = db.Column(db.String(255))
    image_home = db.Column(db.String(255))
    distiller_id = db.Column(db.Integer, db.ForeignKey('distiller.id'))
    distiller = db.relationship('Distiller', backref=db.backref('reviews', lazy='dynamic'))
    age_low = db.Column(db.Float)
    age_high = db.Column(db.Float)
    proof_low = db.Column(db.Float)
    proof_high = db.Column(db.Float)
    price_low = db.Column(db.Float)
    price_high = db.Column(db.Float)
    drink_type = db.Column(db.String(50))
    mashbill = db.Column(db.String(100))
    mashbill_description = db.Column(db.String(50))
    rarity = db.Column(db.String(50))
    color = db.Column(db.Integer)
    body = db.Column(db.Text)
    abstract = db.Column(db.Text)
    rating_low = db.Column(db.Float)
    rating_high = db.Column(db.Float)
    related_reviews = db.relationship('Review',
        secondary=review_rels,
        primaryjoin=(review_rels.c.id == id),
        secondaryjoin=(review_rels.c.related_id == id),
        backref=db.backref('related_reviews_backref', lazy='dynamic'),
        lazy='dynamic')


    def __init__(self, url=None, is_published=False, date_posted=None,
                 title=None, subtitle=None, image_main=None, image_list=None,
                 image_home=None, distiller_id=None, age_low=None, age_high=None,
                 proof_low=None, proof_high=None, price_low=None, price_high=None,
                 drink_type=None, mashbill=None, mashbill_description=None,
                 rarity=None, color=None, body=None, abstract=None,
                 rating_low=None, rating_high=None):

        if date_posted is None:
            date_posted = datetime.utcnow()

        self.url = url
        self.is_published = is_published
        self.date_posted = date_posted
        self.title = title
        self.subtitle = subtitle
        self.image_main = image_main
        self.image_list = image_list
        self.image_home = image_home
        self.distiller_id = distiller_id
        self.age_low = age_low
        self.age_high = age_high
        self.proof_low = proof_low
        self.proof_high = proof_high
        self.price_low = price_low
        self.price_high = price_high
        self.drink_type = drink_type
        self.mashbill = mashbill
        self.mashbill_description = mashbill_description
        self.rarity = rarity
        self.color = color
        self.body = body
        self.abstract = abstract
        self.rating_low = rating_low
        self.rating_high = rating_high

    def __repr__(self):
        return '<Review #{} - {} {}>'.format(self.id, self.title, self.subtitle)


class Distiller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    origin_id = db.Column(db.Integer, db.ForeignKey('origin.id'))
    origin = db.relationship('Origin', backref=db.backref('distillers', lazy='dynamic'))

    def __init__(self, name, origin_id):
        self.name = name
        self.origin_id = origin_id


class Origin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    filter_name = db.Column(db.String(100))

    def __init__(self, name, filter_name=None):
        self.name = name
        self.filter_name = filter_name


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True)
    is_published = db.Column(db.Boolean)
    date_posted = db.Column(db.DateTime)
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))
    image_main = db.Column(db.String(255))
    image_list = db.Column(db.String(255))
    image_home = db.Column(db.String(255))
    body = db.Column(db.Text)
    abstract = db.Column(db.Text)

    def __init__(self, url=None, is_published=False, date_posted=None,
                 title=None, subtitle=None, image_main=None, image_list=None,
                 image_home=None, body=None, abstract=None):

        if date_posted is None:
            date_posted = datetime.utcnow()

        self.url = url
        self.is_published = is_published
        self.date_posted = date_posted
        self.title = title
        self.subtitle = subtitle
        self.image_main = image_main
        self.image_list = image_list
        self.image_home = image_home
        self.body = body
        self.abstract = abstract

    def __repr__(self):
        return '<Article #{} - {} {}>'.format(self.id, self.title, self.subtitle)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, handle, password):
        self.handle = handle
        self.password = password

    def is_active(self):
        # all admins are active
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        # we don't have anon admins
        return False
