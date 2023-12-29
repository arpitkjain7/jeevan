from core import session, logger
from core.orm_models.hims_examinationFindings import ExaminationFindings
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDExaminationFindings:
    def create(self, **kwargs):
        """[CRUD function to create a new ExaminationFindings record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDExaminationFindings create request")
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
            examination_findings = ExaminationFindings(**kwargs)
            with session() as transaction_session:
                transaction_session.add(examination_findings)
                transaction_session.commit()
                transaction_session.refresh(examination_findings)
            return examination_findings.id
        except Exception as error:
            logging.error(f"Error in CRUDExaminationFindings create function : {error}")
            raise error

    def read_by_pmrId(self, pmr_id: int):
        """[CRUD function to read a examination_findings record]

        Args:
            pmr_id (str): [Patient Medical Record Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [ExaminationFindings record matching the criteria]
        """
        try:
            logging.info("CRUDExaminationFindings read request")
            with session() as transaction_session:
                obj: ExaminationFindings = (
                    transaction_session.query(ExaminationFindings)
                    .filter(ExaminationFindings.pmr_id == pmr_id)
                    .order_by(ExaminationFindings.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDExaminationFindings read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all ExaminationFindings record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all ExaminationFindings records]
        """
        try:
            logging.info("CRUDExaminationFindings read_all request")
            with session() as transaction_session:
                obj: ExaminationFindings = transaction_session.query(
                    ExaminationFindings
                ).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDExaminationFindings read_all function : {error}"
            )
            raise error

    def read(self, id: int):
        """[CRUD function to read ExaminationFindings record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all ExaminationFindings records]
        """
        try:
            logging.info("CRUDExaminationFindings read request")
            with session() as transaction_session:
                obj: ExaminationFindings = (
                    transaction_session.query(ExaminationFindings)
                    .filter(ExaminationFindings.id == id)
                    .first()
                )
            if obj:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDExaminationFindings read function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a ExaminationFindings record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDExaminationFindings update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: ExaminationFindings = (
                    transaction_session.query(ExaminationFindings)
                    .filter(ExaminationFindings.id == kwargs["id"])
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDExaminationFindings update function : {error}")
            raise error

    def delete(self, examination_findings_id: int):
        """[CRUD function to delete a ExaminationFindings record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDExaminationFindings delete function")
            with session() as transaction_session:
                obj: ExaminationFindings = (
                    transaction_session.query(ExaminationFindings)
                    .filter(ExaminationFindings.id == examination_findings_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDExaminationFindings delete function : {error}")
            raise error

    def delete_all(self, pmr_id: str):
        """[CRUD function to delete_all  ExaminationFindings record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDExaminationFindings delete_all function")
            with session() as transaction_session:
                obj: ExaminationFindings = (
                    transaction_session.query(ExaminationFindings)
                    .filter(ExaminationFindings.pmr_id == pmr_id)
                    .delete(synchronize_session=False)
                )
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(
                f"Error in CRUDExaminationFindings delete_all function : {error}"
            )
            raise error
