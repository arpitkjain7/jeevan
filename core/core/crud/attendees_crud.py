from core import session, logger
from core.orm_models.attendees import Attendees
from datetime import datetime

logging = logger(__name__)


class CRUDAttendees:
    def create(self, **kwargs):
        """[CRUD function to create a new Attendees record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDAttendees create function")
            kwargs.update(
                {
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            attendee = Attendees(**kwargs)
            with session() as transaction_session:
                transaction_session.add(attendee)
                transaction_session.commit()
                transaction_session.refresh(attendee)
        except Exception as error:
            logging.error(f"Error in CRUDAttendees create function : {error}")
            raise error

    def delete(self, attendee_id: str):
        """[CRUD function to delete a Service record]

        Args:
            service_id (str): [Service id to filter the record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDAttendees delete function")
            with session() as transaction_session:
                obj: Attendees = (
                    transaction_session.query(Attendees)
                    .filter(Attendees.id == attendee_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDAttendees delete function : {error}")
            raise error

    def read(self, user_id: str, event_id: int):
        """[CRUD function to read a Attendees]

        Args:
            catalog_id (str): [Catalog Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Catalog record matching the criteria]
        """
        try:
            logging.info("CRUDAttendees read request")
            with session() as transaction_session:
                obj: Attendees = (
                    transaction_session.query(Attendees)
                    .filter(Attendees.user_id == user_id)
                    .filter(Attendees.event_id == event_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                None
        except Exception as error:
            logging.error(f"Error in CRUDAttendees read function : {error}")
            raise error

    def read_by_user_id(self, user_id: int):
        """[CRUD function to read a Attendees]

        Args:
            catalog_id (str): [Catalog Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Catalog record matching the criteria]
        """
        try:
            logging.info("CRUDAttendees read request")
            with session() as transaction_session:
                obj: Attendees = (
                    transaction_session.query(Attendees)
                    .filter(Attendees.user_id == user_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                []
        except Exception as error:
            logging.error(f"Error in CRUDAttendees read function : {error}")
            raise error

    def read_by_event_id(self, event_id: int):
        """[CRUD function to read a Attendees]

        Args:
            catalog_id (str): [Catalog Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Catalog record matching the criteria]
        """
        try:
            logging.info("CRUDAttendees read request")
            with session() as transaction_session:
                obj: Attendees = (
                    transaction_session.query(Attendees)
                    .filter(Attendees.event_id == event_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                []
        except Exception as error:
            logging.error(f"Error in CRUDAttendees read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read all Attendees]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDAttendees read function")
            with session() as transaction_session:
                obj: Attendees = transaction_session.query(Attendees).all()
            return [row.__dict__ for row in obj]
        except Exception as error:
            logging.error(f"Error in CRUDAttendees read function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a Attendee record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDAttendees update function")
            event_id = kwargs.get("event_id")
            user_id = kwargs.get("user_id")
            kwargs.pop("event_id", None)
            kwargs.pop("user_id", None)
            kwargs.update({"updated_at": datetime.now()})
            with session() as transaction_session:
                obj: Attendees = (
                    transaction_session.query(Attendees)
                    .filter(Attendees.user_id == user_id)
                    .filter(Attendees.event_id == event_id)
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDAttendees update function : {error}")
            raise error
