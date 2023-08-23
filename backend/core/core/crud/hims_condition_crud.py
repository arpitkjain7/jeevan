from core import session, logger
from core.orm_models.hospital_schema.condition import Condition
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDCondition:
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
            condition = Condition(**kwargs)
            with session() as transaction_session:
                transaction_session.add(condition)
                transaction_session.commit()
                transaction_session.refresh(condition)
            return condition.id
        except Exception as error:
            logging.error(f"Error in CRUDCondition create function : {error}")
            raise error

    def read_by_pmrId(self, pmr_id: int):
        """[CRUD function to read a Condition record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Condition record matching the criteria]
        """
        try:
            logging.info("CRUDCondition read request")
            with session() as transaction_session:
                obj: Condition = (
                    transaction_session.query(Condition)
                    .filter(Condition.pmr_id == pmr_id)
                    .order_by(Condition.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDCondition read function : {error}")
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
                obj: Condition = transaction_session.query(Condition).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDCondition read_all function : {error}")
            raise error

    def update(self, id: str, **kwargs):
        """[CRUD function to update a Condition record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDCondition update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: Condition = (
                    transaction_session.query(Condition)
                    .filter(Condition.id == id)
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDCondition update function : {error}")
            raise error

    def delete(self, condition_id: int):
        """[CRUD function to delete a Condition record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDCondition delete function")
            with session() as transaction_session:
                obj: Condition = (
                    transaction_session.query(Condition)
                    .filter(Condition.id == condition_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDCondition delete function : {error}")
            raise error

    def delete_all(self, pmr_id: str):
        """[CRUD function to delete_all a Condition record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDCondition delete_all function")
            with session() as transaction_session:
                obj: Condition = (
                    transaction_session.query(Condition)
                    .filter(Condition.pmr_id == pmr_id)
                    .delete(synchronize_session=False)
                )
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDCondition delete_all function : {error}")
            raise error
