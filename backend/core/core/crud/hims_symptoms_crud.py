from core import session, logger
from core.orm_models.hims_symptoms import Symptoms
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDSymptoms:
    def create(self, **kwargs):
        """[CRUD function to create a new Symptoms record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDSymptoms create request")
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
            symptoms = Symptoms(**kwargs)
            with session() as transaction_session:
                transaction_session.add(symptoms)
                transaction_session.commit()
                transaction_session.refresh(symptoms)
            return symptoms.id
        except Exception as error:
            logging.error(f"Error in CRUDSymptoms create function : {error}")
            raise error

    def read_by_pmrId(self, pmr_id: int):
        """[CRUD function to read a Symptoms record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Symptoms record matching the criteria]
        """
        try:
            logging.info("CRUDSymptoms read request")
            with session() as transaction_session:
                obj: Symptoms = (
                    transaction_session.query(Symptoms)
                    .filter(Symptoms.pmr_id == pmr_id)
                    .order_by(Symptoms.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDSymptoms read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Symptoms record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Symptoms records]
        """
        try:
            logging.info("CRUDSymptoms read_all request")
            with session() as transaction_session:
                obj: Symptoms = transaction_session.query(Symptoms).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDSymptoms read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a Symptoms record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDSymptoms update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: Symptoms = (
                    transaction_session.query(Symptoms)
                    .filter(Symptoms.id == kwargs["id"])
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDSymptoms update function : {error}")
            raise error

    def delete(self, symptoms_id: int):
        """[CRUD function to delete a Symptoms record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDSymptoms delete function")
            with session() as transaction_session:
                obj: Symptoms = (
                    transaction_session.query(Symptoms)
                    .filter(Symptoms.id == symptoms_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDSymptoms delete function : {error}")
            raise error

    def delete_all(self, pmr_id: str):
        """[CRUD function to delete_all a Symptoms record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDSymptoms delete_all function")
            with session() as transaction_session:
                obj: Symptoms = (
                    transaction_session.query(Symptoms)
                    .filter(Symptoms.pmr_id == pmr_id)
                    .delete(synchronize_session=False)
                )
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDSymptoms delete_all function : {error}")
            raise error
