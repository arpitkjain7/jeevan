from core.crud.hims_vitals_crud import CRUDVital
from core.crud.hims_compaint_crud import CRUDComplaint
from core.crud.hims_diagnosis_crud import CRUDDiagnosis
from core.crud.hims_appointments_crud import CRUDAppointments
from core.crud.hims_medicalTest_crud import CRUDMedicalTest
from core.crud.hims_medicines_crud import CRUDMedicines
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from core.crud.hims_medicalHistory_crud import CRUDMedicalHistory
from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.utils.custom.external_call import APIInterface
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.utils.custom.session_helper import get_session_token
from core import logger
from datetime import datetime, timezone
import uuid, os
from pytz import timezone as pytz_timezone

logging = logger(__name__)


class PMRController:
    def __init__(self):
        self.gateway_url = os.environ["gateway_url"]
        self.CRUDComplaint = CRUDComplaint()
        self.CRUDDiagnosis = CRUDDiagnosis()
        self.CRUDAppointments = CRUDAppointments()
        self.CRUDMedicalTest = CRUDMedicalTest()
        self.CRUDMedicines = CRUDMedicines()
        self.CRUDPatientMedicalRecord = CRUDPatientMedicalRecord()
        self.CRUDPatientDetails = CRUDPatientDetails()
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDMedicalHistory = CRUDMedicalHistory()
        self.CRUDVital = CRUDVital()

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
            pmr_id = f"C360_PMR_{str(uuid.uuid1().int)[:18]}"
            request_dict.update({"id": pmr_id, "hip_id": request_dict["hip_id"]})
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
            for vital_obj in request.data:
                vital_obj_dict = vital_obj.dict()
                vital_obj_dict.update({"pmr_id": request.pmr_id})
                vital_id = self.CRUDVital.create(**vital_obj_dict)
            return {"pmr_id": request.pmr_id, "vital_id": vital_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_vital function: {error}")
            raise error

    def update_vital(self, request):
        try:
            logging.info("Updating vital records")
            for vital_obj in request.data:
                vital_obj_dict = vital_obj.dict()
                self.CRUDVital.update(**vital_obj_dict, id=request.id)
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_complaints function: {error}")
            raise error

    def create_complaints(self, request):
        try:
            logging.info("Creating complaint records")
            for complaint_obj in request.data:
                complaint_obj_dict = complaint_obj.dict()
                complaint_obj_dict.update({"pmr_id": request.pmr_id})
                complaint_id = self.CRUDComplaint.create(**complaint_obj_dict)
            return {"pmr_id": request.pmr_id, "complaint_id": complaint_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_complaints function: {error}")
            raise error

    def update_complaints(self, request):
        try:
            logging.info("Updating complaint records")
            for complaint_obj in request.data:
                complaint_obj_dict = complaint_obj.dict()
                self.CRUDComplaint.update(**complaint_obj_dict, id=request.id)
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_complaints function: {error}")
            raise error

    def create_diagnosis(self, request):
        try:
            logging.info("Creating diagnosis records")
            for diagnosis_obj in request.data:
                diagnosis_obj_dict = diagnosis_obj.dict()
                diagnosis_obj_dict.update({"pmr_id": request.pmr_id})
                diagnosis_id = self.CRUDDiagnosis.create(**diagnosis_obj_dict)
            logging.info("Creating complaint records")
            return {"pmr_id": request.pmr_id, "diagnosis_id": diagnosis_id}
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

    def create_medication(self, request):
        try:
            logging.info("Creating medicines records")
            for medicines_obj in request.data:
                medicines_obj_dict = medicines_obj.dict()
                medicines_obj_dict.update({"pmr_id": request.pmr_id})
                medicines_id = self.CRUDMedicines.create(**medicines_obj_dict)
            return {"pmr_id": request.pmr_id, "medicines_id": medicines_id}
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

    def create_medicalTest(self, request):
        try:
            logging.info("Creating medical tests records")
            for medical_tests_obj in request.data:
                medical_tests_obj_dict = medical_tests_obj.dict()
                medical_tests_obj_dict.update({"pmr_id": request.pmr_id})
                medicalTest_id = self.CRUDMedicalTest.create(**medical_tests_obj_dict)
            return {"pmr_id": request.pmr_id, "medicalTest_id": medicalTest_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_diagnosis function: {error}")
            raise error

    def update_medicalTest(self, request):
        try:
            logging.info("Updating medical test records")
            for medical_test_obj in request.data:
                medical_test_obj_dict = medical_test_obj.dict()
                self.CRUDMedicalTest.update(**medical_test_obj_dict, id=request.id)
            return {"pmr_id": request.pmr_id}
        except Exception as error:
            logging.error(f"Error in PMRController.create_complaints function: {error}")
            raise error

    def create_medicalHistory(self, request):
        try:
            logging.info("Creating medical history records")
            logging.info(f"{request=}")
            for medical_history_obj in request.data:
                medical_history_obj_dict = medical_history_obj.dict()
                medical_history_obj_dict.update({"pmr_id": request.pmr_id})
                logging.info(f"{medical_history_obj_dict=}")
                medicalHistory_id = self.CRUDMedicalHistory.create(
                    **medical_history_obj_dict
                )
            return {"pmr_id": request.pmr_id, "medicalHistory_id": medicalHistory_id}
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
            complaint_data = self.CRUDComplaint.read_by_pmrId(pmr_id=pmr_id)
            diagnosis_data = self.CRUDDiagnosis.read_by_pmrId(pmr_id=pmr_id)
            medicine_data = self.CRUDMedicines.read_by_pmrId(pmr_id=pmr_id)
            medicalTest_data = self.CRUDMedicalTest.read_by_pmrId(pmr_id=pmr_id)
            medicalHistory_data = self.CRUDMedicalHistory.read_by_pmrId(pmr_id=pmr_id)

            pmr_metadata.update(
                {
                    "vitals": vitals_data,
                    "complaints": complaint_data,
                    "diagnosis": diagnosis_data,
                    "medicines": medicine_data,
                    "medicalTests": medicalTest_data,
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
            patient_id = pmr_obj.get("patient_id")
            patient_obj = self.CRUDPatientDetails.read_by_patientId(
                patient_id=patient_id
            )
            date_of_consultation = pmr_obj["date_of_consultation"].strftime(
                "%Y-%m-%dT%H:%M:%S.%f"
            )
            request_id = str(uuid.uuid1())
            if pmr_obj["abdm_linked"]:
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
                care_context_url = f"{self.gateway_url}/v0.5/links/link/add-contexts"
                payload = {
                    "requestId": request_id,
                    "timestamp": datetime.now(timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%S.%f"
                    ),
                    "link": {
                        "accessToken": patient_obj.get("access_token"),
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
            resp, resp_code = APIInterface().post(
                route=care_context_url,
                data=payload,
                headers={
                    "X-CM-ID": "sbx",
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
            logging.info("Sending SMS notification")
            sms_notify_url = f"{self.gateway_url}/v0.5/patients/sms/notify"
            mobile_number = patient_obj.get("mobile_number")
            request_id = str(uuid.uuid1())
            payload = {
                "requestId": request_id,
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
                    "X-CM-ID": "sbx",
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.info(f"response code from /patients/sms/notify : {resp_code}")
            return {"pmr_id": pmr_id}
        except Exception as error:
            logging.error(f"Error in PMRController.sync_pmr function: {error}")
            raise error

    def delete_pmr(self, pmr_id):
        try:
            logging.info("executing delete_pmr function")
            logging.info(f"Getting the PMR record for {pmr_id=}")
            self.CRUDComplaint.delete()
            pmr_metadata = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
            complaint_data = self.CRUDComplaint.read_by_pmrId(pmr_id=pmr_id)
            diagnosis_data = self.CRUDComplaint.read_by_pmrId(pmr_id=pmr_id)
            medicine_data = self.CRUDMedicines.read_by_pmrId(pmr_id=pmr_id)
            medicalTest_data = self.CRUDMedicalTest.read_by_pmrId(pmr_id=pmr_id)
            pmr_metadata.update(
                {
                    "complaints": complaint_data,
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
