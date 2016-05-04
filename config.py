# -*- coding: utf-8 -*-

class Config(object):
    DEBUG = False
    SECRET_KEY = 'changemeplz'
    # db
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/dbname'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # file upload
    UPLOAD_FOLDER = 'app/static/uploads/'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://tdw:tdw@localhost/tdw'
