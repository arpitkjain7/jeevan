from core import session, logger
from core.orm_models.hims_listOfDiagnosis import ListOfDiagnosis
from datetime import datetime

logging = logger(__name__)


class CRUDListOfDiagosis:
    def create(self, **kwargs):
        """[CRUD function to create a new Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDListOfDiagosis create request")
            kwargs.update(
                {
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            list_of_diagnosis = ListOfDiagnosis(**kwargs)
            with session() as transaction_session:
                transaction_session.add(list_of_diagnosis)
                transaction_session.commit()
                transaction_session.refresh(list_of_diagnosis)
        except Exception as error:
            logging.error(f"Error in CRUDListOfDiagosis create function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Diagnosis records]
        """
        try:
            logging.info("CRUDListOfDiagosis read_all request")
            with session() as transaction_session:
                obj: ListOfDiagnosis = transaction_session.query(ListOfDiagnosis).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDListOfDiagosis read_all function : {error}")
            raise error

    def read(self, disease: str):
        """[CRUD function to read Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Diagnosis records]
        """
        try:
            logging.info("CRUDListOfDiagnosis read request")
            with session() as transaction_session:
                obj: ListOfDiagnosis = (
                    transaction_session.query(ListOfDiagnosis)
                    .filter(ListOfDiagnosis.disease == disease)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDListOfDiagnosis read function : {error}")
            raise error

    def delete(self, disease_id: int):
        """[CRUD function to delete a Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDListOfDiagosis delete function")
            with session() as transaction_session:
                obj: ListOfDiagnosis = (
                    transaction_session.query(ListOfDiagnosis)
                    .filter(ListOfDiagnosis.id == disease_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDListOfDiagosis delete function : {error}")
            raise error
