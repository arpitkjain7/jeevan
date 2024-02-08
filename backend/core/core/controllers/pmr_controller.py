from core.crud.hims_vitals_crud import CRUDVital
from core.crud.hims_examination_findings_crud import CRUDExaminationFindings
from core.crud.hims_diagnosis_crud import CRUDDiagnosis
from core.crud.hims_appointments_crud import CRUDAppointments
from core.crud.hims_labInvestigation_crud import CRUDLabInvestigation
from core.crud.hims_medicines_crud import CRUDMedicines
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from core.crud.hims_medicalHistory_crud import CRUDMedicalHistory
from core.crud.hims_medicalTestReports_crud import CRUDMedicalTestReports
from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hims_current_medicines_crud import CRUDCurrentMedicines
from core.utils.custom.external_call import APIInterface
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.crud.hims_symptoms_crud import CRUDSymptoms
from core.crud.hims_condition_crud import CRUDCondition
from core.crud.hims_patientMedicalDocuments_crud import CRUDPatientMedicalDocuments
from core.crud.hims_hip_crud import CRUDHIP
from core.utils.fhir.op_consult import opConsultUnstructured
from core.utils.aws.s3_helper import upload_to_s3, create_presigned_url, read_object
from core.utils.custom.session_helper import get_session_token
from core.utils.custom.gupshup_helper import whatsappHelper
from core.utils.custom.prescription_helper import create_pdf_from_images, merge_pdf
from core.utils.custom.msg91_helper import smsHelper
from core import logger
import base64
from datetime import datetime, timezone
from urllib.parse import quote
import uuid, os
from pytz import timezone as pytz_timezone

logging = logger(__name__)


