from core import session, logger
from core.orm_models.hims_hipDetails import HIPDetail
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDHIP:
    def create(self, **kwargs):
        """[CRUD function to create a new User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDUser create request")
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
            hip_details = HIPDetail(**kwargs)
            with session() as transaction_session:
                transaction_session.add(hip_details)
                transaction_session.commit()
                transaction_session.refresh(hip_details)
            return hip_details.id
        except Exception as error:
            logging.error(f"Error in CRUDUser create function : {error}")
            raise error

    def read(self, hip_ip: str):
        """[CRUD function to read a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDUser read request")
            with session() as transaction_session:
                obj: HIPDetail = (
                    transaction_session.query(HIPDetail)
                    .filter(HIPDetail.hip_id == hip_ip)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDUser read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Users record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all user records]
        """
        try:
            logging.info("CRUDUser read_all request")
            with session() as transaction_session:
                obj: HIPDetail = transaction_session.query(HIPDetail).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDUser read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDUser update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: HIPDetail = (
                    transaction_session.query(HIPDetail)
                    .filter(HIPDetail.hip_id == kwargs.get("hip_id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDUser update function : {error}")
            raise error

    def delete(self, hip_id: str):
        """[CRUD function to delete a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDUser delete function")
            with session() as transaction_session:
                obj: HIPDetail = (
                    transaction_session.query(HIPDetail)
                    .filter(HIPDetail.hip_id == hip_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDUser delete function : {error}")
            raise error
