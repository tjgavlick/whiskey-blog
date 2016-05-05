#! ./ve/bin/python

from app import app, db
from app.models import User

db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
