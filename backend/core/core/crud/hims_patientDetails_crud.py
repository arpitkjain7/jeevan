from core import session, logger
from core.orm_models.hims_patientDetails import PatientDetails
from datetime import datetime, timedelta
from pytz import timezone
from core.utils.custom.patient_helper import calculate_age
import pytz

logging = logger(__name__)


class CRUDPatientDetails:
    def create(self, **kwargs):
        """[CRUD function to create a new PatientDetails record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientDetails create request")
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
            patient_details = PatientDetails(**kwargs)
            with session() as transaction_session:
                transaction_session.add(patient_details)
                transaction_session.commit()
                transaction_session.refresh(patient_details)
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails create function : {error}")
            raise error

    def read_by_abhaId(self, abha_number: str, hip_id: str):
        """[CRUD function to read a PatientDetails record]

        Args:
            abha_number (str): [ABHA Number to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientDetails record matching the criteria]
        """
        try:
            logging.info("CRUDPatientDetails read request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.abha_number == abha_number)
                    .filter(PatientDetails.hip_id == hip_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails read function : {error}")
            raise error

    def read_multiple_by_abhaId(self, abha_number: str, hip_id: str):
        """[CRUD function to read a PatientDetails record]

        Args:
            abha_number (str): [ABHA Number to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientDetails record matching the criteria]
        """
        try:
            logging.info("CRUDPatientDetails read request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.abha_number == abha_number)
                    .filter(PatientDetails.hip_id == hip_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientDetails read_multiple_by_abhaId function : {error}"
            )
            raise error

    def read_by_aadharNumber(self, aadhar_number: str):
        """[CRUD function to read a PatientDetails record]

        Args:
            aadhar_number (str): [AADHAR NUMBER to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientDetails record matching the criteria]
        """
        try:
            logging.info("CRUDPatientDetails read request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.aadhar_number == aadhar_number)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails read function : {error}")
            raise error

    def read_by_mobileNumber(self, mobile_number: str, hip_id: str):
        """[CRUD function to read a PatientDetails record]

        Args:
            mobile_number (str): [Mobile Number to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientDetails record matching the criteria]
        """
        try:
            logging.info("CRUDPatientDetails read_by_mobileNumber request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.mobile_number == mobile_number)
                    .filter(PatientDetails.hip_id == hip_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientDetails read_by_mobileNumber function : {error}"
            )
            raise error

    def read_multiple_by_mobileNumber(self, mobile_number: str, hip_id: str):
        """[CRUD function to read a PatientDetails record]

        Args:
            mobile_number (str): [Mobile Number to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientDetails record matching the criteria]
        """
        try:
            logging.info("CRUDPatientDetails read request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.mobile_number == mobile_number)
                    .filter(PatientDetails.hip_id == hip_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails read function : {error}")
            raise error

    def read_by_abhaAddress(self, abha_address: str):
        """[CRUD function to read a PatientDetails record]

        Args:
            mobile_number (str): [Mobile Number to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientDetails record matching the criteria]
        """
        try:
            logging.info("CRUDPatientDetails read request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.abha_address == abha_address)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails read function : {error}")
            raise error

    def read_multiple_by_abhaAddress(self, abha_address: str, hip_id: str):
        """[CRUD function to read a PatientDetails record]

        Args:
            mobile_number (str): [Mobile Number to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientDetails record matching the criteria]
        """
        try:
            logging.info("CRUDPatientDetails read request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.abha_address == abha_address)
                    .filter(PatientDetails.hip_id == hip_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails read function : {error}")
            raise error

    def read_by_patientId(self, patient_id: int):
        """[CRUD function to read a PatientDetails record]

        Args:
            patient_id (str): [patient_id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientDetails record matching the criteria]
        """
        try:
            logging.info("CRUDPatientDetails read_by_patientId request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.id == patient_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientDetails read_by_patientId function : {error}"
            )
            raise error

    def read_by_patientUId(self, patient_uid: str, hip_id: str):
        try:
            logging.info("CRUDPatientDetails read_by_patientUId request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.patient_uid == patient_uid)
                    .filter(PatientDetails.hip_id == hip_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientDetails read_by_patientUId function : {error}"
            )
            raise error

    def read_by_name(self, name: str, DOB: str):
        """[CRUD function to read a PatientDetails record]

        Args:
            name (str): [name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientDetails record matching the criteria]
        """
        try:
            logging.info("CRUDPatientDetails read request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.name == name)
                    .filter(PatientDetails.DOB == DOB)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails read function : {error}")
            raise error

    def read_by_mobile_dob_hip(self, mobile_number: str, DOB: str, hip_id: str):
        """[CRUD function to read a PatientDetails record]

        Args:
            name (str): [name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientDetails record matching the criteria]
        """
        try:
            logging.info("CRUDPatientDetails read_by_mobile_dob request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.mobile_number == mobile_number)
                    .filter(PatientDetails.DOB == DOB)
                    .filter(PatientDetails.hip_id == hip_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientDetails read_by_mobile_dob function : {error}"
            )
            raise error

    def read_by_mobile_name(self, mobile_number: str, name: str):
        """[CRUD function to read a PatientDetails record]

        Args:
            name (str): [name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [PatientDetails record matching the criteria]
        """
        try:
            logging.info("CRUDPatientDetails read_by_mobile_dob request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.mobile_number == mobile_number)
                    .filter(PatientDetails.name == name)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientDetails read_by_mobile_dob function : {error}"
            )
            raise error

    def read_all(self, hip_id: str):
        """[CRUD function to read_all PatientDetails record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all PatientDetails records]
        """
        try:
            logging.info("CRUDPatientDetails read_all request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.hip_id == hip_id)
                    .order_by(PatientDetails.created_at.desc())
                    .all()
                )
            result = []
            if obj is not None:
                for row in obj:
                    patient_obj = row.__dict__
                    patient_dob = patient_obj.get("DOB", None)
                    if patient_dob:
                        dob = datetime.strptime(patient_dob, "%Y-%m-%d")
                        age_in_years, age_in_months = calculate_age(dob=dob)
                        patient_obj["age_in_years"] = age_in_years
                        patient_obj["age_in_months"] = age_in_months
                    else:
                        patient_yob = patient_obj.get("year_of_birth", None)
                        today = datetime.today()
                        age_in_years = today.year - int(patient_yob)
                        patient_obj["age_in_years"] = age_in_years

                    result.append(patient_obj)
                return result  # testing return [row.__dict__ for row in obj]
            return result
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails read_all function : {error}")
            raise error

    def read_verified(self, hip_id: str):
        """[CRUD function to read_verified PatientDetails record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all PatientDetails records]
        """
        try:
            logging.info("CRUDPatientDetails read_verified request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.hip_id == hip_id)
                    .order_by(PatientDetails.created_at.desc())
                    .all()
                )
            result = []
            if obj is not None:
                for row in obj:
                    patient_obj = row.__dict__
                    patient_dob = patient_obj.get("DOB", None)
                    if patient_dob:
                        dob = datetime.strptime(patient_dob, "%Y-%m-%d")
                        age_in_years, age_in_months = calculate_age(dob=dob)
                        patient_obj["age_in_years"] = age_in_years
                        patient_obj["age_in_months"] = age_in_months
                    else:
                        patient_yob = patient_obj.get("year_of_birth", None)
                        today = datetime.today()
                        age_in_years = today.year - int(patient_yob)
                        patient_obj["age_in_years"] = age_in_years
                    patient_verified = patient_obj.get("is_verified")
                    if patient_verified:
                        result.append(patient_obj)
                    else:
                        last_updated_date = patient_obj.get("updated_at")
                        threshold_datetime = last_updated_date + timedelta(minutes=30)
                        threshold_datetime = threshold_datetime.replace(tzinfo=pytz.UTC)
                        now_datetime = datetime.now(timezone("Asia/Kolkata"))
                        now_datetime.replace(tzinfo=pytz.UTC)
                        threshold_time = threshold_datetime.time()
                        now_time = now_datetime.time()
                        if now_time < threshold_time:
                            result.append(patient_obj)
                return result
            return result
        except Exception as error:
            logging.error(
                f"Error in CRUDPatientDetails read_verified function : {error}"
            )
            raise error

    def read_by_hip(self, hip_id: str):
        """[CRUD function to read_all PatientDetails record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all PatientDetails records]
        """
        try:
            logging.info("CRUDPatientDetails read_all request")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.hip_id == hip_id)
                    .order_by(PatientDetails.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a PatientDetails record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientDetails update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.id == kwargs.get("id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails update function : {error}")
            raise error

    def update_by_abhaNumber(self, **kwargs):
        """[CRUD function to update a PatientDetails record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientDetails update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.abha_number == kwargs.get("abha_number"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails update function : {error}")
            raise error

    def delete(self, patient_id: int):
        """[CRUD function to delete a PatientDetails record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDPatientDetails delete function")
            with session() as transaction_session:
                obj: PatientDetails = (
                    transaction_session.query(PatientDetails)
                    .filter(PatientDetails.id == patient_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails delete function : {error}")
            raise error
