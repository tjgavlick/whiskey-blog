class Config(object):
    DEBUG = False
    SECRET_KEY = 'changeme'
    DATABASE_URI = 'sqlite://:memory:'

class DevelopmentConfig(Config):
    DEBUG = True
