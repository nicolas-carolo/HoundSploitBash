import sqlalchemy
from sqlalchemy.orm import sessionmaker
import sys
import os


def start_session():
    """
    Start a new database session.
    :return: a new database session.
    """
    init_path = os.path.expanduser("~") + "/.HoundSploit/"
    db_path = "sqlite:///" + init_path + "hound_db.sqlite3"
    engine = sqlalchemy.create_engine(db_path)
    Session = sessionmaker(bind=engine)
    return Session()
