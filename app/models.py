from datetime import datetime

from app import db


class Review(db.Model):
    # __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean)
    title = db.Column(db.String(200))
    subtitle = db.Column(db.String(200))
    rating = db.Column(db.Float)
    # TODO: rating range
    image_main = db.Column(db.String(255))
    image_list = db.Column(db.String(255))
    age = db.Column(db.Float)
    # TODO: age range
    proof = db.Column(db.Float)
    # TODO: proof range
    price = db.Column(db.Float)
    # TODO: price range
    mashbill = db.Column(db.String(100))
    mashbill_description = db.Column(db.String(50))
    rarity = db.Column(db.Integer)
    color = db.Column(db.Integer)
    body = db.Column(db.Text)

    drink_type_id = db.Column(db.Integer, db.ForeignKey('drink_type.id'))
    drink_type = db.relationship('DrinkType', backref=db.backref('reviews', lazy='dynamic'))

    distiller_id = db.Column(db.Integer, db.ForeignKey('distiller.id'))
    distiller = db.relationship('Distiller', backref=db.backref('reviews', lazy='dynamic'))

    origin_id = db.Column(db.Integer, db.ForeignKey('origin.id'))
    origin = db.relationship('Origin', backref=db.backref('reviews', lazy='dynamic'))

    def __init__(self, is_published=False,
                 date_posted=None, title=None, subtitle=None, rating=None, image_main=None,
                 image_list=None, drink_type_id=None, age=None, proof=None, price=None,
                 mashbill=None, mashbill_description=None, distiller_id=None, origin_id=None,
                 rarity=None, color=None, body=None):
        if date_posted is None:
            date_posted = datetime.utcnow()
        self.date_posted = date_posted
        self.is_published = is_published
        self.title = title
        self.subtitle = subtitle
        self.rating = rating
        self.image_main = image_main
        self.image_list = image_list
        self.drink_type_id = drink_type_id
        self.age = age
        self.proof = proof
        self.price = price
        self.mashbill = mashbill
        self.mashbill_description = mashbill_description
        self.distiller_id = distiller_id
        self.origin_id = origin_id
        self.rarity = rarity
        self.color = color
        self.body = body

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
