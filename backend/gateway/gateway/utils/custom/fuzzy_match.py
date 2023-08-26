from gateway.crud.hims_patientDetails_crud import CRUDPatientDetails
from gateway import logger

logging = logger(__name__)


class FuzzyMatch:
    def __init__(self):
        self.patient_list = []
        self.matched_by = None

    def attribute_match(self, discover_request):
        try:
            matched_obj = {}
            logging.info("Fuzzy Matching attribute_match initiated")
            logging.info(f"{self.patient_list=}")
            for patient_obj in self.patient_list:
                logging.info(f"{patient_obj=}")
                if discover_request.get("gender", None):
                    if discover_request.get("gender") == patient_obj.get("gender"):
                        patient_obj.update({"matched_by": self.matched_by})
                        matched_obj.update({patient_obj.get("id"): patient_obj})
                        continue
                    if discover_request.get("name") == patient_obj.get("name"):
                        patient_obj.update({"matched_by": self.matched_by})
                        matched_obj.update({patient_obj.get("id"): patient_obj})
                        continue
                    if discover_request.get("yearOfBirth") == int(
                        patient_obj.get("DOB").split("/")[-1]
                    ):
                        patient_obj.update({"matched_by": self.matched_by})
                        matched_obj.update({patient_obj.get("id"): patient_obj})
                        continue
            return matched_obj
        except Exception as error:
            logging.error(f"Error in FuzzyMatch.attribute_match function: {error}")
            raise error

    def find_record(self, request):
        try:
            logging.info("Fuzzy Matching find_record initiated")
            discover_request = request.get("patient")
            logging.info(f"{discover_request=}")
            list_of_verifiedIdentifiers = discover_request.get("verifiedIdentifiers")
            list_of_unverifiedIdentifiers = discover_request.get(
                "unverifiedIdentifiers"
            )
            logging.info(f"{list_of_verifiedIdentifiers=}")
            logging.info(f"{list_of_unverifiedIdentifiers=}")
            for verifiedIdentifier in list_of_verifiedIdentifiers:
                if verifiedIdentifier.get("type") == "MOBILE":
                    patient_recs = CRUDPatientDetails().read_multiple_by_mobileNumber(
                        mobile_number=verifiedIdentifier.get("value")
                    )
                    if len(patient_recs) > 0:
                        self.patient_list = patient_recs
                        self.matched_by = verifiedIdentifier.get("type")
                        break
                elif verifiedIdentifier.get("type") == "NDHM_HEALTH_NUMBER":
                    patient_recs = CRUDPatientDetails().read_multiple_by_abhaId(
                        abha_number=verifiedIdentifier.get("value")
                    )
                    if len(patient_recs) > 0:
                        self.patient_list = patient_recs
                        self.matched_by = verifiedIdentifier.get("type")
                        break
                elif verifiedIdentifier.get("type") == "HEALTH_ID":
                    patient_recs = CRUDPatientDetails().read_multiple_by_abhaAddress(
                        abha_address=verifiedIdentifier.get("value")
                    )
                    if len(patient_recs) > 0:
                        self.patient_list = patient_recs
                        self.matched_by = verifiedIdentifier.get("type")
                        break
            if len(list_of_unverifiedIdentifiers) > 0:
                # TODO: add unverified flow
                pass
            matching_results = self.attribute_match(discover_request=discover_request)
            return matching_results
        except Exception as error:
            logging.error(f"Error in FuzzyMatch.find_record function: {error}")
            raise error
