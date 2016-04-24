import re
from datetime import datetime

from app import db


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    is_published = db.Column(db.Boolean)
    date_posted = db.Column(db.DateTime)
    title = db.Column(db.String(200))
    subtitle = db.Column(db.String(200))
    image_main = db.Column(db.String(255))
    image_list = db.Column(db.String(255))
    rating_low = db.Column(db.Float)
    rating_high = db.Column(db.Float)
    age_low = db.Column(db.Float)
    age_high = db.Column(db.Float)
    proof_low = db.Column(db.Float)
    proof_high = db.Column(db.Float)
    price_low = db.Column(db.Float)
    price_high = db.Column(db.Float)
    mashbill = db.Column(db.String(100))
    mashbill_description = db.Column(db.String(50))
    rarity = db.Column(db.Integer)
    color = db.Column(db.Integer)
    body = db.Column(db.Text)
    abstract = db.Column(db.Text)

    drink_type_id = db.Column(db.Integer, db.ForeignKey('drink_type.id'))
    drink_type = db.relationship('DrinkType', backref=db.backref('reviews', lazy='dynamic'))

    distiller_id = db.Column(db.Integer, db.ForeignKey('distiller.id'))
    distiller = db.relationship('Distiller', backref=db.backref('reviews', lazy='dynamic'))

    origin_id = db.Column(db.Integer, db.ForeignKey('origin.id'))
    origin = db.relationship('Origin', backref=db.backref('reviews', lazy='dynamic'))

    def __init__(self, url=None, is_published=False, date_posted=None,
                 title=None, subtitle=None, rating_low=None, rating_high=None,
                 image_main=None, image_list=None, age_low=None, age_high=None,
                 proof_low=None, proof_high=None, price_low=None, price_high=None,
                 mashbill=None, mashbill_description=None, rarity=None,
                 color=None, body=None, abstract=None, drink_type_id=None,
                 distiller_id=None, origin_id=None):

        if date_posted is None:
            date_posted = datetime.utcnow()

        self.url = url
        self.is_published = is_published
        self.date_posted = date_posted
        self.title = title
        self.subtitle = subtitle
        self.image_main = image_main
        self.image_list = image_list
        self.rating_low = rating_low
        self.rating_high = rating_high
        self.age_low = age_low
        self.age_high = age_high
        self.proof_low = proof_low
        self.proof_high = proof_high
        self.price_low = price_low
        self.price_high = price_high
        self.mashbill = mashbill
        self.mashbill_description = mashbill_description
        self.rarity = rarity
        self.color = color
        self.body = body
        self.abstract = abstract
        self.drink_type_id = drink_type_id
        self.distiller_id = distiller_id
        self.origin_id = origin_id

    def __repr__(self):
        return '<Review #{} - {} {}>'.format(self.id, self.title, self.subtitle)


class DrinkType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name


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

    def __init__(self, name):
        self.name = name
