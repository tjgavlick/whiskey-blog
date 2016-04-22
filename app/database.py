from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app import app

engine = create_engine('sqlite:///:memory:', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import app.models
    Base.metadata.create_all(bind=engine)

# automatically remove db session at the end of request or at shutdown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
