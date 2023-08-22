from greenlet import getcurrent
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql:///marmodb', echo=False, pool_size=20)
DatabaseSession = sessionmaker()
DatabaseSession.configure(bind=engine)
Base = declarative_base()
db_session = None


def get_db_session():
    """ This accessor function allows us to creation of singleton database
    session into the database module, so that it can be accessed from both
    `main.py` and `marmobox_schema.py` cleanly.

    Avoid potential of unintentionally working with more than one independent
    session and therefore having unsynchronized or un-committed changes.
    """
    global db_session
    if not db_session:
        db_session = scoped_session(
            DatabaseSession,
            scopefunc=getcurrent,
        )
    assert db_session is not None
    return db_session
