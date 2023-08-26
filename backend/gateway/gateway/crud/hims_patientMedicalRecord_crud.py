from gateway import create_session, logger
from gateway.orm_models.hospital_schema.patientMedicalRecord import PatientMedicalRecord
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDPatientMedicalRecord:
    def read(self, pmr_id: str):
        """[CRUD function to read a PatientMedicalRecord record]

        Args:
            doc_id (str): [Doctor Id to filter PatientMedicalRecord]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientMedicalRecord record matching the criteria]
        """
        try:
            logging.info("CRUDPatientMedicalRecord read request")
            with create_session() as transaction_session:
                obj: PatientMedicalRecord = (
                    transaction_session.query(PatientMedicalRecord)
                    .filter(PatientMedicalRecord.id == pmr_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDPatientMedicalRecord read function : {error}")
            raise error

    def read_by_patientId(self, patient_id: int):
        """[CRUD function to read a PatientMedicalRecord record]

        Args:
            patient_id (str): [Patient Id to filter PatientMedicalRecord]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientMedicalRecord record matching the criteria]
        """
        try:
            logging.info("CRUDPatientMedicalRecord read_by_patientId request")
            with create_session() as transaction_session:
                obj: PatientMedicalRecord = (
                    transaction_session.query(PatientMedicalRecord)
                    .filter(PatientMedicalRecord.patient_id == patient_id)
                    .order_by(PatientMedicalRecord.date_of_consultation.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalRecord read_by_patientId function : {error}"
            )
            raise error

    def update(self, pmr_id, **kwargs):
        """[CRUD function to update a PatientMedicalRecord record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientMedicalRecord update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with create_session() as transaction_session:
                obj: PatientMedicalRecord = (
                    transaction_session.query(PatientMedicalRecord)
                    .filter(PatientMedicalRecord.id == pmr_id)
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
            if obj is not None:
                return pmr_id
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalRecord update function : {error}"
            )
            raise error
