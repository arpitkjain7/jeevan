from core import session, logger
from core.orm_models.hims_patientMedicalRecord import PatientMedicalRecord
from core.orm_models.hims_complaint import Complaint
from core.orm_models.hims_diagnosis import Diagnosis
from core.orm_models.hims_medicines import Medicines
from core.orm_models.hims_medicalTest import MedicalTest
from core.orm_models.hims_precautions import Precautions
from datetime import datetime

logging = logger(__name__)


class CRUDPatientMedicalRecord:
    def create(self, **kwargs):
        """[CRUD function to create a new PatientMedicalRecord record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientMedicalRecord create request")
            kwargs.update(
                {
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            pmr_record = PatientMedicalRecord(**kwargs)
            with session() as transaction_session:
                transaction_session.add(pmr_record)
                transaction_session.commit()
                transaction_session.refresh(pmr_record)
            return pmr_record.id
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalRecord create function : {error}"
            )
            raise error

    def read_new(self, pmr_id: int):
        """[CRUD function to read a PatientMedicalRecord record]

        Args:
            pmr_id (str): [PMR Id to filter PatientMedicalRecord]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientMedicalRecord record matching the criteria]
        """
        try:
            logging.info("CRUDPatientMedicalRecord read request")
            with session() as transaction_session:
                joined_result = []
                for (
                    complaint_obj,
                    medicine_obj,
                    diagnosis_obj,
                    pmr_obj,
                    medicalTest_obj,
                ) in (
                    transaction_session.query(
                        Complaint,
                        Medicines,
                        Diagnosis,
                        PatientMedicalRecord,
                        MedicalTest,
                    )
                    .filter(Complaint.pmr_id == pmr_id)
                    .filter(MedicalTest.pmr_id == pmr_id)
                    .filter(Diagnosis.pmr_id == pmr_id)
                    .filter(Medicines.pmr_id == pmr_id)
                    .filter(PatientMedicalRecord.id == pmr_id)
                    .all()
                ):
                    pmr_obj.__dict__.update(
                        {
                            "complaints": complaint_obj,
                            "diagnosis": diagnosis_obj,
                            "medicines": medicine_obj,
                            "medicalTests": medicalTest_obj,
                        }
                    )
                    joined_result.append(pmr_obj)
            return joined_result
        except Exception as error:
            logging.error(f"Error in CRUDPatientMedicalRecord read function : {error}")
            raise error

    def read(self, pmr_id: int):
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
            with session() as transaction_session:
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

    def read_by_docId(self, doc_id: int):
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
            with session() as transaction_session:
                obj: PatientMedicalRecord = (
                    transaction_session.query(PatientMedicalRecord)
                    .filter(PatientMedicalRecord.doc_id == doc_id)
                    .order_by(PatientMedicalRecord.date_of_consultation.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
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
            logging.info("CRUDPatientMedicalRecord read request")
            with session() as transaction_session:
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
            logging.error(f"Error in CRUDPatientMedicalRecord read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all PatientMedicalRecord record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all PatientMedicalRecord records]
        """
        try:
            logging.info("CRUDPatientMedicalRecord read_all request")
            with session() as transaction_session:
                obj: PatientMedicalRecord = (
                    transaction_session.query(PatientMedicalRecord)
                    .order_by(PatientMedicalRecord.date_of_consultation.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalRecord read_all function : {error}"
            )
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a PatientMedicalRecord record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientMedicalRecord update function")
            kwargs.update({"updated_at": datetime.now()})
            with session() as transaction_session:
                obj: PatientMedicalRecord = (
                    transaction_session.query(PatientMedicalRecord)
                    .filter(PatientMedicalRecord.id == kwargs.get("id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalRecord update function : {error}"
            )
            raise error

    def delete(self, pmr_id: int):
        """[CRUD function to delete a PatientMedicalRecord record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientMedicalRecord delete function")
            with session() as transaction_session:
                obj: PatientMedicalRecord = (
                    transaction_session.query(PatientMedicalRecord)
                    .filter(PatientMedicalRecord.id == pmr_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalRecord delete function : {error}"
            )
            raise error
