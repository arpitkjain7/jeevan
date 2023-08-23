from core import database_manager
from contextlib import contextmanager


@contextmanager
def session():
    try:
        current_session = database_manager.SessionMaker()
        # current_session = database_manager.session()
        yield current_session
    finally:
        current_session.close()
