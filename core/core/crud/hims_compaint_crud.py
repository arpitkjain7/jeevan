from core import session, logger
from core.orm_models.hims_complaint import Complaint
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDComplaint:
    def create(self, **kwargs):
        """[CRUD function to create a new Complaint record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDComplaint create request")
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
            complaint = Complaint(**kwargs)
            with session() as transaction_session:
                transaction_session.add(complaint)
                transaction_session.commit()
                transaction_session.refresh(complaint)
        except Exception as error:
            logging.error(f"Error in CRUDComplaint create function : {error}")
            raise error

    def read_by_pmrId(self, pmr_id: int):
        """[CRUD function to read a complaint record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Complaint record matching the criteria]
        """
        try:
            logging.info("CRUDComplaint read request")
            with session() as transaction_session:
                obj: Complaint = (
                    transaction_session.query(Complaint)
                    .filter(Complaint.pmr_id == pmr_id)
                    .order_by(Complaint.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDComplaint read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Complaint record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Complaint records]
        """
        try:
            logging.info("CRUDComplaint read_all request")
            with session() as transaction_session:
                obj: Complaint = transaction_session.query(Complaint).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDComplaint read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a Complaint record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDComplaint update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: Complaint = (
                    transaction_session.query(Complaint)
                    .filter(Complaint.id == kwargs.get("id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDComplaint update function : {error}")
            raise error

    def delete(self, complaint_id: int):
        """[CRUD function to delete a Complaint record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDComplaint delete function")
            with session() as transaction_session:
                obj: Complaint = (
                    transaction_session.query(Complaint)
                    .filter(Complaint.id == complaint_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDComplaint delete function : {error}")
            raise error
