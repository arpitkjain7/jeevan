from core import session, logger
from core.orm_models.hims_medicalTest import MedicalTest
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDMedicalTest:
    def create(self, **kwargs):
        """[CRUD function to create a new Medical Test record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicalTest create request")
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
            medical_test = MedicalTest(**kwargs)
            with session() as transaction_session:
                transaction_session.add(medical_test)
                transaction_session.commit()
                transaction_session.refresh(medical_test)
        except Exception as error:
            logging.error(f"Error in CRUDMedicalTest create function : {error}")
            raise error

    def read_by_pmrId(self, pmr_id: str):
        """[CRUD function to read a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDMedicalTest read request")
            with session() as transaction_session:
                obj: MedicalTest = (
                    transaction_session.query(MedicalTest)
                    .filter(MedicalTest.pmr_id == pmr_id)
                    .order_by(MedicalTest.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDMedicalTest read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Users record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all user records]
        """
        try:
            logging.info("CRUDMedicalTest read_all request")
            with session() as transaction_session:
                obj: MedicalTest = transaction_session.query(MedicalTest).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDMedicalTest read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicalTest update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: MedicalTest = (
                    transaction_session.query(MedicalTest)
                    .filter(MedicalTest.id == kwargs.get("id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDMedicalTest update function : {error}")
            raise error

    def delete(self, medical_test_id: int):
        """[CRUD function to delete a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicalTest delete function")
            with session() as transaction_session:
                obj: MedicalTest = (
                    transaction_session.query(MedicalTest)
                    .filter(MedicalTest.id == medical_test_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDMedicalTest delete function : {error}")
            raise error

    def delete_all(self, pmr_id: str):
        """[CRUD function to delete_all a Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicalTest delete_all function")
            with session() as transaction_session:
                obj: MedicalTest = (
                    transaction_session.query(MedicalTest)
                    .filter(MedicalTest.pmr_id == pmr_id)
                    .delete(synchronize_session=False)
                )
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDMedicalTest delete_all function : {error}")
            raise error
