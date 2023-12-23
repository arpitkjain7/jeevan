from core import session, logger
from core.orm_models.hims_medicines import Medicines
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDMedicines:
    def create(self, **kwargs):
        """[CRUD function to create a new Appointment record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicines create request")
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
            medicines = Medicines(**kwargs)
            with session() as transaction_session:
                transaction_session.add(medicines)
                transaction_session.commit()
                transaction_session.refresh(medicines)
            return medicines.id
        except Exception as error:
            logging.error(f"Error in CRUDMedicines create function : {error}")
            raise error

    def read_by_pmrId(self, pmr_id: int):
        """[CRUD function to read a Medicines record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Medicines record matching the criteria]
        """
        try:
            logging.info("CRUDMedicines read request")
            with session() as transaction_session:
                obj: Medicines = (
                    transaction_session.query(Medicines)
                    .filter(Medicines.pmr_id == pmr_id)
                    .order_by(Medicines.created_at.desc())
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return []
        except Exception as error:
            logging.error(f"Error in CRUDMedicines read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Medicines record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all Medicines records]
        """
        try:
            logging.info("CRUDMedicines read_all request")
            with session() as transaction_session:
                obj: Medicines = transaction_session.query(Medicines).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDMedicines read_all function : {error}")
            raise error

    def update(self, id: str, **kwargs):
        """[CRUD function to update a Medicines record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicines update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: Medicines = (
                    transaction_session.query(Medicines)
                    .filter(Medicines.id == id)
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDMedicines update function : {error}")
            raise error

    def delete(self, medicine_id: int):
        """[CRUD function to delete a Medicines record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicines delete function")
            with session() as transaction_session:
                obj: Medicines = (
                    transaction_session.query(Medicines)
                    .filter(Medicines.id == medicine_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDMedicines delete function : {error}")
            raise error

    def delete_all(self, pmr_id: str):
        """[CRUD function to delete_all a Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDMedicines delete_all function")
            with session() as transaction_session:
                obj: Medicines = (
                    transaction_session.query(Medicines)
                    .filter(Medicines.pmr_id == pmr_id)
                    .delete(synchronize_session=False)
                )
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDMedicines delete_all function : {error}")
            raise error
