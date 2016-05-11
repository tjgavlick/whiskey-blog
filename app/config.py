# -*- coding: utf-8 -*-

class Config(object):
    DEBUG = False
    SECRET_KEY = 'changemeplz'
    SQLALCHEMY_DATABASE_URI = 'postgresql://tdw:tdw@db:5432/tdw'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/uploads/'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://tdw:tdw@localhost/tdw'
