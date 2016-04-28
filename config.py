class Config(object):
    DEBUG = False
    # db
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SQLALCHEMY_ECHO = False
    # file upload
    UPLOAD_FOLDER = 'app/static/uploads/'


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://tdw:tdw@localhost/tdw'
