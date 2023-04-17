from core import session, logger
from core.orm_models.hims_patientVaccinationRecords import PatientVaccinationRecords
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDPatientVaccinationRecords:
    def create(self, **kwargs):
        """[CRUD function to create a new PatientVaccinationRecords record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientVaccinationRecords create request")
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
            patient_details = PatientVaccinationRecords(**kwargs)
            with session() as transaction_session:
                transaction_session.add(patient_details)
                transaction_session.commit()
                transaction_session.refresh(patient_details)
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientVaccinationRecords create function : {error}"
            )
            raise error

    def read_by_patientId(self, patient_id: int):
        """[CRUD function to read a PatientVaccinationRecords record]

        Args:
            patient_id (str): [patient_id to filter PatientVaccinationRecords]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientVaccinationRecords record matching the criteria]
        """
        try:
            logging.info("CRUDPatientVaccinationRecords read request")
            with session() as transaction_session:
                obj: PatientVaccinationRecords = (
                    transaction_session.query(PatientVaccinationRecords)
                    .filter(PatientVaccinationRecords.patient_id == patient_id)
                    .order_by(PatientVaccinationRecords.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientVaccinationRecords read function : {error}"
            )
            raise error

    def read_all(self):
        """[CRUD function to read_all PatientVaccinationRecords record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all PatientVaccinationRecords records]
        """
        try:
            logging.info("CRUDPatientVaccinationRecords read_all request")
            with session() as transaction_session:
                obj: PatientVaccinationRecords = (
                    transaction_session.query(PatientVaccinationRecords)
                    .order_by(PatientVaccinationRecords.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientVaccinationRecords read_all function : {error}"
            )
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a PatientVaccinationRecords record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientVaccinationRecords update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: PatientVaccinationRecords = (
                    transaction_session.query(PatientVaccinationRecords)
                    .filter(PatientVaccinationRecords.id == kwargs.get("id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientVaccinationRecords update function : {error}"
            )
            raise error

    def delete(self, vaccination_record_id: int):
        """[CRUD function to delete a PatientVaccinationRecords record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientVaccinationRecords delete function")
            with session() as transaction_session:
                obj: PatientVaccinationRecords = (
                    transaction_session.query(PatientVaccinationRecords)
                    .filter(PatientVaccinationRecords.id == vaccination_record_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientVaccinationRecords delete function : {error}"
            )
            raise error
