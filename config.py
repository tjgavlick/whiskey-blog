class Config(object):
    DEBUG = False
    # db
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    # file upload
    UPLOAD_FOLDER = 'app/static/uploads/'


class DevelopmentConfig(Config):
    DEBUG = True
