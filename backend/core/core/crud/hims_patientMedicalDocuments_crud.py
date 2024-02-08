from core import session, logger
from core.orm_models.hims_patientMedicalDocuments import PatientMedicalDocuments
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDPatientMedicalDocuments:
    def create(self, **kwargs):
        """[CRUD function to create a new PatientMedicalDocuments record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientMedicalDocuments create request")
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
            pmr_record = PatientMedicalDocuments(**kwargs)
            with session() as transaction_session:
                transaction_session.add(pmr_record)
                transaction_session.commit()
                transaction_session.refresh(pmr_record)
            return pmr_record.id
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalDocuments create function : {error}"
            )
            raise error

    def read(self, document_id: str):
        """[CRUD function to read a PatientMedicalDocuments record]

        Args:
            doc_id (str): [Doctor Id to filter PatientMedicalDocuments]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientMedicalDocuments record matching the criteria]
        """
        try:
            logging.info("CRUDPatientMedicalDocuments read request")
            with session() as transaction_session:
                obj: PatientMedicalDocuments = (
                    transaction_session.query(PatientMedicalDocuments)
                    .filter(PatientMedicalDocuments.id == document_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalDocuments read function : {error}"
            )
            raise error

    def read_by_type(self, pmr_id: str, document_type: str):
        """[CRUD function to read a PatientMedicalDocuments record]

        Args:
            doc_id (str): [Doctor Id to filter PatientMedicalDocuments]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientMedicalDocuments record matching the criteria]
        """
        try:
            logging.info("CRUDPatientMedicalDocuments read request")
            with session() as transaction_session:
                obj: PatientMedicalDocuments = (
                    transaction_session.query(PatientMedicalDocuments)
                    .filter(PatientMedicalDocuments.pmr_id == pmr_id)
                    .filter(PatientMedicalDocuments.document_type == document_type)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalDocuments read function : {error}"
            )
            raise error

    def read_by_pmr_id(self, pmr_id: int):
        """[CRUD function to read a PatientMedicalDocuments record]

        Args:
            doc_id (str): [Doctor Id to filter PatientMedicalDocuments]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientMedicalDocuments record matching the criteria]
        """
        try:
            logging.info("CRUDPatientMedicalDocuments read request")
            with session() as transaction_session:
                obj: PatientMedicalDocuments = (
                    transaction_session.query(PatientMedicalDocuments)
                    .filter(PatientMedicalDocuments.pmr_id == pmr_id)
                    .order_by(PatientMedicalDocuments.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalDocuments read function : {error}"
            )
            raise error

    def update(self, document_id, **kwargs):
        """[CRUD function to update a PatientMedicalDocuments record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientMedicalDocuments update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: PatientMedicalDocuments = (
                    transaction_session.query(PatientMedicalDocuments)
                    .filter(PatientMedicalDocuments.id == document_id)
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalDocuments update function : {error}"
            )
            raise error

    def delete(self, document_id: str):
        """[CRUD function to delete a PatientMedicalDocuments record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientMedicalDocuments delete function")
            with session() as transaction_session:
                obj: PatientMedicalDocuments = (
                    transaction_session.query(PatientMedicalDocuments)
                    .filter(PatientMedicalDocuments.id == document_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalDocuments delete function : {error}"
            )
            raise error
