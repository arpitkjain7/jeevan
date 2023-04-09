from core.crud.hims_compaint_crud import CRUDComplaint
from core.crud.hims_diagnosis_crud import CRUDDiagnosis
from core.crud.hims_appointments_crud import CRUDAppointments
from core.crud.hims_medicalTest_crud import CRUDMedicalTest
from core.crud.hims_medicines_crud import CRUDMedicines
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from core import logger

logging = logger(__name__)


class PMRController:
    def __init__(self):
        self.CRUDComplaint = CRUDComplaint()
        self.CRUDDiagnosis = CRUDDiagnosis()
        self.CRUDAppointments = CRUDAppointments()
        self.CRUDMedicalTest = CRUDMedicalTest()
        self.CRUDMedicines = CRUDMedicines()
        self.CRUDPatientMedicalRecord = CRUDPatientMedicalRecord()

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
            complaints_list = request_dict.pop("complaints")
            diagnosis_list = request_dict.pop("diagnosis")
            medicines_list = request_dict.pop("medicines")
            medical_tests_list = request_dict.pop("medical_tests")
            logging.info("Creating PMR record")
            pmr_id = self.CRUDPatientMedicalRecord.create(**request_dict)
            logging.info(f"PMR record created with PMR_ID = {pmr_id}")
            logging.info("Creating complaint records")
            for complaint_obj in complaints_list:
                complaint_obj.update({"pmr_id": pmr_id})
                self.CRUDComplaint.create(**complaint_obj)
            logging.info("Creating diagnosis records")
            for diagnosis_obj in diagnosis_list:
                diagnosis_obj.update({"pmr_id": pmr_id})
                self.CRUDDiagnosis.create(**diagnosis_obj)
            logging.info("Creating medicines records")
            for medicines_obj in medicines_list:
                medicines_obj.update({"pmr_id": pmr_id})
                self.CRUDMedicines.create(**medicines_obj)
            logging.info("Creating medical tests records")
            for medical_tests_obj in medical_tests_list:
                medical_tests_obj.update({"pmr_id": pmr_id})
                self.CRUDMedicalTest.create(**medical_tests_obj)
            return {"pmr_id": pmr_id}
        except Exception as error:
            logging.error(
                f"Error in PMRController.create_pmr_controller function: {error}"
            )
            raise error

    def get_pmr_with_patientId(self, patient_id: int):
        """[Controller to create new pmr record]

        Args:
            patient_id ([int]): [patient id for getting pmr records]

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

    def get_pmr(self, pmr_id: int):
        """[Controller to create new pmr record]

        Args:
            patient_id ([int]): [patient id for getting pmr records]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing get pmr function")
            logging.info(f"Getting the PMR record for {pmr_id=}")
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
