from core import create_session, logger
from core.orm_models.hospital_schema.labInvestigations import LabInvestigations
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDLabInvestigation:
    def create(self, **kwargs):
        """[CRUD function to create a new Medical Test record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("`CRUDLabInvestigation` create request")
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
            lab_investigation = LabInvestigations(**kwargs)
            with create_session() as transaction_session:
                transaction_session.add(lab_investigation)
                transaction_session.commit()
                transaction_session.refresh(lab_investigation)
            return lab_investigation.id
        except Exception as error:
            logging.error(f"Error in CRUDLabInvestigation create function : {error}")
            raise error

    def read_by_pmrId(self, pmr_id: str):
        """[CRUD function to read a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDLabInvestigation read request")
            with create_session() as transaction_session:
                obj: LabInvestigations = (
                    transaction_session.query(LabInvestigations)
                    .filter(LabInvestigations.pmr_id == pmr_id)
                    .order_by(LabInvestigations.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDLabInvestigation read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Users record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all user records]
        """
        try:
            logging.info("CRUDLabInvestigation read_all request")
            with create_session() as transaction_session:
                obj: LabInvestigations = transaction_session.query(
                    LabInvestigations
                ).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDLabInvestigation read_all function : {error}")
            raise error

    def update(self, id: str, **kwargs):
        """[CRUD function to update a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDLabInvestigation update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with create_session() as transaction_session:
                obj: LabInvestigations = (
                    transaction_session.query(LabInvestigations)
                    .filter(LabInvestigations.id == id)
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDMedicalTest update function : {error}")
            raise error

    def delete(self, lab_investigation_id: int):
        """[CRUD function to delete a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDLabInvestigation delete function")
            with create_session() as transaction_session:
                obj: LabInvestigations = (
                    transaction_session.query(LabInvestigations)
                    .filter(LabInvestigations.id == LabInvestigations)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDLabInvestigation delete function : {error}")
            raise error

    def delete_all(self, pmr_id: str):
        """[CRUD function to delete_all a Diagnosis record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDLabInvestigation delete_all function")
            with create_session() as transaction_session:
                obj: LabInvestigations = (
                    transaction_session.query(LabInvestigations)
                    .filter(LabInvestigations.pmr_id == pmr_id)
                    .delete(synchronize_session=False)
                )
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(
                f"Error in CRUDLabInvestigation delete_all function : {error}"
            )
            raise error
