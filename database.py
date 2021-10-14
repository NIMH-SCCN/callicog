from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql:///marmodb', echo=False)
DatabaseSession = sessionmaker()
DatabaseSession.configure(bind=engine)
Base = declarative_base()
#db_session = DatabaseSession()