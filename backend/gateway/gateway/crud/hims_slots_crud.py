from gateway import create_session, logger
from gateway.orm_models.hospital_schema.slots import Slots
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDSlots:
    def create(self, **kwargs):
        """[CRUD function to create a new User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDSlots create request")
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
            slots_details = Slots(**kwargs)
            with create_session() as transaction_session:
                transaction_session.add(slots_details)
                transaction_session.commit()
                transaction_session.refresh(slots_details)
            return slots_details.slot_id
        except Exception as error:
            logging.error(f"Error in CRUDSlots create function : {error}")
            raise error

    def read(self, slot_id: int):
        """[CRUD function to read a User record]

        Args:
            slot_id (int): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDSlots read request")
            with create_session() as transaction_session:
                obj: Slots = (
                    transaction_session.query(Slots)
                    .filter(Slots.slot_id == slot_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDSlots read function : {error}")
            raise error

    def read_by_doc_id(self, doc_id: str, appointment_date: str):
        """[CRUD function to read a User record]

        Args:
            slot_id (int): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDSlots read request")
            with create_session() as transaction_session:
                obj: Slots = (
                    transaction_session.query(Slots)
                    .filter(Slots.doc_id == doc_id)
                    .filter(Slots.date == appointment_date)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDSlots read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Users record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all user records]
        """
        try:
            logging.info("CRUDSlots read_all request")
            with create_session() as transaction_session:
                obj: Slots = transaction_session.query(Slots).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDSlots read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDSlots update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with create_session() as transaction_session:
                obj: Slots = (
                    transaction_session.query(Slots)
                    .filter(Slots.slot_id == kwargs.get("slot_id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDSlots update function : {error}")
            raise error

    def delete(self, slot_id: int):
        """[CRUD function to delete a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDSlots delete function")
            with create_session() as transaction_session:
                obj: Slots = (
                    transaction_session.query(Slots)
                    .filter(Slots.slot_id == slot_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDSlots delete function : {error}")
            raise error
