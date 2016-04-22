class Config(object):
    DEBUG = False
    SECRET_KEY = 'changeme'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

class DevelopmentConfig(Config):
    DEBUG = True
