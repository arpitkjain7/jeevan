from core import session, logger
from core.orm_models.events import Events
from datetime import datetime

logging = logger(__name__)


class CRUDEvents:
    def create(self, **kwargs):
        """[CRUD function to create a new Events record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDEvents create request")
            kwargs.update(
                {
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            event = Events(**kwargs)
            with session() as transaction_session:
                transaction_session.add(event)
                transaction_session.commit()
                transaction_session.refresh(event)
            return event.id
        except Exception as error:
            logging.error(f"Error in CRUDEvents create function : {error}")
            raise error

    def read(self, event_id: int):
        """[CRUD function to read a Events record]

        Args:
            pricing_id (str): [Events Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Events record matching the criteria]
        """
        try:
            logging.info("CRUDEvents read request")
            with session() as transaction_session:
                obj: Events = (
                    transaction_session.query(Events)
                    .filter(Events.id == event_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDEvents read function : {error}")
            raise error

    def read_by_uuid(self, event_uuid: str):
        """[CRUD function to read a Events record]

        Args:
            pricing_id (str): [Events Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Events record matching the criteria]
        """
        try:
            logging.info("CRUDEvents read_by_uuid request")
            with session() as transaction_session:
                obj: Events = (
                    transaction_session.query(Events)
                    .filter(Events.event_uuid == event_uuid)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDEvents read_by_uuid function : {error}")
            raise error

    def read_multiple(self, event_list: list):
        try:
            logging.info("CRUDEvents read_multiple request")
            with session() as transaction_session:
                obj: Events = (
                    transaction_session.query(Events)
                    .filter(Events.id.in_(event_list))
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDEvents read_multiple function : {error}")
            raise error

    def read_by_owner_id(self, user_id: int):
        """[CRUD function to read a Events record]

        Args:
            cognitive_service (str): [Events Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Events record matching the criteria]
        """
        try:
            logging.info("CRUDEvents read request")
            with session() as transaction_session:
                obj: Events = (
                    transaction_session.query(Events)
                    .filter(Events.owner_id == user_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDEvents read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Events record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Events records]
        """
        try:
            logging.info("CRUDEvents read_all request")
            with session() as transaction_session:
                obj: Events = transaction_session.query(Events).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDEvents read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a Events record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDEvents update function")
            kwargs.update({"updated_at": datetime.now()})
            event_id = kwargs.get("event_id")
            del kwargs["event_id"]
            with session() as transaction_session:
                obj: Events = (
                    transaction_session.query(Events)
                    .filter(Events.id == event_id)
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDEvents update function : {error}")
            raise error

    def delete(self, event_id: str):
        """[CRUD function to delete a User record]

        Args:
            pricing_id (str): [Events Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDEvents delete function")
            with session() as transaction_session:
                obj: Events = (
                    transaction_session.query(Events)
                    .filter(Events.id == event_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDEvents delete function : {error}")
            raise error
