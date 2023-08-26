# Database Manager
from gateway.database.database_manager import DatabaseManager
from commons.logger import logger
from celery import Celery

database_manager = DatabaseManager.sharedInstance()
Base = database_manager.Base
# hospital_Base = database_manager.hospital_Base
# Metadata = database_manager.metadata
from gateway.database.context_manager import create_session

# Create Tables
from gateway.orm_models.hospital_schema import *
from gateway.orm_models.lobster_schema import *

Base.metadata.create_all(bind=database_manager.engine)
# hospital_Base.metadata.create_all(bind=database_manager.engine)
from commons.load_config import load_configuration

config = load_configuration()

celery = Celery("tasks", broker="amqp://lobster-mq", backend="rpc://lobster-mq")
