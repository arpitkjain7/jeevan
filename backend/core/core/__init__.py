# Database Manager
from core.database.database_manager import DatabaseManager
from commons.logger import logger

database_manager = DatabaseManager.sharedInstance()
Base = database_manager.Base
Metadata = database_manager.metadata
from core.database.context_manager import session

# Create Tables
from core.orm_models import *

Base.metadata.create_all(bind=database_manager.engine)
from commons.load_config import load_configuration

config = load_configuration()
