from gateway import create_session, logger
from gateway.orm_models.lobster_schema.hiuConsent import HIUConsent
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDHIUConsents:
    def create(self, **kwargs):
        """[CRUD function to create a new Consent record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDConsents create request")
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
            consent = HIUConsent(**kwargs)
            with create_session() as transaction_session:
                transaction_session.add(consent)
                transaction_session.commit()
                transaction_session.refresh(consent)
        except Exception as error:
            logging.error(f"Error in CRUDConsents create function : {error}")
            raise error

    def read(self, consent_id: str):
        """[CRUD function to read a User record]

        Args:
            consent_id (str): [consent_id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDConsents read request")
            with create_session() as transaction_session:
                obj: HIUConsent = (
                    transaction_session.query(HIUConsent)
                    .filter(HIUConsent.id == consent_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            return None
        except Exception as error:
            logging.error(f"Error in CRUDConsents read function : {error}")
            raise error

    def read_by_abhaAddress(self, abha_address: str):
        """[CRUD function to read a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDConsents read request")
            with create_session() as transaction_session:
                obj: HIUConsent = (
                    transaction_session.query(HIUConsent)
                    .filter(HIUConsent.patient == abha_address)
                    .order_by(HIUConsent.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDConsents read function : {error}")
            raise error

    def read_approved_by_abhaAddress(self, abha_address: str):
        """[CRUD function to read a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDConsents read request")
            with create_session() as transaction_session:
                obj: HIUConsent = (
                    transaction_session.query(HIUConsent)
                    .filter(HIUConsent.patient == abha_address)
                    .filter(HIUConsent.status == "GRANTED")
                    .order_by(HIUConsent.created_at.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDConsents read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Users record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all user records]
        """
        try:
            logging.info("CRUDConsents read_all request")
            with create_session() as transaction_session:
                obj: HIUConsent = transaction_session.query(HIUConsent).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDConsents read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDConsents update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with create_session() as transaction_session:
                obj: HIUConsent = (
                    transaction_session.query(HIUConsent)
                    .filter(HIUConsent.id == kwargs.get("id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDConsents update function : {error}")
            raise error

    def delete(self, Consent_id: int):
        """[CRUD function to delete a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDConsents delete function")
            with create_session() as transaction_session:
                obj: HIUConsent = (
                    transaction_session.query(HIUConsent)
                    .filter(HIUConsent.id == Consent_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDConsents delete function : {error}")
            raise error
