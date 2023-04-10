from core import session, logger
from core.orm_models.hims_listOfMedicines import ListOfMedicines
from datetime import datetime

logging = logger(__name__)


class CRUDListOfMedicines:
    def create(self, **kwargs):
        """[CRUD function to create a new Medicine record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDListOfMedicines create request")
            kwargs.update(
                {
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            list_of_medicines = ListOfMedicines(**kwargs)
            with session() as transaction_session:
                transaction_session.add(list_of_medicines)
                transaction_session.commit()
                transaction_session.refresh(list_of_medicines)
            return list_of_medicines.id
        except Exception as error:
            logging.error(f"Error in CRUDListOfMedicines create function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Medicine record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Medicine records]
        """
        try:
            logging.info("CRUDListOfMedicines read_all request")
            with session() as transaction_session:
                obj: ListOfMedicines = transaction_session.query(ListOfMedicines).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDListOfMedicines read_all function : {error}")
            raise error

    def read(self, medicine: str):
        """[CRUD function to read Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Diagnosis records]
        """
        try:
            logging.info("CRUDListOfMedicines read request")
            with session() as transaction_session:
                obj: ListOfMedicines = (
                    transaction_session.query(ListOfMedicines)
                    .filter(ListOfMedicines.name == medicine)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDListOfMedicines read function : {error}")
            raise error

    def delete(self, medicine_id: int):
        """[CRUD function to delete a Medicine record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDListOfMedicines delete function")
            with session() as transaction_session:
                obj: ListOfMedicines = (
                    transaction_session.query(ListOfMedicines)
                    .filter(ListOfMedicines.id == medicine_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDListOfMedicines delete function : {error}")
            raise error
