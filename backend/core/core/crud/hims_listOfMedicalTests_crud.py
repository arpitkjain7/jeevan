from core import session, logger
from core.orm_models.hims_listOfMedicalTests import ListOfMedicalTests
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDListOfMedicalTests:
    def create(self, **kwargs):
        """[CRUD function to create a new Medical Tests record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDListOfMedicalTests create request")
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
            list_of_medical_tests = ListOfMedicalTests(**kwargs)
            with session() as transaction_session:
                transaction_session.add(list_of_medical_tests)
                transaction_session.commit()
                transaction_session.refresh(list_of_medical_tests)
            return list_of_medical_tests.id
        except Exception as error:
            logging.error(f"Error in CRUDListOfMedicalTests create function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Medical Tests record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Medical Tests records]
        """
        try:
            logging.info("CRUDListOfMedicalTests read_all request")
            with session() as transaction_session:
                obj: ListOfMedicalTests = transaction_session.query(
                    ListOfMedicalTests
                ).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDListOfMedicalTests read_all function : {error}"
            )
            raise error

    def read(self, medical_test_name: str):
        """[CRUD function to read Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Diagnosis records]
        """
        try:
            logging.info("CRUDListOfMedicalTests read request")
            with session() as transaction_session:
                obj: ListOfMedicalTests = (
                    transaction_session.query(ListOfMedicalTests)
                    .filter(ListOfMedicalTests.name == medical_test_name)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDListOfMedicalTests read function : {error}")
            raise error

    def delete(self, medical_test_id: int):
        """[CRUD function to delete a Medical Tests record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDListOfMedicalTests delete function")
            with session() as transaction_session:
                obj: ListOfMedicalTests = (
                    transaction_session.query(ListOfMedicalTests)
                    .filter(ListOfMedicalTests.id == medical_test_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDListOfMedicalTests delete function : {error}")
            raise error
