import datetime

from flask import request
from werkzeug import url_encode

from app import constants


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in constants.ALLOWED_EXTENSIONS


def format_price(price):
    if price % 1 == 0:
        return '${}'.format(int(price))
    return '${}'.format(Decimal(price).quantize(Decimal('1.00')))


def format_age(age):
    if age % 1 == 0:
        if age == 1:
            return 'One year'
        else:
            return '{} years'.format(int(age))
    elif age < 1:
        return '{} months'.format(round(age * 12))
    elif age < 2:
        return 'One year {} months'.format(round(age % 1 * 12))
    return '{} years {} months'.format(int(age), round(age % 1 * 12))


def format_age_range(age1, age2):
    if age1 > age2:
        age1, age2 = age2, age1
    if age1 % 1 == 0 and age2 % 1 == 0:
        return '{} – {} years'.format(int(age1), int(age2))
    return format_age(age1) + ' – ' + format_age(age2)


def format_proof(proof):
    if proof % 1 == 0:
        return str(int(proof))
    return proof


def format_datetime(t):
    return t.strftime('%B %d, %Y at %H:%M')


def modify_query(**new_values):
    args = request.args.copy()

    for key, val in new_values.items():
        args[key] = val

    return '{}?{}'.format(request.path, url_encode(args))
