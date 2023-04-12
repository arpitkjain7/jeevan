from core import session, logger
from core.orm_models.hims_listOfPrecautions import ListOfPrecautions
from datetime import datetime

logging = logger(__name__)


class CRUDListOfPrecautions:
    def create(self, **kwargs):
        """[CRUD function to create a new Precaution record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDListOfPrecautions create request")
            kwargs.update(
                {
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            list_of_precautions = ListOfPrecautions(**kwargs)
            with session() as transaction_session:
                transaction_session.add(list_of_precautions)
                transaction_session.commit()
                transaction_session.refresh(list_of_precautions)
        except Exception as error:
            logging.error(f"Error in CRUDListOfPrecautions create function : {error}")
            raise error


    def read_all(self):
        """[CRUD function to read_all Precaution record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Precaution records]
        """
        try:
            logging.info("CRUDListOfPrecautions read_all request")
            with session() as transaction_session:
                obj: ListOfPrecautions = transaction_session.query(ListOfPrecautions).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDListOfPrecautions read_all function : {error}")
            raise error
        
    def read(self, instruction_name: str):
        """[CRUD function to read Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Diagnosis records]
        """
        try:
            logging.info("CRUDListOfPrecautionsTests read request")
            with session() as transaction_session:
                obj: ListOfPrecautions = (
                    transaction_session.query(ListOfPrecautions)
                    .filter(ListOfPrecautions.instructions == instruction_name)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDListOfPrecautionsTests read function : {error}")
            raise error

    def delete(self, instruction_id: int):
        """[CRUD function to delete a Precaution record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDListOfPrecautions delete function")
            with session() as transaction_session:
                obj: ListOfPrecautions = (
                    transaction_session.query(ListOfPrecautions)
                    .filter(ListOfPrecautions.id == instruction_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDListOfPrecautions delete function : {error}")
            raise error
