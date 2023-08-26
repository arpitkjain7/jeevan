from gateway import database_manager
from contextlib import contextmanager


@contextmanager
def create_session():
    try:
        current_session = database_manager.SessionMaker()
        # current_session = database_manager.session()
        yield current_session
    finally:
        current_session.close()
