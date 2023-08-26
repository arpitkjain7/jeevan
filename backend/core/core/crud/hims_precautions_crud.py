from core import create_session, logger
from core.orm_models.hospital_schema.precautions import Precautions
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDPrecautions:
    def create(self, **kwargs):
        """[CRUD function to create a new Precautions record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPrecautions create request")
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
            precautions = Precautions(**kwargs)
            with create_session() as transaction_session:
                transaction_session.add(precautions)
                transaction_session.commit()
                transaction_session.refresh(precautions)
        except Exception as error:
            logging.error(f"Error in CRUDPrecautions create function : {error}")
            raise error

    def read_by_pmrId(self, pmr_id: int):
        """[CRUD function to read a Precautions record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Precautions record matching the criteria]
        """
        try:
            logging.info("CRUDPrecautions read request")
            with create_session() as transaction_session:
                obj: Precautions = (
                    transaction_session.query(Precautions)
                    .filter(Precautions.pmr_id == pmr_id)
                    .order_by(Precautions.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDPrecautions read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Precautions record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Precautions records]
        """
        try:
            logging.info("CRUDPrecautions read_all request")
            with create_session() as transaction_session:
                obj: Precautions = transaction_session.query(Precautions).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDPrecautions read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a Precautions record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPrecautions update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with create_session() as transaction_session:
                obj: Precautions = (
                    transaction_session.query(Precautions)
                    .filter(Precautions.id == kwargs.get("id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDPrecautions update function : {error}")
            raise error

    def delete(self, precaution_id: int):
        """[CRUD function to delete a Precautions record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPrecautions delete function")
            with create_session() as transaction_session:
                obj: Precautions = (
                    transaction_session.query(Precautions)
                    .filter(Precautions.id == precaution_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDPrecautions delete function : {error}")
            raise error
