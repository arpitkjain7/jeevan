from core import session, logger
from core.orm_models.hims_docDetails import DocDetails
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDDocDetails:
    def create(self, **kwargs):
        """[CRUD function to create a new Doctor Detail record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDDocDetails create request")
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
            doc_details = DocDetails(**kwargs)
            with session() as transaction_session:
                transaction_session.add(doc_details)
                transaction_session.commit()
                transaction_session.refresh(doc_details)
        except Exception as error:
            logging.error(f"Error in CRUDDocDetails create function : {error}")
            raise error

    def read_by_docId(self, doc_id: int):
        """[CRUD function to read a DocDetails record]

        Args:
            doc_id (str): [Doctor Id for filtering records]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [DocDetails record matching the criteria]
        """
        try:
            logging.info("CRUDDocDetails read request")
            with session() as transaction_session:
                obj: DocDetails = (
                    transaction_session.query(DocDetails)
                    .filter(DocDetails.id == doc_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDDocDetails read function : {error}")
            raise error

    def read_by_department(self, department: str):
        """[CRUD function to read a DocDetails record]

        Args:
            department (str): [department name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [DocDetails record matching the criteria]
        """
        try:
            logging.info("CRUDDocDetails read request")
            with session() as transaction_session:
                obj: DocDetails = (
                    transaction_session.query(DocDetails)
                    .filter(DocDetails.doc_department == department)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDDocDetails read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all DocDetails record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all DocDetails records]
        """
        try:
            logging.info("CRUDDocDetails read_all request")
            with session() as transaction_session:
                obj: DocDetails = transaction_session.query(DocDetails).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDDocDetails read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a DocDetails record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDDocDetails update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: DocDetails = (
                    transaction_session.query(DocDetails)
                    .filter(DocDetails.id == kwargs.get("id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDDocDetails update function : {error}")
            raise error

    def delete(self, doc_id: int):
        """[CRUD function to delete a DocDetails record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDDocDetails delete function")
            with session() as transaction_session:
                obj: DocDetails = (
                    transaction_session.query(DocDetails)
                    .filter(DocDetails.id == doc_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDDocDetails delete function : {error}")
            raise error
