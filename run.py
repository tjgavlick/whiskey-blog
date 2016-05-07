#! ./ve/bin/python

import time

from app import app, db
from app.models import User

# wait for postgres server to be up. ugly, revise
time.sleep(10)

db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
