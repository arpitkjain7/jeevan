from core import session, logger
from core.orm_models.hims_medicalTestReports import MedicalTestReports
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDMedicalTestReports:
    def create(self, **kwargs):
        """[CRUD function to create a new Appointment record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicalTestReports create request")
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
            medical_test_report = MedicalTestReports(**kwargs)
            with session() as transaction_session:
                transaction_session.add(medical_test_report)
                transaction_session.commit()
                transaction_session.refresh(medical_test_report)
        except Exception as error:
            logging.error(f"Error in CRUDMedicalTestReports create function : {error}")
            raise error

    def read_by_medicalTestId(self, medical_test_id: str):
        """[CRUD function to read a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDMedicalTestReports read request")
            with session() as transaction_session:
                obj: MedicalTestReports = (
                    transaction_session.query(MedicalTestReports)
                    .filter(MedicalTestReports.medical_test_id == medical_test_id)
                    .order_by(MedicalTestReports.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDMedicalTestReports read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Users record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all user records]
        """
        try:
            logging.info("CRUDMedicalTestReports read_all request")
            with session() as transaction_session:
                obj: MedicalTestReports = transaction_session.query(
                    MedicalTestReports
                ).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDMedicalTestReports read_all function : {error}"
            )
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicalTestReports update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: MedicalTestReports = (
                    transaction_session.query(MedicalTestReports)
                    .filter(MedicalTestReports.id == kwargs.get("id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDMedicalTestReports update function : {error}")
            raise error

    def delete(self, medical_test_report_id: int):
        """[CRUD function to delete a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicalTestReports delete function")
            with session() as transaction_session:
                obj: MedicalTestReports = (
                    transaction_session.query(MedicalTestReports)
                    .filter(MedicalTestReports.id == medical_test_report_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDMedicalTestReports delete function : {error}")
            raise error
