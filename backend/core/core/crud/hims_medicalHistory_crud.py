from core import session, logger
from core.orm_models.hims_medicalHistory import MedicalHistory
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDMedicalHistory:
    def create(self, **kwargs):
        """[CRUD function to create a new MedicalHistory record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicalHistory create request")
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
            medicalHistory = MedicalHistory(**kwargs)
            with session() as transaction_session:
                transaction_session.add(medicalHistory)
                transaction_session.commit()
                transaction_session.refresh(medicalHistory)
            return medicalHistory.id
        except Exception as error:
            logging.error(f"Error in CRUDMedicalHistory create function : {error}")
            raise error

    def read_by_pmrId(self, pmr_id: int):
        """[CRUD function to read a medicalHistory record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [MedicalHistory record matching the criteria]
        """
        try:
            logging.info("CRUDMedicalHistory read request")
            with session() as transaction_session:
                obj: MedicalHistory = (
                    transaction_session.query(MedicalHistory)
                    .filter(MedicalHistory.pmr_id == pmr_id)
                    .order_by(MedicalHistory.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDMedicalHistory read function : {error}")
            raise error

    def read_self_by_pmrId(self, pmr_id: int):
        """[CRUD function to read a medicalHistory record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [MedicalHistory record matching the criteria]
        """
        try:
            logging.info("CRUDMedicalHistory read request")
            with session() as transaction_session:
                obj: MedicalHistory = (
                    transaction_session.query(MedicalHistory)
                    .filter(MedicalHistory.pmr_id == pmr_id)
                    .filter(MedicalHistory.relationship == "self")
                    .order_by(MedicalHistory.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDMedicalHistory read function : {error}")
            raise error

    def read_others_by_pmrId(self, pmr_id: int):
        """[CRUD function to read a medicalHistory record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [MedicalHistory record matching the criteria]
        """
        try:
            logging.info("CRUDMedicalHistory read request")
            with session() as transaction_session:
                obj: MedicalHistory = (
                    transaction_session.query(MedicalHistory)
                    .filter(MedicalHistory.pmr_id == pmr_id)
                    .filter(MedicalHistory.relationship != "self")
                    .order_by(MedicalHistory.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDMedicalHistory read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all MedicalHistory record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all MedicalHistory records]
        """
        try:
            logging.info("CRUDMedicalHistory read_all request")
            with session() as transaction_session:
                obj: MedicalHistory = transaction_session.query(MedicalHistory).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDMedicalHistory read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a MedicalHistory record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicalHistory update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: MedicalHistory = (
                    transaction_session.query(MedicalHistory)
                    .filter(MedicalHistory.id == kwargs["id"])
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDMedicalHistory update function : {error}")
            raise error

    def delete(self, medicalHistory_id: int):
        """[CRUD function to delete a MedicalHistory record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicalHistory delete function")
            with session() as transaction_session:
                obj: MedicalHistory = (
                    transaction_session.query(MedicalHistory)
                    .filter(MedicalHistory.id == medicalHistory_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDMedicalHistory delete function : {error}")
            raise error

    def delete_all(self, pmr_id: str):
        """[CRUD function to delete_all  MedicalHistory record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicalHistory delete_all function")
            with session() as transaction_session:
                obj: MedicalHistory = (
                    transaction_session.query(MedicalHistory)
                    .filter(MedicalHistory.pmr_id == pmr_id)
                    .delete(synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDMedicalHistory delete_all function : {error}")
            raise error
