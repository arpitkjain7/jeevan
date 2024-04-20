from core import session, logger
from core.orm_models.hims_patientMedicalRecord import PatientMedicalRecord
from core.orm_models.hims_examinationFindings import ExaminationFindings
from core.orm_models.hims_diagnosis import Diagnosis
from core.orm_models.hims_medicines import Medicines
from core.orm_models.hims_labInvestigations import LabInvestigations
from core.orm_models.hims_precautions import Precautions
from core.orm_models.hims_hipDetails import HIPDetail
from core.orm_models.hims_appointments import Appointments
from core.orm_models.hims_patientDetails import PatientDetails
from core.orm_models.hims_docDetails import DocDetails
from core.orm_models.hims_vitals import Vital
from core.orm_models.hims_medicalHistory import MedicalHistory
from core.orm_models.hims_symptoms import Symptoms
from core.orm_models.hims_condition import Condition
from datetime import datetime
from pytz import timezone

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
                    "created_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    ),
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    ),
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
        """[CRUD function to read_new a PatientMedicalRecord record]

        Args:
            pmr_id (str): [PMR Id to filter PatientMedicalRecord]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientMedicalRecord record matching the criteria]
        """
        try:
            logging.info("CRUDPatientMedicalRecord read_new request")
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
                        LabInvestigations,
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
            logging.error(
                f"Error in CRUDPatientMedicalRecord read_new function : {error}"
            )
            raise error

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
            logging.info("CRUDPatientMedicalRecord read_by_docId request")
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
            logging.error(
                f"Error in CRUDPatientMedicalRecord read_by_docId function : {error}"
            )
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
            logging.error(
                f"Error in CRUDPatientMedicalRecord read_by_patientId function : {error}"
            )
            raise error

    def read_unlinked_by_patientId(self, patient_id: int):
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
            with session() as transaction_session:
                obj: PatientMedicalRecord = (
                    transaction_session.query(PatientMedicalRecord)
                    .filter(PatientMedicalRecord.patient_id == patient_id)
                    .filter(PatientMedicalRecord.abdm_linked == False)
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

    def read_by_appointmentId(self, appointment_id: int):
        """[CRUD function to read a PatientMedicalRecord record]

        Args:
            doc_id (str): [Doctor Id to filter PatientMedicalRecord]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientMedicalRecord record matching the criteria]
        """
        try:
            logging.info("CRUDPatientMedicalRecord read_by_docId request")
            with session() as transaction_session:
                obj: PatientMedicalRecord = (
                    transaction_session.query(PatientMedicalRecord)
                    .filter(PatientMedicalRecord.appointment_id == appointment_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalRecord read_by_docId function : {error}"
            )
            raise error

    def read_pmr_diagnosis_by_patientId(self, patient_id: int):
        """[CRUD function to read a PatientMedicalRecord record]

        Args:
            patient_id (str): [Patient Id to filter PatientMedicalRecord]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientMedicalRecord record matching the criteria]
        """
        try:
            logging.info(
                "CRUDPatientMedicalRecord read_pmr_diagnosis_by_patientId request"
            )
            """with session() as transaction_session:
                obj: PatientMedicalRecord = (
                    transaction_session.query(PatientMedicalRecord,Diagnosis)
                    .filter(PatientMedicalRecord.patient_id == patient_id)
                    .order_by(PatientMedicalRecord.date_of_consultation.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []"""

            with session() as transaction_session:
                joined_result = []
                for (
                    diagnosis_obj,
                    pmr_obj,
                ) in (
                    transaction_session.query(
                        Diagnosis,
                        PatientMedicalRecord,
                    )
                    .filter(PatientMedicalRecord.patient_id == patient_id)
                    .filter(Diagnosis.pmr_id == PatientMedicalRecord.id)
                    .all()
                ):
                    pmr_obj.__dict__.update(
                        {
                            "diagnosis_name": diagnosis_obj.__dict__["disease"],
                        }
                    )
                    joined_result.append(pmr_obj)
            return joined_result

        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalRecord read_by_patientId function : {error}"
            )
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
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: PatientMedicalRecord = (
                    transaction_session.query(PatientMedicalRecord)
                    .filter(PatientMedicalRecord.id == kwargs.get("id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
            if obj is not None:
                return kwargs.get("id")
            return []
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

    def read_details(self, pmr_id: str):
        try:
            logging.info("CRUDPatientMedicalRecord read_details request")
            with session() as transaction_session:
                joined_result = []
                for (
                    hip_obj,
                    doctor_obj,
                    appointment_obj,
                    patient_obj,
                    pmr_obj,
                ) in (
                    transaction_session.query(
                        HIPDetail,
                        DocDetails,
                        Appointments,
                        PatientDetails,
                        PatientMedicalRecord,
                    )
                    .filter(HIPDetail.hip_id == PatientMedicalRecord.hip_id)
                    .filter(DocDetails.id == PatientMedicalRecord.doc_id)
                    .filter(Appointments.id == PatientMedicalRecord.appointment_id)
                    .filter(PatientDetails.id == PatientMedicalRecord.patient_id)
                    .filter(PatientMedicalRecord.id == pmr_id)
                    .all()
                ):
                    pmr_obj.__dict__.update(
                        {
                            "hip": hip_obj.__dict__,
                            "doctor": doctor_obj.__dict__,
                            "appointment": appointment_obj.__dict__,
                            "patient": patient_obj.__dict__,
                        }
                    )
                    joined_result.append(pmr_obj.__dict__)
            return joined_result
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalRecord read_details function : {error}"
            )
            raise error

    def read_joined(self, pmr_id: str):
        try:
            logging.info(
                f"CRUDPatientMedicalRecord read_joined request for pmr_id: {pmr_id}"
            )
            with session() as transaction_session:
                # Diagnosis table
                diagnosis_results = (
                    transaction_session.query(Diagnosis)
                    .filter(Diagnosis.pmr_id == pmr_id)
                    .all()
                )
                diagnosis_list = [
                    diagnosis_obj.__dict__ for diagnosis_obj in diagnosis_results
                ]
                # Vitals table
                vital_results = (
                    transaction_session.query(Vital)
                    .filter(Vital.pmr_id == pmr_id)
                    .first()
                )
                # Examination Findings table
                examination_finding_results = (
                    transaction_session.query(ExaminationFindings)
                    .filter(ExaminationFindings.pmr_id == pmr_id)
                    .all()
                )
                examination_finding_list = [
                    examination_finding_obj.__dict__
                    for examination_finding_obj in examination_finding_results
                ]
                # Medicines table
                medicines_results = (
                    transaction_session.query(Medicines)
                    .filter(Medicines.pmr_id == pmr_id)
                    .all()
                )
                medicines_list = [
                    medicines_obj.__dict__ for medicines_obj in medicines_results
                ]
                # Medical History table
                medical_history_results = (
                    transaction_session.query(MedicalHistory)
                    .filter(MedicalHistory.pmr_id == pmr_id)
                    .all()
                )
                medical_history_list = [
                    medical_history_obj.__dict__
                    for medical_history_obj in medical_history_results
                ]
                # Symptoms table
                symptoms_results = (
                    transaction_session.query(Symptoms)
                    .filter(Symptoms.pmr_id == pmr_id)
                    .all()
                )
                symptoms_list = [
                    symptoms_obj.__dict__ for symptoms_obj in symptoms_results
                ]
                # Lab Investigation table
                lab_investigation_results = (
                    transaction_session.query(LabInvestigations)
                    .filter(LabInvestigations.pmr_id == pmr_id)
                    .all()
                )
                lab_investigation_list = [
                    lab_investigation_obj.__dict__
                    for lab_investigation_obj in lab_investigation_results
                ]
                # PatientMedicalRecord table
                pmr_obj = transaction_session.query(PatientMedicalRecord).get(pmr_id)
                pmr_dict = pmr_obj.__dict__

                pmr_dict.update(
                    {
                        "pmr_data": {
                            "vital": vital_results.__dict__ if vital_results else None,
                            "diagnosis": {"data": diagnosis_list},
                            "examination_findings": {"data": examination_finding_list},
                            "medication": {"data": medicines_list},
                            "medical_history": {"data": medical_history_list},
                            "lab_investigation": {"data": lab_investigation_list},
                            "symptom": {"data": symptoms_list},
                        }
                    }
                )
                return pmr_dict
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientMedicalRecord read_joined function: {error}"
            )
            raise
