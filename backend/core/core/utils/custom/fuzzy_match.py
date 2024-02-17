from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core import logger
import jellyfish
from fuzzywuzzy import fuzz

logging = logger(__name__)


class FuzzyMatch:
    def __init__(self):
        self.patient_list = []
        self.matched_by = None

    def get_phonitic_match(source_name: str, target_name: str):
        try:
            source_name_code = jellyfish.soundex(source_name)
            target_name_code = jellyfish.soundex(target_name)
            return fuzz.ratio(source_name_code, target_name_code)
        except Exception as error:
            logging.error(f"Error in FuzzyMatch.get_phonitic_match function: {error}")
            raise error

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

    def find_record(self, request, hip_id):
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
                        mobile_number=verifiedIdentifier.get("value"), hip_id=hip_id
                    )
                    if len(patient_recs) > 0:
                        self.patient_list = patient_recs
                        self.matched_by = verifiedIdentifier.get("type")
                        break
                elif verifiedIdentifier.get("type") == "NDHM_HEALTH_NUMBER":
                    patient_recs = CRUDPatientDetails().read_multiple_by_abhaId(
                        abha_number=verifiedIdentifier.get("value"), hip_id=hip_id
                    )
                    if len(patient_recs) > 0:
                        self.patient_list = patient_recs
                        self.matched_by = verifiedIdentifier.get("type")
                        break
                elif verifiedIdentifier.get("type") == "HEALTH_ID":
                    patient_recs = CRUDPatientDetails().read_multiple_by_abhaAddress(
                        abha_address=verifiedIdentifier.get("value"), hip_id=hip_id
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

    def find_duplicate_record(self, mobile_number, name, dob, gender, hip_id):
        try:
            logging.info("Fuzzy Matching find_duplicate_record initiated")
            patient_recs = CRUDPatientDetails().read_by_mobileNumber(
                mobile_number=mobile_number
            )
            if patient_recs:
                if gender == patient_recs.get("gender"):
                    patient_birth_year = patient_recs.get("DOB").split("-")[0]
                    if int(dob) - 2 <= patient_birth_year <= int(dob) + 2:
                        patient_name = patient_recs.get("name")
                        phonotic_match_ratio = self.get_phonitic_match(
                            source_name=name, target_name=patient_name
                        )
                        if phonotic_match_ratio >= 80:
                            return patient_recs
                        else:
                            return None
                    else:
                        return None
                else:
                    return None
            else:
                return None

        except Exception as error:
            logging.error(
                f"Error in FuzzyMatch.find_duplicate_record function: {error}"
            )
            raise error
