from core import session, logger
from core.orm_models.hims_silo import Silo
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDSilo:
    def create(self, **kwargs):
        """[CRUD function to create a new Condition record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDCondition create request")
            kwargs.update(
                {
                    "created_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    ),
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    ),
                }
            )
            condition = Silo(**kwargs)
            with session() as transaction_session:
                transaction_session.connection(
                    execution_options={
                        "schema_translate_map": {"abc_healthcare": "abc_healthcare"}
                    }
                )
                transaction_session.add(condition)
                transaction_session.commit()
                transaction_session.refresh(condition)
            return condition.id
        except Exception as error:
            logging.error(f"Error in CRUDCondition create function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Condition record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Condition records]
        """
        try:
            logging.info("CRUDCondition read_all request")
            with session() as transaction_session:
                transaction_session.connection(
                    execution_options={
                        "schema_translate_map": {"abc_healthcare": "abc_healthcare"}
                    }
                )
                obj: Silo = transaction_session.query(Silo).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDCondition read_all function : {error}")
            raise error
