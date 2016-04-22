from flask import Flask

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = None

from app import views, models

