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
from core.utils.fhir.op_consult import opConsultUnstructured
from core.utils.aws.s3_helper import upload_to_s3, create_presigned_url, read_object
from core.utils.custom.session_helper import get_session_token
from core import logger
from datetime import datetime, timezone
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
        self.mime_type_mapping = {
            "pdf": "application/pdf",
            "jpeg": "image/jpg",
            "jpg": "image/jpg",
            "png": "image/png",
        }
        self.abha_url = os.environ["abha_url"]

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
            if type(request) is dict:
                request_dict = request
            else:
                request_dict = request.dict()
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
                    "hip_id": request_dict["hip_id"],
                    "date_of_consultation": consultation_date,
                }
            )
            logging.info("Creating PMR record")
            logging.info(f"PMR: {request_dict=}")
            pmr_id = self.CRUDPatientMedicalRecord.create(**request_dict)
            logging.info(f"PMR record created with PMR_ID = {pmr_id}")
            return {"pmr_id": pmr_id}
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_pmr_controller function: {error}"
            )
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
            vital_obj_dict.update({"pmr_id": pmr_id})
            vital_id = self.CRUDVital.create(**vital_obj_dict)
            return {"pmr_id": pmr_id, "vital_id": vital_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_vital function: {error}")
            raise error

    def update_vital(self, request):
        try:
            logging.info("Updating vital records")
            vital_obj_dict = request.data.dict()
            self.CRUDVital.update(**vital_obj_dict, id=request.id)
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_examination_findings function: {error}"
            )
            raise error

    def create_examination_findings(self, request, pmr_id):
        try:
            logging.info("Creating examination findings records")
            for examination_findings_obj in request.data:
                examination_findings_obj_dict = examination_findings_obj.dict()
                logging.info(f"{examination_findings_obj_dict=}")
                examination_findings_obj_dict.update({"pmr_id": pmr_id})
                examination_findings_id = self.CRUDExaminationFindings.create(
                    **examination_findings_obj_dict
                )
            return {
                "pmr_id": pmr_id,
                "examination_findings_id": examination_findings_id,
            }
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_examination_findings function: {error}"
            )
            raise error

    def update_examination_findings(self, request):
        try:
            logging.info("Updating examination findings records")
            for examination_findings_obj in request.data:
                examination_findings_obj_dict = examination_findings_obj.dict()
                self.CRUDExaminationFindings.update(
                    **examination_findings_obj_dict, id=request.id
                )
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_examination_findings function: {error}"
            )
            raise error

    def create_condition(self, request, pmr_id):
        try:
            logging.info("Creating condition records")
            for condition_obj in request.data:
                condition_obj_dict = condition_obj.dict()
                condition_obj_dict.update({"pmr_id": pmr_id})
                logging.info(f"{condition_obj_dict=}")
                condition_id = self.CRUDCondition.create(**condition_obj_dict)
            logging.info("Creating condition records")
            return {"pmr_id": pmr_id, "condition_id": condition_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_condition function: {error}")
            raise error

    def update_condition(self, request):
        try:
            logging.info("Updating condition records")
            for condition_obj in request.data:
                condition_obj_dict = condition_obj.dict()
                self.CRUDCondition.update(**condition_obj_dict, id=request.id)
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_conditions function: {error}")
            raise error

    def create_diagnosis(self, request, pmr_id):
        try:
            logging.info("Creating diagnosis records")
            for diagnosis_obj in request.data:
                diagnosis_obj_dict = diagnosis_obj.dict()
                diagnosis_obj_dict.update({"pmr_id": pmr_id})
                logging.info(f"{diagnosis_obj_dict=}")
                diagnosis_id = self.CRUDDiagnosis.create(**diagnosis_obj_dict)
            logging.info("Creating complaint records")
            return {"pmr_id": pmr_id, "diagnosis_id": diagnosis_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_diagnosis function: {error}")
            raise error

    def update_diagnosis(self, request):
        try:
            logging.info("Updating complaint records")
            for diagnosis_obj in request.data:
                diagnosis_obj_dict = diagnosis_obj.dict()
                self.CRUDDiagnosis.update(**diagnosis_obj_dict, id=request.id)
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_complaints function: {error}")
            raise error

    def create_symptoms(self, request, pmr_id):
        try:
            logging.info("Creating symptoms records")
            for symptoms_obj in request.data:
                symptoms_obj_dict = symptoms_obj.dict()
                symptoms_obj_dict.update({"pmr_id": pmr_id})
                symptom_id = self.CRUDSymptoms.create(**symptoms_obj_dict)
            logging.info("Creating symptoms records")
            return {"pmr_id": pmr_id, "symptom_id": symptom_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_symptoms function: {error}")
            raise error

    def update_symptoms(self, request):
        try:
            logging.info("Updating symptoms records")
            for symptoms_obj in request.data:
                symptoms_obj_dict = symptoms_obj.dict()
                self.CRUDSymptoms.update(**symptoms_obj_dict, id=request.id)
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(f"Error in PMRController.update_symptoms function: {error}")
            raise error

    def create_medication(self, request, pmr_id):
        try:
            logging.info("Creating medicines records")
            for medicines_obj in request.data:
                medicines_obj_dict = medicines_obj.dict()
                medicines_obj_dict.update({"pmr_id": pmr_id})
                medicines_id = self.CRUDMedicines.create(**medicines_obj_dict)
            return {"pmr_id": pmr_id, "medicines_id": medicines_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_medication function: {error}")
            raise error

    def update_medication(self, request):
        try:
            logging.info("Updating medicine records")
            for medication_obj in request.data:
                medication_obj_dict = medication_obj.dict()
                self.CRUDMedicines.update(**medication_obj_dict, id=request.id)
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_complaints function: {error}")
            raise error

    def create_current_medication(self, request, pmr_id):
        try:
            logging.info("Creating curremt medicines records")
            for current_medicines_obj in request.data:
                current_medicines_obj_dict = current_medicines_obj.dict()
                current_medicines_obj_dict.update({"pmr_id": pmr_id})
                current_medicines_id = self.CRUDCurrentMedicines.create(
                    **current_medicines_obj_dict
                )
            return {
                "pmr_id": pmr_id,
                "current_medicines_id": current_medicines_id,
            }
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
            for lab_investigation_obj in request.data:
                lab_investigation_obj_dict = lab_investigation_obj.dict()
                lab_investigation_obj_dict.update({"pmr_id": pmr_id})
                lab_investigation_id = self.CRUDLabInvestigation.create(
                    **lab_investigation_obj_dict
                )
            return {
                "pmr_id": pmr_id,
                "labInvestigation_id": lab_investigation_id,
            }
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_labInvestigation function: {error}"
            )
            raise error

    def update_medicalTest(self, request):
        try:
            logging.info("Updating medical test records")
            for medical_test_obj in request.data:
                medical_test_obj_dict = medical_test_obj.dict()
                self.CRUDLabInvestigation.update(**medical_test_obj_dict, id=request.id)
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_labInvestigation function: {error}"
            )
            raise error

    def create_medicalHistory(self, request, pmr_id):
        try:
            logging.info("Creating medical history records")
            logging.info(f"{request=}")
            for medical_history_obj in request.data:
                medical_history_obj_dict = medical_history_obj.dict()
                medical_history_obj_dict.update({"pmr_id": pmr_id})
                logging.info(f"{medical_history_obj_dict=}")
                medicalHistory_id = self.CRUDMedicalHistory.create(
                    **medical_history_obj_dict
                )
            return {"pmr_id": pmr_id, "medicalHistory_id": medicalHistory_id}
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_medical_history function: {error}"
            )
            raise error

    def update_medicalHistory(self, request):
        try:
            logging.info("Updating medical history records")
            for medical_history_obj in request.data:
                medical_history_obj_dict = medical_history_obj.dict()
                self.CRUDMedicalHistory.update(
                    **medical_history_obj_dict, id=request.id
                )
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_complaints function: {error}")
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
            return self.CRUDPatientMedicalRecord.read_by_patientId(
                patient_id=patient_id
            )
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
            medicalTestReport_data = self.CRUDMedicalTestReports.read_by_pmrId(
                pmr_id=pmr_id
            )
            medicalHistory_data = self.CRUDMedicalHistory.read_by_pmrId(pmr_id=pmr_id)
            condition = self.CRUDCondition.read_by_pmrId(pmr_id=pmr_id)
            symptoms = self.CRUDSymptoms.read_by_pmrId(pmr_id=pmr_id)
            current_medication = self.CRUDCurrentMedicines.read_by_pmrId(pmr_id=pmr_id)
            pmr_metadata.update(
                {
                    "vitals": vitals_data,
                    "examination_findings": examination_findings_data,
                    "conditions": condition,
                    "diagnosis": diagnosis_data,
                    "symptoms": symptoms,
                    "medicines": medicine_data,
                    "current_medication": current_medication,
                    "medicalTestReport": medicalTestReport_data,
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
            logging.info(
                f"Consultation Status: {request_dict=}, PMR: {appointment_id=}"
            )
            self.CRUDAppointments.update(appointment_id, **request_dict)
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
            logging.info(f"Follow Up date : {request_dict=}, PMR: {appointment_id=}")
            self.CRUDAppointments.update(appointment_id, **request_dict)
            return {"appointment_id": appointment_id}
        except Exception as error:
            logging.error(f"Error in PMRController.update_followup function: {error}")
            raise error

    def submit_pmr(self, request):
        """[Controller to create new pmr record]

        Args:
            request ([dict]): [create new pmr request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing submit pmr function")
            pmr_id = request.pmr_id
            logging.info("Submitting PMR record")
            logging.info(f"{request=}")
            resp = dict()
            if request.vital is not None:
                resp["vital_id"] = self.create_vital_pmr(request.vital, pmr_id)[
                    "vital_id"
                ]
            # if request.condition is not None:
            #     # logging.info(type(request.condition))
            #     resp["condition_id"] = self.create_condition(request.condition, pmr_id)[
            #         "condition_id"
            #     ]
            if request.examinationFindings is not None:
                resp["examination_findings_id"] = self.create_examination_findings(
                    request.examinationFindings, pmr_id
                )["examination_findings_id"]
            if request.diagnosis is not None:
                resp["diagnosis_id"] = self.create_diagnosis(request.diagnosis, pmr_id)[
                    "diagnosis_id"
                ]
            if request.symptom is not None:
                resp["symptom_id"] = self.create_symptoms(request.symptom, pmr_id)[
                    "symptom_id"
                ]
            if request.medication is not None:
                resp["medication_id"] = self.create_medication(
                    request.medication, pmr_id
                )["medicines_id"]
            if request.currentMedication is not None:
                resp["current_medication_id"] = self.create_current_medication(
                    request.currentMedication, pmr_id
                )["current_medicines_id"]
            if request.lab_investigation is not None:
                resp["lab_investigation_id"] = self.create_labInvestigation(
                    request.lab_investigation, pmr_id
                )["labInvestigation_id"]
            if request.medical_history is not None:
                resp["medical_history_id"] = self.create_medicalHistory(
                    request.medical_history, pmr_id
                )["medicalHistory_id"]
            # if request.advice is not None:
            #     resp["advice_id"] = self.create_advice(request.advice, pmr_id)
            # if request.notes is not None:
            #     resp["notes_id"] = self.create_notes(request.notes, pmr_id)
            self.CRUDPatientMedicalRecord.update(
                **{
                    "id": pmr_id,
                    "follow_up": request.follow_up,
                    "advices": request.advice,
                    "notes": request.notes,
                }
            )
            logging.info(f"PMR record submitted with PMR_ID = {pmr_id}")
            logging.info(f"{resp=}")
            return {
                "pmr_id": pmr_id,
                "response": resp,
            }
        except Exception as error:
            logging.error(
                f"Error in PMRController.submit_pmr_controller function: {error}"
            )
            raise error

    def upload_document(self, pmr_id, document_data, document_type, document_name):
        try:
            logging.info("executing upload_document function")
            pmr_obj = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
            patient_id = pmr_obj.get("patient_id")
            document_ext = document_name.split(".")[-1]
            document_key = f"PATIENT_DATA/{patient_id}/{pmr_id}/{document_name}"
            s3_location = upload_to_s3(
                bucket_name=self.cliniq_bucket,
                byte_data=document_data,
                file_name=document_key,
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
            return {"document_id": document_id, "status": "success"}
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

    def get_document(self, document_id):
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
                bucket_name=bucket_name, key=document_key, expires_in=1800
            )
            return {"document_url": presigned_url}
        except Exception as error:
            logging.error(f"Error in PMRController.get_document function: {error}")
            raise error

    def get_document_bytes(self, document_id):
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
            document_bytes = read_object(
                bucket_name=bucket_name,
                prefix=document_key,
            )
            return {"data": document_bytes}
        except Exception as error:
            logging.error(f"Error in PMRController.get_document function: {error}")
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
