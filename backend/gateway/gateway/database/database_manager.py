from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import MetaData, create_engine, DDL, event
import os

# from gateway import logger

# logging = logger(__name__)


class DatabaseManager:
    __instance = None

    def __setup_schema(self):
        event.listen(
            self.Base.metadata,
            "before_create",
            DDL("CREATE SCHEMA IF NOT EXISTS lobster_schema"),
        )
        event.listen(
            self.Base.metadata,
            "before_create",
            DDL("CREATE SCHEMA IF NOT EXISTS hospital_schema"),
        )

    @staticmethod
    def sharedInstance():
        """Static access method."""
        if DatabaseManager.__instance is None:
            DatabaseManager()
        return DatabaseManager.__instance

    def __init__(self):
        """Virtually private constructor."""
        if DatabaseManager.__instance is not None:
            try:
                raise Exception("Instance exists!")
            except Exception as e:
                print(e)
                # logging.error(e)
        else:
            self.db_url = os.environ.get("db_url")
            # self.db_url = "postgresql://postgres:postgres@localhost:5432/postgres"
            self.metadata = MetaData(schema="hospital_schema")
            self.engine = create_engine(self.db_url, pool_pre_ping=True)
            self.Base = declarative_base(metadata=self.metadata)
            self.session = Session(bind=self.engine)
            self.SessionMaker = sessionmaker(bind=self.engine)
            # self.hospital_metadata = MetaData(schema="lobster_schema")
            # self.hospital_Base = declarative_base(metadata=self.hospital_metadata)
            # self.hospital_session = Session(bind=self.engine)
            # self.hospital_SessionMaker = sessionmaker(bind=self.engine)
            self.__setup_schema()
            DatabaseManager.__instance = self
