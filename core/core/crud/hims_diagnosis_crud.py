from core import session, logger
from core.orm_models.hims_diagnosis import Diagnosis
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDDiagnosis:
    def create(self, **kwargs):
        """[CRUD function to create a new Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDDiagnosis create request")
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
            diagnosis = Diagnosis(**kwargs)
            with session() as transaction_session:
                transaction_session.add(diagnosis)
                transaction_session.commit()
                transaction_session.refresh(diagnosis)
        except Exception as error:
            logging.error(f"Error in CRUDDiagnosis create function : {error}")
            raise error

    def read_by_pmrId(self, pmr_id: int):
        """[CRUD function to read a Diagnosis record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Diagnosis record matching the criteria]
        """
        try:
            logging.info("CRUDDiagnosis read request")
            with session() as transaction_session:
                obj: Diagnosis = (
                    transaction_session.query(Diagnosis)
                    .filter(Diagnosis.pmr_id == pmr_id)
                    .order_by(Diagnosis.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDDiagnosis read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Diagnosis records]
        """
        try:
            logging.info("CRUDDiagnosis read_all request")
            with session() as transaction_session:
                obj: Diagnosis = transaction_session.query(Diagnosis).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDDiagnosis read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDDiagnosis update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: Diagnosis = (
                    transaction_session.query(Diagnosis)
                    .filter(Diagnosis.id == kwargs.get("id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDDiagnosis update function : {error}")
            raise error

    def delete(self, diagnosis_id: int):
        """[CRUD function to delete a Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDDiagnosis delete function")
            with session() as transaction_session:
                obj: Diagnosis = (
                    transaction_session.query(Diagnosis)
                    .filter(Diagnosis.id == diagnosis_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDDiagnosis delete function : {error}")
            raise error

    def delete_all(self, pmr_id: str):
        """[CRUD function to delete_all a Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDDiagnosis delete_all function")
            with session() as transaction_session:
                obj: Diagnosis = (
                    transaction_session.query(Diagnosis)
                    .filter(Diagnosis.pmr_id == pmr_id)
                    .delete(synchronize_session=False)
                )
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDDiagnosis delete_all function : {error}")
            raise error
