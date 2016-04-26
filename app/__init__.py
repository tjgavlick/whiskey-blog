from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mistune

from app.functions import format_price, format_age, format_proof, format_datetime, modify_query

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

renderer = mistune.Renderer(escape=True, use_xhtml=True)
markdown = mistune.Markdown(renderer=renderer)

app.jinja_env.globals.update(format_price=format_price)
app.jinja_env.globals.update(format_age=format_age)
app.jinja_env.globals.update(format_proof=format_proof)
app.jinja_env.globals.update(modify_query=modify_query)
app.jinja_env.globals.update(markdown=markdown)

app.jinja_env.filters['datetime'] = format_datetime

db = SQLAlchemy(app)

from app import models, views
