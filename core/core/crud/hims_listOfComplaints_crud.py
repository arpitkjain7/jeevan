from core import session, logger
from core.orm_models.hims_listOfComplaints import ListOfComplaints
from datetime import datetime

logging = logger(__name__)


class CRUDListOfComplaints:
    def create(self, **kwargs):
        """[CRUD function to create a new Complaint record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDListOfComplaints create request")
            kwargs.update(
                {
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            list_of_complaints = ListOfComplaints(**kwargs)
            with session() as transaction_session:
                transaction_session.add(list_of_complaints)
                transaction_session.commit()
                transaction_session.refresh(list_of_complaints)
            return list_of_complaints.id
        except Exception as error:
            logging.error(f"Error in CRUDListOfComplaints create function : {error}")
            raise error


    def read_all(self):
        """[CRUD function to read_all Complaint record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Complaint records]
        """
        try:
            logging.info("CRUDListOfComplaints read_all request")
            with session() as transaction_session:
                obj: ListOfComplaints = transaction_session.query(ListOfComplaints).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDListOfComplaints read_all function : {error}")
            raise error

    def read(self,complaint: str):
        """[CRUD function to read_all Complaint record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Complaint records]
        """
        try:
            logging.info("CRUDListOfComplaints read request")
            with session() as transaction_session:
                obj: ListOfComplaints = transaction_session.query(ListOfComplaints).filter(ListOfComplaints.complaint == complaint).first()
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDListOfComplaints read_all function : {error}")
            raise error

    def delete(self, complaint_id: int):
        """[CRUD function to delete a Complaint record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDListOfComplaints delete function")
            with session() as transaction_session:
                obj: ListOfComplaints = (
                    transaction_session.query(ListOfComplaints)
                    .filter(ListOfComplaints.id == complaint_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDListOfComplaints delete function : {error}")
            raise error
