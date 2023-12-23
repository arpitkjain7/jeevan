from core import session, logger
from core.orm_models.hims_vitals import Vital
from datetime import datetime
from pytz import timezone
from core.orm_models.hims_patientMedicalRecord import PatientMedicalRecord

logging = logger(__name__)


class CRUDVital:
    def create(self, **kwargs):
        """[CRUD function to create a new Vital record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDVital create request")
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
            vital = Vital(**kwargs)
            with session() as transaction_session:
                transaction_session.add(vital)
                transaction_session.commit()
                transaction_session.refresh(vital)
            return vital.id
        except Exception as error:
            logging.error(f"Error in CRUDVital create function : {error}")
            raise error

    def read_by_pmrId(self, pmr_id: int):
        """[CRUD function to read a vital record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Vital record matching the criteria]
        """
        try:
            logging.info("CRUDVital read request")
            with session() as transaction_session:
                obj: Vital = (
                    transaction_session.query(Vital)
                    .filter(Vital.pmr_id == pmr_id)
                    .order_by(Vital.created_at.desc())
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return []
        except Exception as error:
            logging.error(f"Error in CRUDVital read function : {error}")
            raise error

    def read_by_patientId(self, patient_id: int):
        """[CRUD function to read a vital record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Vital record matching the criteria]
        """
        try:
            logging.info("CRUDVital read request")
            with session() as transaction_session:
                obj: Vital = (
                    transaction_session.query(PatientMedicalRecord, Vital)
                    .join(PatientMedicalRecord, PatientMedicalRecord.id == Vital.pmr_id)
                    .filter(PatientMedicalRecord.patient_id == patient_id)
                    .order_by(Vital.created_at.desc())
                    .all()
                )
            logging.info(f"{obj=}")
            if obj is not None:
                vitals = [v for p, v in obj]
                return [v.__dict__ for v in vitals]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDVital read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Vital record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Vital records]
        """
        try:
            logging.info("CRUDVital read_all request")
            with session() as transaction_session:
                obj: Vital = transaction_session.query(Vital).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDVital read_all function : {error}")
            raise error

    def update(self, id: str, **kwargs):
        """[CRUD function to update a Vital record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDVital update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: Vital = (
                    transaction_session.query(Vital)
                    .filter(Vital.id == id)
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDVital update function : {error}")
            raise error

    def delete(self, vital_id: int):
        """[CRUD function to delete a Vital record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDVital delete function")
            with session() as transaction_session:
                obj: Vital = (
                    transaction_session.query(Vital)
                    .filter(Vital.id == vital_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDVital delete function : {error}")
            raise error

    def delete_all(self, pmr_id: str):
        """[CRUD function to delete_all  Vital record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDVital delete_all function")
            with session() as transaction_session:
                obj: Vital = (
                    transaction_session.query(Vital)
                    .filter(Vital.pmr_id == pmr_id)
                    .delete(synchronize_session=False)
                )
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDVital delete_all function : {error}")
            raise error