class PMRController:
    def __init__(self):
        self.gateway_url = os.environ["gateway_url"]
        self.cliniq_bucket = os.environ["s3_location"]
        self.CRUDExaminationFindings = CRUDExaminationFindings()
        self.CRUDDiagnosis = CRUDDiagnosis()
        self.CRUDAppointments = CRUDAppointments()
        self.CRUDLabInvestigation = CRUDLabInvestigation()
        self.CRUDMedicines = CRUDMedicines()
        self.CRUDPatientMedicalRecord = CRUDPatientMedicalRecord()
        self.CRUDPatientDetails = CRUDPatientDetails()
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDMedicalHistory = CRUDMedicalHistory()
        self.CRUDMedicalTestReports = CRUDMedicalTestReports()
        self.CRUDVital = CRUDVital()
        self.CRUDSymptoms = CRUDSymptoms()
        self.CRUDCurrentMedicines = CRUDCurrentMedicines()
        self.CRUDCondition = CRUDCondition()
        self.CRUDPatientMedicalDocuments = CRUDPatientMedicalDocuments()
        self.CRUDHIP = CRUDHIP()
        self.mime_type_mapping = {
            "pdf": "application/pdf",
            "jpeg": "image/jpg",
            "jpg": "image/jpg",
            "png": "image/png",
        }
        self.abha_url = os.environ["abha_url"]

    def get_pmr(self, pmr_id: str):
        """[Controller to create new pmr record]

        Args:
            pmr_id ([str]): [pmr id for getting pmr records]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing get pmr function")
            logging.info(f"Getting the PMR record for {pmr_id=}")
            return self.CRUDPatientMedicalRecord.read_joined(pmr_id=pmr_id)
        except Exception as error:
            logging.error(
                f"Error in PMRController.get_pmr_controller function: {error}"
            )
            raise error

    def create_pmr(self, request):
        """[Controller to create new pmr record]

        Args:
            request ([dict]): [create new pmr request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing create new pmr function")
            request_dict = request.dict()
            pmr_obj = self.CRUDPatientMedicalRecord.read_by_appointmentId(
                appointment_id=request_dict.get("appointment_id")
            )
            logging.debug(f"{pmr_obj=}")
            if pmr_obj is None:
                pmr_id = f"C360-PMR-{str(uuid.uuid1().int)[:18]}"
                appointment_obj = self.CRUDAppointments.read(
                    appointment_id=request_dict.get("appointment_id")
                )
                logging.info(f"{appointment_obj=}")
                consultation_date = appointment_obj.get("slot_details").get("date")
                logging.info(f"{consultation_date=}")
                request_dict.update(
                    {
                        "id": pmr_id,
                        "date_of_consultation": consultation_date,
                    }
                )
                logging.info("Creating PMR record")
                logging.info(f"PMR: {request_dict=}")
                pmr_id = self.CRUDPatientMedicalRecord.create(**request_dict)
                logging.info(f"PMR record created with PMR_ID = {pmr_id}")
            else:
                logging.info("PMR object already exist")
                pmr_id = pmr_obj.get("id")
            # TODO: Optimise the function to reduce additional query
            pmr_details = self.CRUDPatientMedicalRecord.read_joined(pmr_id=pmr_id)
            appointment_details = self.CRUDAppointments.read(
                request_dict.get("appointment_id")
            )
            return {
                "pmr_details": pmr_details,
                "appointment_details": appointment_details,
            }
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_pmr_controller function: {error}"
            )
            raise error

    def create_pmr_v2(self, request):
        """[Controller to create new pmr record and update consultation status]

        Args:
            request ([dict]): [create new pmr request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing create_pmr_v2 function")
            request_dict = request.dict()
            pmr_obj = self.CRUDPatientMedicalRecord.read_by_appointmentId(
                appointment_id=request_dict.get("appointment_id")
            )
            logging.debug(f"{pmr_obj=}")
            consultation_status = request_dict.pop("consultation_status")
            if pmr_obj is None:
                pmr_id = f"C360-PMR-{str(uuid.uuid1().int)[:18]}"
                appointment_obj = self.CRUDAppointments.read(
                    appointment_id=request_dict.get("appointment_id")
                )
                logging.info(f"{appointment_obj=}")
                consultation_date = appointment_obj.get("slot_details").get("date")
                logging.info(f"{consultation_date=}")
                request_dict.update(
                    {
                        "id": pmr_id,
                        "date_of_consultation": consultation_date,
                    }
                )
                logging.info("Creating PMR record")
                logging.info(f"PMR: {request_dict=}")
                pmr_id = self.CRUDPatientMedicalRecord.create(**request_dict)
                logging.info(f"PMR record created with PMR_ID = {pmr_id}")
            else:
                logging.info("PMR object already exist")
                pmr_id = pmr_obj.get("id")
            logging.info("Updating consultation status")
            logging.info(
                f"Consultation Status: {request_dict=}, PMR: {request_dict.get('appointment_id')=}"
            )
            self.CRUDAppointments.update(
                **{
                    "id": request_dict.get("appointment_id"),
                    "consultation_status": consultation_status,
                },
            )
            # TODO: Optimise the function to reduce additional query
            pmr_details = self.CRUDPatientMedicalRecord.read_joined(pmr_id=pmr_id)
            appointment_details = self.CRUDAppointments.read(
                request_dict.get("appointment_id")
            )
            return {
                "pmr_details": pmr_details,
                "appointment_details": appointment_details,
            }
        except Exception as error:
            logging.error(f"Error in PMRController.create_pmr_v2 function: {error}")
            raise error

    def update_pmr(self, request):
        """[Controller to update pmr record]

        Args:
            request ([dict]): [update pmr request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing update pmr function")
            request_dict = request.dict()
            logging.info(f"PMR: {request_dict=}")
            self.CRUDPatientMedicalRecord.update(**request_dict)
            return {"pmr_id": request.id}
        except Exception as error:
            logging.error(
                f"Error in PMRController.update_pmr_controller function: {error}"
            )
            raise error

    def create_vital(self, request):
        try:
            logging.info("Creating vital records")
            vital_obj_dict = request.data.dict()
            vital_obj_dict.update({"pmr_id": request.pmr_id})
            vital_id = self.CRUDVital.create(**vital_obj_dict)
            return {"pmr_id": request.pmr_id, "vital_id": vital_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_vital function: {error}")
            raise error

    def create_vital_pmr(self, request, pmr_id):
        try:
            logging.info("Creating vital records")
            logging.info(f"{request=}")
            vital_obj_dict = request.dict()
            logging.info(f"{vital_obj_dict=}")
            vital_db_dict = vital_obj_dict.copy()
            vital_db_dict.update({"pmr_id": pmr_id})
            logging.info(f"{vital_db_dict=}")
            vital_dict = self.CRUDVital.read_by_pmrId(pmr_id=pmr_id)
            logging.info(f"{vital_dict=}")
            if vital_dict is None:
                vital_id = self.CRUDVital.create(**vital_db_dict)
                logging.info(f"{vital_id=}")
                vital_obj_dict.update({"id": vital_id})
                return vital_obj_dict
            self.CRUDVital.update_by_pmr_id(**vital_db_dict)
            logging.debug(f"{vital_db_dict=}")
            return vital_obj_dict
        except Exception as error:
            logging.error(f"Error in PMRController.create_vital function: {error}")
            raise error

    def create_examination_findings(self, request, pmr_id):
        try:
            logging.info("Creating examination findings records")
            examination_records = []
            for examination_findings_obj in request.data:
                examination_findings_obj_dict = examination_findings_obj.dict()
                logging.info(f"{examination_findings_obj_dict=}")
                examination_findings_obj_dict.update({"pmr_id": pmr_id})
                examination_finding_exists = examination_findings_obj_dict.get(
                    "id", None
                )
                if examination_finding_exists:
                    self.CRUDExaminationFindings.update(**examination_findings_obj_dict)
                    examination_records.append(examination_findings_obj_dict)
                else:
                    examination_findings_id = self.CRUDExaminationFindings.create(
                        **examination_findings_obj_dict
                    )
                    logging.info(f"{examination_findings_id=}")
                    examination_findings_obj_dict.update(
                        {"id": examination_findings_id}
                    )
                    examination_records.append(examination_findings_obj_dict)
            logging.info(f"{examination_records=}")
            return examination_records
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_examination_findings function: {error}"
            )
            raise error

    def create_examination_findings_v1(self, request, pmr_id):
        try:
            logging.info("create_examination_findings_v1 records")
            examination_records = []
            self.CRUDExaminationFindings.delete_all(pmr_id=pmr_id)
            for examination_findings_obj in request.data:
                examination_findings_obj_dict = examination_findings_obj.dict()
                examination_findings_obj_dict.update({"pmr_id": pmr_id})
                logging.info(f"{examination_findings_obj_dict=}")
                examination_findings_id = self.CRUDExaminationFindings.create(
                    **examination_findings_obj_dict
                )
                logging.info(f"{examination_findings_id=}")
                examination_findings_obj_dict.update({"id": examination_findings_id})
                examination_records.append(examination_findings_obj_dict)
            logging.info(f"{examination_records=}")
            return examination_records
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_examination_findings_v1 function: {error}"
            )
            raise error

    def create_diagnosis(self, request, pmr_id):
        try:
            logging.info("Creating diagnosis records")
            diagnosis_records = []
            for diagnosis_obj in request.data:
                diagnosis_obj_dict = diagnosis_obj.dict()
                diagnosis_obj_dict.update({"pmr_id": pmr_id})
                diagnosis_obj_exists = diagnosis_obj_dict.get("id", None)
                if diagnosis_obj_exists:
                    self.CRUDDiagnosis.update(**diagnosis_obj_dict)
                    diagnosis_records.append(diagnosis_obj_dict["id"])
                else:
                    diagnosis_id = self.CRUDDiagnosis.create(**diagnosis_obj_dict)
                    logging.info(f"{diagnosis_id=}")
                    diagnosis_records.append(diagnosis_id)
            logging.info(f"{diagnosis_records=}")
            return diagnosis_records
        except Exception as error:
            logging.error(f"Error in PMRController.create_diagnosis function: {error}")
            raise error

    def create_diagnosis_v1(self, request, pmr_id):
        try:
            logging.info("create_diagnosis_v1 records")
            diagnosis_records = []
            self.CRUDDiagnosis.delete_all(pmr_id=pmr_id)
            for diagnosis_obj in request.data:
                diagnosis_obj_dict = diagnosis_obj.dict()
                diagnosis_obj_dict.update({"pmr_id": pmr_id})
                diagnosis_id = self.CRUDDiagnosis.create(**diagnosis_obj_dict)
                logging.info(f"{diagnosis_id=}")
                diagnosis_obj_dict.update({"id": diagnosis_id})
                diagnosis_records.append(diagnosis_obj_dict)
            logging.info(f"{diagnosis_records=}")
            return diagnosis_records
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_diagnosis_v1 function: {error}"
            )
            raise error

    def create_symptoms(self, request, pmr_id):
        try:
            logging.info("Creating symptoms records")
            symptom_records = []
            for symptoms_obj in request.data:
                symptoms_obj_dict = symptoms_obj.dict()
                symptoms_obj_dict.update({"pmr_id": pmr_id})
                symptoms_record_exists = symptoms_obj_dict.get("id", None)
                if symptoms_record_exists:
                    self.CRUDSymptoms.update(**symptoms_obj_dict)
                    symptom_records.append(symptoms_obj_dict["id"])
                else:
                    symptoms_id = self.CRUDSymptoms.create(**symptoms_obj_dict)
                    logging.info(f"{symptoms_id=}")
                    symptom_records.append(symptoms_id)
            logging.info(f"{symptom_records=}")
            return symptom_records
        except Exception as error:
            logging.error(f"Error in PMRController.create_symptoms function: {error}")
            raise error

    def create_symptoms_v1(self, request, pmr_id):
        try:
            logging.info("create_symptoms_v1 records")
            symptom_records = []
            self.CRUDSymptoms.delete_all(pmr_id=pmr_id)
            for symptoms_obj in request.data:
                symptoms_obj_dict = symptoms_obj.dict()
                symptoms_obj_dict.update({"pmr_id": pmr_id})
                symptoms_id = self.CRUDSymptoms.create(**symptoms_obj_dict)
                symptoms_obj_dict.update({"id": symptoms_id})
                symptom_records.append(symptoms_obj_dict)
            logging.info(f"{symptom_records=}")
            return symptom_records
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_symptoms_v1 function: {error}"
            )
            raise error

    def create_medication(self, request, pmr_id):
        try:
            logging.info("Creating medicines records")
            medicines_records = []
            for medicines_obj in request.data:
                medicines_obj_dict = medicines_obj.dict()
                medicines_obj_dict.update({"pmr_id": pmr_id})
                medicines_obj_exists = medicines_obj_dict.get("id", None)
                if medicines_obj_exists:
                    self.CRUDMedicines.update(**medicines_obj_dict)
                    medicines_records.append(medicines_obj_dict["id"])
                else:
                    medicines_id = self.CRUDMedicines.create(**medicines_obj_dict)
                    logging.info(f"{medicines_id=}")
                    medicines_records.append(medicines_id)
            logging.info(f"{medicines_records=}")
            return medicines_records
        except Exception as error:
            logging.error(f"Error in PMRController.create_medication function: {error}")
            raise error

    def create_medication_v1(self, request, pmr_id):
        try:
            logging.info("Creating medicines records")
            medicines_records = []
            self.CRUDMedicines.delete_all(pmr_id=pmr_id)
            for medicines_obj in request.data:
                medicines_obj_dict = medicines_obj.dict()
                medicines_obj_dict.update({"pmr_id": pmr_id})
                medicines_id = self.CRUDMedicines.create(**medicines_obj_dict)
                medicines_obj_dict.update({"id": medicines_id})
                medicines_records.append(medicines_obj_dict)
            logging.info(f"{medicines_records=}")
            return medicines_records
        except Exception as error:
            logging.error(f"Error in PMRController.create_medication function: {error}")
            raise error

    def create_current_medication(self, request, pmr_id):
        try:
            logging.info("Creating curremt medicines records")
            resp = []
            for current_medicines_obj in request.data:
                current_medicines_obj_dict = current_medicines_obj.dict()
                current_medicines_obj_dict.update({"pmr_id": pmr_id})
                current_medicines_dict = self.CRUDCurrentMedicines.read_by_pmrId(
                    pmr_id=pmr_id
                )
                if current_medicines_dict == []:
                    current_medicines_id = self.CRUDCurrentMedicines.create(
                        **current_medicines_obj_dict
                    )
                    logging.info(f"{current_medicines_id=}")
                else:
                    self.CRUDCurrentMedicines.update(
                        **current_medicines_obj_dict,
                        id=current_medicines_dict["id"],
                    )
                    logging.debug(f"{current_medicines_dict}")
                    current_medicines_id = current_medicines_dict["id"]

                resp.append(
                    {
                        "pmr_id": pmr_id,
                        "current_medicines_id": current_medicines_id,
                    }
                )
            return resp
        except Exception as error:
            logging.error(f"Error in PMRController.create_medication function: {error}")
            raise error

    def update_current_medication(self, request):
        try:
            logging.info("Updating current medicine records")
            for current_medicines_obj in request.data:
                current_medicines_obj_dict = current_medicines_obj.dict()
                self.CRUDCurrentMedicines.update(
                    **current_medicines_obj_dict, id=request.id
                )
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(
                f"Error in PMRController.update_current_medication function: {error}"
            )
            raise error

    def create_labInvestigation(self, request, pmr_id):
        try:
            logging.info("Creating lab investigation records")
            lab_investigation_records = []
            for lab_investigation_obj in request.data:
                lab_investigation_obj_dict = lab_investigation_obj.dict()
                lab_investigation_obj_dict.update({"pmr_id": pmr_id})
                lab_investigation_exists = lab_investigation_obj_dict.get("id", None)
                if lab_investigation_exists:
                    self.CRUDLabInvestigation.update(**lab_investigation_obj_dict)
                    lab_investigation_records.append(lab_investigation_obj_dict["id"])
                else:
                    lab_investigation_id = self.CRUDLabInvestigation.create(
                        **lab_investigation_obj_dict
                    )
                    lab_investigation_records.append(lab_investigation_id)
            logging.info(f"{lab_investigation_records=}")
            return lab_investigation_records
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_labInvestigation function: {error}"
            )
            raise error

    def create_labInvestigation_v1(self, request, pmr_id):
        try:
            logging.info("create_labInvestigation_v1 records")
            lab_investigation_records = []
            self.CRUDLabInvestigation.delete_all(pmr_id=pmr_id)
            for lab_investigation_obj in request.data:
                lab_investigation_obj_dict = lab_investigation_obj.dict()
                lab_investigation_obj_dict.update({"pmr_id": pmr_id})
                lab_investigation_id = self.CRUDLabInvestigation.create(
                    **lab_investigation_obj_dict
                )
                lab_investigation_obj_dict.update({"id": lab_investigation_id})
                lab_investigation_records.append(lab_investigation_obj_dict)
            logging.info(f"{lab_investigation_records=}")
            return lab_investigation_records
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_labInvestigation_v1 function: {error}"
            )
            raise error

    def create_medicalHistory(self, request, pmr_id):
        try:
            logging.info("Creating medical history records")
            logging.info(f"{request=}")
            medical_history_records = []
            for medical_history_obj in request.data:
                medical_history_obj_dict = medical_history_obj.dict()
                medical_history_obj_dict.update({"pmr_id": pmr_id})
                logging.info(f"{medical_history_obj_dict=}")
                medical_history_exists = medical_history_obj_dict.get("id", None)
                if medical_history_exists:
                    self.CRUDMedicalHistory.update(**medical_history_obj_dict)
                    medical_history_records.append(medical_history_obj_dict["id"])
                else:
                    medical_history_id = self.CRUDMedicalHistory.create(
                        **medical_history_obj_dict
                    )
                    logging.info(f"{medical_history_id=}")
                    medical_history_records.append(medical_history_id)
            logging.info(f"{medical_history_records=}")
            return medical_history_records
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_medical_history function: {error}"
            )
            raise error

    def create_medicalHistory_v1(self, request, pmr_id):
        try:
            logging.info("create_medicalHistory_v1 records")
            logging.info(f"{request=}")
            medical_history_records = []
            self.CRUDMedicalHistory.delete_all(pmr_id=pmr_id)
            for medical_history_obj in request.data:
                medical_history_obj_dict = medical_history_obj.dict()
                medical_history_obj_dict.update({"pmr_id": pmr_id})
                logging.info(f"{medical_history_obj_dict=}")
                medical_history_id = self.CRUDMedicalHistory.create(
                    **medical_history_obj_dict
                )
                medical_history_obj_dict.update({"id": medical_history_id})
                medical_history_records.append(medical_history_obj_dict)
            logging.info(f"{medical_history_records=}")
            return medical_history_records
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_medicalHistory_v1 function: {error}"
            )
            raise error

    def create_advice(self, request, pmr_id):
        try:
            logging.info("Creating advice records")
            advice_obj_dict = request.dict()
            advice_obj_dict.update({"id": pmr_id})
            logging.info(f"{advice_obj_dict=}")
            # pmr_id = advice_obj_dict.pop("pmr_id")
            logging.info(f"{advice_obj_dict=}")
            self.CRUDPatientMedicalRecord.update(**advice_obj_dict)
            return {"pmr_id": pmr_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_advice function: {error}")
            raise error

    def create_notes(self, request, pmr_id):
        try:
            logging.info("Creating notes records")
            notes_obj_dict = request.dict()
            notes_obj_dict.update({"id": pmr_id})
            # pmr_id = notes_obj_dict.pop("pmr_id")
            logging.info(f"{notes_obj_dict=}")
            self.CRUDPatientMedicalRecord.update(**notes_obj_dict)
            return {"pmr_id": pmr_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_notes function: {error}")
            raise error

    def get_pmr_with_patientId(self, patient_id: str):
        """[Controller to create new pmr record]

        Args:
            patient_id ([str]): [patient id for getting pmr records]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing get pmr function")
            logging.info(f"Getting the PMR record for {patient_id=}")
            pmr_list = self.CRUDPatientMedicalRecord.read_by_patientId(
                patient_id=patient_id
            )
            response = []
            for pmr_obj in pmr_list:
                diagnosis_obj_list = self.CRUDDiagnosis.read_by_pmrId(
                    pmr_id=pmr_obj["id"]
                )
                appointment_obj = self.CRUDAppointments.read(
                    appointment_id=pmr_obj["appointment_id"]
                )
                consultation_status = appointment_obj["consultation_status"]
                logging.debug(f"{consultation_status=}")
                # if consultation_status == "Completed":
                # removing check to return only completed consultation
                diagnosis_length = len(diagnosis_obj_list)
                if diagnosis_length == 1:
                    diagnosis_name = f"{diagnosis_obj_list[0]['disease']}"
                elif diagnosis_length >= 2:
                    diagnosis_name = f"{diagnosis_obj_list[0]['disease']} | {diagnosis_obj_list[1]['disease']}"
                else:
                    diagnosis_name = "Diagnosis"
                pmr_obj.update(
                    {
                        "diagnosis_name": diagnosis_name,
                        "consultation_status": consultation_status,
                    }
                )

                response.append(pmr_obj)
            return response
        except Exception as error:
            logging.error(
                f"Error in PMRController.get_pmr_controller function: {error}"
            )
            raise error

    def get_pmr(self, pmr_id: str):
        """[Controller to create new pmr record]

        Args:
            pmr_id ([str]): [pmr id for getting pmr records]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing get pmr function")
            logging.info(f"Getting the PMR record for {pmr_id=}")
            pmr_metadata = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
            vitals_data = self.CRUDVital.read_by_pmrId(pmr_id=pmr_id)
            examination_findings_data = self.CRUDExaminationFindings.read_by_pmrId(
                pmr_id=pmr_id
            )
            diagnosis_data = self.CRUDDiagnosis.read_by_pmrId(pmr_id=pmr_id)
            medicine_data = self.CRUDMedicines.read_by_pmrId(pmr_id=pmr_id)
            medicalHistory_data = self.CRUDMedicalHistory.read_by_pmrId(pmr_id=pmr_id)
            condition = self.CRUDCondition.read_by_pmrId(pmr_id=pmr_id)
            symptoms = self.CRUDSymptoms.read_by_pmrId(pmr_id=pmr_id)
            pmr_metadata.update(
                {
                    "vitals": vitals_data,
                    "examination_findings": examination_findings_data,
                    "conditions": condition,
                    "diagnosis": diagnosis_data,
                    "symptoms": symptoms,
                    "medicines": medicine_data,
                    "medicalHistory": medicalHistory_data,
                }
            )
            return pmr_metadata
        except Exception as error:
            logging.error(
                f"Error in PMRController.get_pmr_controller function: {error}"
            )
            raise error

    def sync_pmr(self, pmr_id, hip_id):
        """[Sync PMR record with gateway]

        Args:
            request ([dict]): [create new pmr request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing sync_pmr new pmr function")
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            pmr_obj = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
            date_of_consultation = pmr_obj["date_of_consultation"].strftime(
                "%Y-%m-%dT%H:%M:%S.%f"
            )
            patient_id = pmr_obj.get("patient_id")
            patient_obj = self.CRUDPatientDetails.read_by_patientId(
                patient_id=patient_id
            )
            access_token = patient_obj.get("access_token").get("value")
            access_token_validity = patient_obj.get("access_token").get("valid_till")
            access_token_validity = datetime.strptime(
                access_token_validity, "%m/%d/%Y, %H:%M:%S"
            )
            request_id = str(uuid.uuid1())
            if pmr_obj["abdm_linked"]:
                logging.info("PMR already linked")
                care_context_url = f"{self.gateway_url}/v0.5/links/context/notify"
                payload = {
                    "requestId": request_id,
                    "timestamp": datetime.now(timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%S.%f"
                    ),
                    "notification": {
                        "patient": {"id": patient_obj["abha_address"]},
                        "careContext": {
                            "patientReference": patient_obj["abha_address"],
                            "careContextReference": pmr_id,
                        },
                        "date": date_of_consultation,
                        "hip": {"id": hip_id},
                    },
                }
            else:
                logging.info("Adding PMR to gateway")
                care_context_url = f"{self.gateway_url}/v0.5/links/link/add-contexts"
                payload = {
                    "requestId": request_id,
                    "timestamp": datetime.now(timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%S.%f"
                    ),
                    "link": {
                        "accessToken": access_token,
                        "patient": {
                            "referenceNumber": patient_id,
                            "display": patient_obj.get("name"),
                            "careContexts": [
                                {
                                    "referenceNumber": pmr_id,
                                    "display": f"Consultation Record for {date_of_consultation}",
                                }
                            ],
                        },
                    },
                }
            if datetime.now() > access_token_validity:
                return {
                    "pmr_id": pmr_id,
                    "request_id": request_id,
                    "status": "expired_token",
                }
            else:
                resp, resp_code = APIInterface().post(
                    route=care_context_url,
                    data=payload,
                    headers={
                        "X-CM-ID": os.environ["X-CM-ID"],
                        "Authorization": f"Bearer {gateway_access_token}",
                    },
                )

                self.CRUDGatewayInteraction.create(
                    **{
                        "request_id": request_id,
                        "request_type": "ADD_UPDATE_CARE_CONTEXT",
                        "request_status": "PROCESSING",
                        "transaction_id": request_id,
                        "gateway_metadata": {
                            "pmr_id": pmr_id,
                            "patient_id": patient_id,
                        },
                    }
                )
                # if not pmr_obj["abdm_linked"]:
                #     logging.info("Updating abdm linked flag on PMR")
                #     self.CRUDPatientMedicalRecord.update(
                #         pmr_id=pmr_id, **{"abdm_linked": True}
                #     )
                logging.info("Sending SMS notification")
                sms_notify_url = f"{self.gateway_url}/v0.5/patients/sms/notify"
                mobile_number = patient_obj.get("mobile_number")
                deep_link_request_id = str(uuid.uuid1())
                payload = {
                    "requestId": deep_link_request_id,
                    "timestamp": datetime.now(timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%S.%f"
                    ),
                    "notification": {
                        "phoneNo": mobile_number,
                        "careContextInfo": f"Consultation Record for {date_of_consultation}",
                        "hip": {"id": hip_id},
                    },
                }
                resp, resp_code = APIInterface().post(
                    route=sms_notify_url,
                    data=payload,
                    headers={
                        "X-CM-ID": os.environ["X-CM-ID"],
                        "Authorization": f"Bearer {gateway_access_token}",
                    },
                )
                self.CRUDGatewayInteraction.create(
                    **{
                        "request_id": deep_link_request_id,
                        "request_type": "DEEP_LINK_NOTIFICATION",
                        "request_status": "PROCESSING",
                        "transaction_id": request_id,
                        "gateway_metadata": {
                            "phoneNo": mobile_number,
                            "careContextInfo": f"Consultation Record for {date_of_consultation}",
                            "hip": {"id": hip_id},
                        },
                    }
                )
                logging.info(f"response code from /patients/sms/notify : {resp_code}")
                return {"pmr_id": pmr_id, "request_id": request_id, "status": "success"}
        except Exception as error:
            logging.error(f"Error in PMRController.sync_pmr function: {error}")
            raise error

    def deep_link_ack(self, request: dict):
        try:
            logging.info("executing  deep_link_ack function")
            logging.info("Getting request id")
            request_id = request.get("resp").get("requestId")
            logging.info("Getting error message")
            error_message = request.get("error")
            logging.info(f"{error_message=}")
            if error_message:
                gateway_request = {
                    "request_id": request_id,
                    "callback_response": request,
                    "request_status": "FAILED",
                    "error_code": error_message.get("code", 000),
                    "error_message": error_message.get("message", None),
                }
            else:
                gateway_request = {
                    "request_id": request_id,
                    "callback_response": request,
                    "request_status": "SUCESS",
                }
            self.CRUDGatewayInteraction.update(**gateway_request)
            return {"status": "trigger success"}
        except Exception as error:
            logging.error(f"Error in PMRController.deep_link_ack function: {error}")
            raise error

    def delete_pmr(self, pmr_id):
        try:
            logging.info("executing delete_pmr function")
            logging.info(f"Getting the PMR record for {pmr_id=}")
            self.CRUDExaminationFindings.delete()
            pmr_metadata = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
            examination_findings_data = self.CRUDExaminationFindings.read_by_pmrId(
                pmr_id=pmr_id
            )
            diagnosis_data = self.CRUDExaminationFindings.read_by_pmrId(pmr_id=pmr_id)
            medicine_data = self.CRUDMedicines.read_by_pmrId(pmr_id=pmr_id)
            medicalTest_data = self.CRUDMedicalTest.read_by_pmrId(pmr_id=pmr_id)
            pmr_metadata.update(
                {
                    "examination_findings": examination_findings_data,
                    "diagnosis": diagnosis_data,
                    "medicines": medicine_data,
                    "medicalTests": medicalTest_data,
                }
            )
            return pmr_metadata
        except Exception as error:
            logging.error(
                f"Error in PMRController.get_pmr_controller function: {error}"
            )
            raise error

    def delete_condition(self, condition_id):
        try:
            logging.info("executing delete_condition function")
            logging.info(f"Getting the PMR record for {condition_id=}")
            delete_obj = self.CRUDCondition.delete(condition_id=condition_id)
            return f"Deleted Conditiion {delete_obj}"
        except Exception as error:
            logging.error(f"Error in PMRController.delete_condition function: {error}")
            raise error

    def update_consultation_status(self, request):
        """[Controller to update pmr record]

        Args:
            request ([dict]): [update pmr request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing update consultation status function")
            request_dict = request.dict()
            appointment_id = request_dict.pop("appointment_id")
            request_dict.update({"id": appointment_id})
            logging.info(f"Consultation Status: {request_dict=}")
            self.CRUDAppointments.update(**request_dict)
            return {"appointment_id": appointment_id}
        except Exception as error:
            logging.error(
                f"Error in PMRController.update_consultation_status function: {error}"
            )
            raise error

    def update_followup(self, request):
        """[Controller to update pmr record]

        Args:
            request ([dict]): [update pmr request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing update followup date function")
            request_dict = request.dict()
            appointment_id = request_dict.pop("appointment_id")
            request_dict.update({"id": appointment_id})
            logging.info(f"Follow Up date : {request_dict=}")
            self.CRUDAppointments.update(**request_dict)
            return {"appointment_id": appointment_id}
        except Exception as error:
            logging.error(f"Error in PMRController.update_followup function: {error}")
            raise error

    def submit_pmr(self, pmr_request, appointment_request):
        """[Controller to create new pmr record]

        Args:
            request ([dict]): [create new pmr request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            pmr_updated, appointment_updated = False, False
            logging.info("executing submit pmr function")
            if pmr_request:
                pmr_data = {}
                pmr_request_dict = pmr_request.dict()
                pmr_id = pmr_request.pmr_id
                logging.info("Submitting PMR record")
                logging.info(f"{pmr_request=}")
                resp = dict()
                if pmr_request.vital:
                    pmr_data["vital"] = self.create_vital_pmr(pmr_request.vital, pmr_id)
                if pmr_request.examination_findings:
                    pmr_data["examination_findings"][
                        "data"
                    ] = self.create_examination_findings(
                        pmr_request.examination_findings, pmr_id
                    )
                if pmr_request.diagnosis:
                    resp["diagnosis_ids"] = self.create_diagnosis(
                        pmr_request.diagnosis, pmr_id
                    )
                if pmr_request.symptom:
                    resp["symptom_ids"] = self.create_symptoms(
                        pmr_request.symptom, pmr_id
                    )
                if pmr_request.medication:
                    resp["medication_ids"] = self.create_medication(
                        pmr_request.medication, pmr_id
                    )
                # TODO: To be used in future
                # if request.currentMedication:
                #     resp["current_medication_id"] = self.create_current_medication(
                #         request.currentMedication, pmr_id
                #     )
                if pmr_request.lab_investigation:
                    resp["lab_investigation_ids"] = self.create_labInvestigation(
                        pmr_request.lab_investigation, pmr_id
                    )
                if pmr_request.medical_history:
                    resp["medical_history_ids"] = self.create_medicalHistory(
                        pmr_request.medical_history, pmr_id
                    )
                self.CRUDPatientMedicalRecord.update(
                    **{
                        "id": pmr_id,
                        "advices": pmr_request.advice,
                        "notes": pmr_request.notes,
                    }
                )
                logging.info(f"PMR record submitted with PMR_ID = {pmr_id}")
                logging.info(f"{resp=}")
                pmr_updated = True
            if appointment_request:
                appointment_request_dict = appointment_request.dict()
                appointment_id = appointment_request_dict.pop("appointment_id")
                appointment_request_dict.update({"id": appointment_id})
                self.CRUDAppointments.update(**appointment_request_dict)
                appointment_updated = True
            return {
                "pmr_details": pmr_request.dict(),
                "appointment_details": appointment_request.dict(),
                "pmr_updated": pmr_updated,
                "appointment_updated": appointment_updated,
            }
        except Exception as error:
            logging.error(
                f"Error in PMRController.submit_pmr_controller function: {error}"
            )
            raise error

    def submit_pmr_v1(self, pmr_request, appointment_request):
        """[Controller to create new pmr record v1]

        Args:
            request ([dict]): [create new pmr request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            pmr_updated, appointment_updated = False, False
            pmr_request_dict = pmr_request.dict()
            appointment_request_dict = appointment_request.dict()
            logging.info("executing submit pmr function")
            if pmr_request:
                pmr_data = {}
                del pmr_request_dict["vital"]
                del pmr_request_dict["examination_findings"]
                del pmr_request_dict["diagnosis"]
                del pmr_request_dict["symptom"]
                del pmr_request_dict["medication"]
                del pmr_request_dict["lab_investigation"]
                del pmr_request_dict["medical_history"]
                pmr_id = pmr_request.pmr_id
                logging.info("Submitting PMR record")
                logging.info(f"{pmr_request=}")
                resp = dict()
                if pmr_request.vital:
                    pmr_data["vital"] = self.create_vital_pmr(pmr_request.vital, pmr_id)
                if pmr_request.examination_findings:
                    logging.info(f"{pmr_data=}")
                    pmr_data.setdefault("examination_findings", {})
                    logging.info(f"{pmr_data=}")
                    pmr_data["examination_findings"][
                        "data"
                    ] = self.create_examination_findings_v1(
                        pmr_request.examination_findings, pmr_id
                    )
                    logging.info(f"{pmr_data=}")
                if pmr_request.diagnosis:
                    pmr_data.setdefault("diagnosis", {})
                    pmr_data["diagnosis"]["data"] = self.create_diagnosis_v1(
                        pmr_request.diagnosis, pmr_id
                    )
                if pmr_request.symptom:
                    pmr_data.setdefault("symptom", {})
                    pmr_data["symptom"]["data"] = self.create_symptoms_v1(
                        pmr_request.symptom, pmr_id
                    )
                if pmr_request.medication:
                    pmr_data.setdefault("medication", {})
                    pmr_data["medication"]["data"] = self.create_medication_v1(
                        pmr_request.medication, pmr_id
                    )
                # TODO: To be used in future
                # if request.currentMedication:
                #     resp["current_medication_id"] = self.create_current_medication(
                #         request.currentMedication, pmr_id
                #     )
                if pmr_request.lab_investigation:
                    pmr_data.setdefault("lab_investigation", {})
                    pmr_data["lab_investigation"][
                        "data"
                    ] = self.create_labInvestigation_v1(
                        pmr_request.lab_investigation, pmr_id
                    )
                if pmr_request.medical_history:
                    pmr_data.setdefault("medical_history", {})
                    pmr_data["medical_history"]["data"] = self.create_medicalHistory_v1(
                        pmr_request.medical_history, pmr_id
                    )
                self.CRUDPatientMedicalRecord.update(
                    **{
                        "id": pmr_id,
                        "advices": pmr_request.advice,
                        "notes": pmr_request.notes,
                    }
                )
                pmr_request_dict.update({"pmr_data": pmr_data})
                logging.info(f"PMR record submitted with PMR_ID = {pmr_id}")
                logging.info(f"{resp=}")
                pmr_updated = True
            if appointment_request:
                appointment_id = appointment_request_dict.pop("appointment_id")
                appointment_request_dict.update({"id": appointment_id})
                self.CRUDAppointments.update(**appointment_request_dict)
                appointment_updated = True
            return {
                "pmr_details": pmr_request_dict,
                "appointment_details": appointment_request_dict,
                "pmr_updated": pmr_updated,
                "appointment_updated": appointment_updated,
            }
        except Exception as error:
            logging.error(
                f"Error in PMRController.submit_pmr_controller function: {error}"
            )
            raise error

    async def upload_document(self, pmr_id, files, document_type):
        try:
            logging.info("executing upload_document function")
            pmr_obj = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
            patient_id = pmr_obj.get("patient_id")
            uploaded_document_list = []
            for document in files:
                logging.info(f"{document=}")
                document_name = document.filename
                document_data = await document.read()
                document_ext = document_name.split(".")[-1]
                document_key = f"PATIENT_DATA/{patient_id}/{pmr_id}/{document_name}"
                s3_location = upload_to_s3(
                    bucket_name=self.cliniq_bucket,
                    byte_data=document_data,
                    file_name=document_key,
                    content_type="application/pdf",
                )
                document_id = f"C360-DOC-{str(uuid.uuid1().int)[:18]}"
                self.CRUDPatientMedicalDocuments.create(
                    **{
                        "id": document_id,
                        "pmr_id": pmr_id,
                        "document_name": document_name,
                        "document_mime_type": self.mime_type_mapping.get(document_ext),
                        "document_type": document_type.name,
                        "document_type_code": document_type.value,
                        "document_location": s3_location,
                    }
                )
                uploaded_document_list.append(
                    {"document_id": document_id, "status": "success"}
                )
            return uploaded_document_list
        except Exception as error:
            logging.error(f"Error in PMRController.upload_document function: {error}")
            raise error

    def list_documents(self, pmr_id):
        try:
            logging.info("executing list_documents function")
            return self.CRUDPatientMedicalDocuments.read_by_pmr_id(pmr_id=pmr_id)
        except Exception as error:
            logging.error(f"Error in PMRController.list_documents function: {error}")
            raise error

    def get_document(self, document_id, expires_in=1800):
        try:
            logging.info("executing get_document function")
            document_obj = self.CRUDPatientMedicalDocuments.read(
                document_id=document_id
            )
            logging.info(f"{document_obj=}")
            document_location = document_obj.get("document_location")
            bucket_name = document_location.split("/")[0]
            document_key = "/".join(document_location.split("/")[1:])
            logging.info(f"{bucket_name=}")
            logging.info(f"{document_key=}")
            presigned_url = create_presigned_url(
                bucket_name=bucket_name, key=document_key, expires_in=expires_in
            )
            return {"document_url": presigned_url}
        except Exception as error:
            logging.error(f"Error in PMRController.get_document function: {error}")
            raise error

    def get_document_bytes(self, document_id):
        try:
            logging.info("executing get_document_bytes function")
            document_obj = self.CRUDPatientMedicalDocuments.read(
                document_id=document_id
            )
            logging.info(f"{document_obj=}")
            document_location = document_obj.get("document_location")
            bucket_name = document_location.split("/")[0]
            document_key = "/".join(document_location.split("/")[1:])
            logging.info(f"{bucket_name=}")
            logging.info(f"{document_key=}")
            document_bytes = read_object(
                bucket_name=bucket_name,
                prefix=document_key,
            )
            return {"data": document_bytes}
        except Exception as error:
            logging.error(
                f"Error in PMRController.get_document_bytes function: {error}"
            )
            raise error

    def upload_prescription(self, pmr_id, files, mode):
        try:
            logging.info("executing upload_prescription function")
            document_type = f"Prescription_{mode}"
            logging.debug(f"{mode=}")
            document_type_code = "Prescription"
            pmr_obj = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
            pmr_doc_obj = self.CRUDPatientMedicalDocuments.read_by_type(
                pmr_id=pmr_id, document_type=document_type
            )
            logging.debug(f"{pmr_doc_obj=}")
            patient_id = pmr_obj.get("patient_id")

            if mode == "digital":
                document_data = files[0]
                if pmr_doc_obj is not None:
                    document_id = pmr_doc_obj.get("id")
                    document_key = (
                        f"PATIENT_DATA/{patient_id}/{pmr_id}/{document_id}.pdf"
                    )
                    s3_location = upload_to_s3(
                        bucket_name=self.cliniq_bucket,
                        byte_data=document_data,
                        file_name=document_key,
                        content_type="application/pdf",
                    )
                    self.CRUDPatientMedicalDocuments.update(
                        document_id=document_id,
                        **{"id": document_id, "document_location": s3_location},
                    )
                    return {"document_id": document_id}
                else:
                    document_id = f"C360-DOC-{str(uuid.uuid1().int)[:18]}"
                    document_key = (
                        f"PATIENT_DATA/{patient_id}/{pmr_id}/{document_id}.pdf"
                    )
                    s3_location = upload_to_s3(
                        bucket_name=self.cliniq_bucket,
                        byte_data=document_data,
                        file_name=document_key,
                        content_type="application/pdf",
                    )
                    self.CRUDPatientMedicalDocuments.create(
                        **{
                            "id": document_id,
                            "pmr_id": pmr_id,
                            "document_name": document_type,
                            "document_mime_type": self.mime_type_mapping.get("pdf"),
                            "document_type": document_type,
                            "document_type_code": document_type_code,
                            "document_location": s3_location,
                        }
                    )
                    logging.info(f"{s3_location=}")
                    return {"document_id": document_id}
            elif mode == "handwritten":
                if pmr_doc_obj is not None:
                    document_id = pmr_doc_obj.get("id")
                    document_key = (
                        f"PATIENT_DATA/{patient_id}/{pmr_id}/{document_id}.pdf"
                    )
                    pdf1_data = self.get_document_bytes(document_id=document_id)
                    logging.info("1")
                    pdf1_bytes_str = pdf1_data["data"]
                    pdf1_bytes = base64.b64decode(pdf1_bytes_str)
                    logging.info(f"{type(pdf1_bytes)}")
                    pdf =  merge_pdf(pdf1_bytes=pdf1_bytes, files=files)
                    s3_location = upload_to_s3(
                        bucket_name=self.cliniq_bucket,
                        byte_data=pdf,
                        file_name=document_key,
                        content_type="application/pdf",
                    )
                    logging.info(f"{s3_location=}")
                    return {"document_id": document_id}
                else:
                    pdf =  create_pdf_from_images(files=files)
                    document_id = f"C360-DOC-{str(uuid.uuid1().int)[:18]}"
                    document_key = (
                        f"PATIENT_DATA/{patient_id}/{pmr_id}/{document_id}.pdf"
                    )
                    s3_location = upload_to_s3(
                        bucket_name=self.cliniq_bucket,
                        byte_data=pdf,
                        file_name=document_key,
                        content_type="application/pdf",
                    )
                    self.CRUDPatientMedicalDocuments.create(
                        **{
                            "id": document_id,
                            "pmr_id": pmr_id,
                            "document_name": document_type,
                            "document_mime_type": self.mime_type_mapping.get("pdf"),
                            "document_type": document_type,
                            "document_type_code": document_type_code,
                            "document_location": s3_location,
                        }
                    )
                    logging.info(f"{s3_location=}")
                    return {"document_id": document_id}
        except Exception as error:
            logging.error(
                f"Error in PMRController.upload_prescription function: {error}"
            )
            raise error

    def upload_health_document(
        self,
        pmr_id,
        patient_id,
        document_data,
        document_type,
        document_name,
    ):
        try:
            logging.info("executing upload_health_document function")
            logging.info(f"{pmr_id=}")
            document_ext = document_name.split(".")[-1]
            document_key = f"PATIENT_DATA/{patient_id}/{pmr_id}/{document_name}"
            s3_location = upload_to_s3(
                bucket_name=self.cliniq_bucket,
                byte_data=document_data,
                file_name=document_key,
                content_type=self.mime_type_mapping.get(document_ext),
            )
            document_id = f"C360-DOC-{str(uuid.uuid1().int)[:18]}"
            self.CRUDPatientMedicalDocuments.create(
                **{
                    "id": document_id,
                    "pmr_id": pmr_id,
                    "document_name": document_name,
                    "document_mime_type": self.mime_type_mapping.get(document_ext),
                    "document_type": document_type,
                    "document_location": s3_location,
                }
            )
            return {"document_id": document_id, "status": "success"}
        except Exception as error:
            logging.error(
                f"Error in PMRController.upload_health_document function: {error}"
            )
            raise error

    def get_fhir(self, pmr_id):
        try:
            logging.info("executing get_fhir function")
            logging.info(f"{pmr_id=}")
            bundle_id = str(uuid.uuid1())
            return opConsultUnstructured(
                bundle_name=f"OPConsultNote-{bundle_id}",
                bundle_identifier=bundle_id,
                pmr_id=pmr_id,
            )
        except Exception as error:
            logging.error(f"Error in PMRController.get_fhir function: {error}")
            raise error

    def send_notification(self, request):
        try:
            logging.info("executing  PMRController.send_notification function")
            request = request.dict()
            logging.info(f"{request=}")
            channel = request.get("channel").value
            logging.info(f"{channel=}")
            alternate_mobile_number = request.get("mobile_number", None)
            pmr_id = request.get("pmr_id")
            pmr_obj = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
            logging.info(f"{pmr_obj=}")
            document_id = pmr_obj.get("doc_id")
            hip_id = pmr_obj.get("hip_id")
            date_of_consultation = pmr_obj.get("date_of_consultation")
            patient_id = pmr_obj.get("patient_id")
            patient_obj = self.CRUDPatientDetails.read_by_patientId(
                patient_id=patient_id
            )
            logging.info(f"{patient_obj=}")
            patient_name = patient_obj.get("name")
            hip_obj = self.CRUDHIP.read(hip_ip=hip_id)
            logging.info(f"{hip_obj=}")
            document_obj_list = self.CRUDPatientMedicalDocuments.read_by_pmr_id(
                pmr_id=pmr_id
            )
            if alternate_mobile_number:
                mobile_number = alternate_mobile_number
            else:
                mobile_number = patient_obj.get("mobile_number")
            logging.info(f"{document_obj_list=}")
            for document_obj in document_obj_list:
                document_details_obj = self.get_document(
                    document_id=document_obj.get("id"), expires_in=604800
                )
                document_url = document_details_obj.get("document_url")
                if channel == "whatsapp":
                    opt_in_response, opt_in_status_code = whatsappHelper().optin_user(
                        mobile_number=mobile_number
                    )
                    logging.info(f"{opt_in_response=} | {opt_in_status_code=}")
                    (
                        send_msg_response,
                        send_msg_status_code,
                    ) = whatsappHelper().send_prescription(
                        mobile_number=mobile_number,
                        document_url=document_url,
                        patient_name=patient_name,
                        hospital_name=hip_obj.get("name"),
                        date_of_consultation=date_of_consultation,
                    )
                    logging.info(f"{send_msg_response=} | {send_msg_status_code=}")
                elif channel == "sms":
                    encoded_url = quote(document_url)
                    double_encoded_url = quote(encoded_url)
                    sms_response, sms_response_code = smsHelper().send_prescription(
                        mobile_number=mobile_number,
                        hospital_name=hip_obj.get("name"),
                        document_url=double_encoded_url,
                    )
                    logging.info(f"{sms_response=} | {sms_response_code=}")
        except Exception as error:
            logging.error(f"Error in PMRController.send_notification function: {error}")
            raise error

    def send_notification_by_documentId(self, request):
        try:
            logging.info(
                "executing  PMRController.send_notification_by_documentId function"
            )
            request = request.dict()
            logging.info(f"{request=}")
            channel = request.get("channel").value
            logging.info(f"{channel=}")
            alternate_mobile_number = request.get("mobile_number", None)
            pmr_id = request.get("pmr_id")
            pmr_obj = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
            logging.info(f"{pmr_obj=}")
            hip_id = pmr_obj.get("hip_id")
            date_of_consultation = pmr_obj.get("date_of_consultation")
            patient_id = pmr_obj.get("patient_id")
            patient_obj = self.CRUDPatientDetails.read_by_patientId(
                patient_id=patient_id
            )
            logging.info(f"{patient_obj=}")
            patient_name = patient_obj.get("name")
            hip_obj = self.CRUDHIP.read(hip_ip=hip_id)
            logging.info(f"{hip_obj=}")
            document_id = request.get("document_id", None)
            document_obj = self.CRUDPatientMedicalDocuments.read(
                document_id=document_id
            )
            if alternate_mobile_number:
                mobile_number = alternate_mobile_number
            document_details_obj = self.get_document(
                document_id=document_obj.get("id"), expires_in=604800
            )
            document_url = document_details_obj.get("document_url")
            if channel == "whatsapp":
                opt_in_response, opt_in_status_code = whatsappHelper().optin_user(
                    mobile_number=mobile_number
                )
                logging.info(f"{opt_in_response=} | {opt_in_status_code=}")
                (
                    send_msg_response,
                    send_msg_status_code,
                ) = whatsappHelper().send_prescription(
                    mobile_number=mobile_number,
                    document_url=document_url,
                    patient_name=patient_name,
                    hospital_name=hip_obj.get("name"),
                    date_of_consultation=date_of_consultation,
                )
                logging.info(f"{send_msg_response=} | {send_msg_status_code=}")
            elif channel == "sms":
                encoded_url = quote(document_url)
                double_encoded_url = quote(encoded_url)
                sms_response, sms_response_code = smsHelper().send_prescription(
                    mobile_number=mobile_number,
                    hospital_name=hip_obj.get("name"),
                    document_url=double_encoded_url,
                )
                logging.info(f"{sms_response=} | {sms_response_code=}")
        except Exception as error:
            logging.error(
                f"Error in PMRController.send_notification_by_documentId function: {error}"
            )
            raise error
