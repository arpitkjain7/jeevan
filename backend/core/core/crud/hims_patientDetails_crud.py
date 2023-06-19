from core import session, logger
from core.orm_models.hims_patientDetails import PatientDetails
from datetime import datetime
from pytz import timezone

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

    def read_by_abhaId(self, abha_number: str):
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
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails read function : {error}")
            raise error

    def read_multiple_by_abhaId(self, abha_number: str):
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

    def read_by_mobileNumber(self, mobile_number: str):
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
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDPatientDetails read function : {error}")
            raise error

    def read_multiple_by_mobileNumber(self, mobile_number: str):
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

    def read_multiple_by_abhaAddress(self, abha_address: str):
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
            logging.info("CRUDPatientDetails read request")
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
            logging.error(f"Error in CRUDPatientDetails read function : {error}")
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
            if obj is not None:
                return [
                    [row.__dict__] for row in obj
                ]  # testing return [row.__dict__ for row in obj]
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