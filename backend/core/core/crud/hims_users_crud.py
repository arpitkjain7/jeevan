from core import session, logger
from core.orm_models.hims_users import Users
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDUser:
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
            user = Users(**kwargs)
            with session() as transaction_session:
                transaction_session.add(user)
                transaction_session.commit()
                transaction_session.refresh(user)
        except Exception as error:
            logging.error(f"Error in CRUDUser create function : {error}")
            raise error

    def read_by_username(self, username: str):
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
                obj: Users = (
                    transaction_session.query(Users)
                    .filter(Users.username == username)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDUser read function : {error}")
            raise error

    def read_by_userid(self, user_id: int):
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
                obj: Users = (
                    transaction_session.query(Users).filter(Users.id == user_id).first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDUser read function : {error}")
            raise error

    def read_by_mobilenumber(self, mobile_number: str):
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
                obj: Users = (
                    transaction_session.query(Users)
                    .filter(Users.mobile_number == mobile_number)
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
                obj: Users = transaction_session.query(Users).all()
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
                obj: Users = (
                    transaction_session.query(Users)
                    .filter(Users.username == kwargs.get("username"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDUser update function : {error}")
            raise error

    def delete(self, email_id: str):
        """[CRUD function to delete a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDUser delete function")
            with session() as transaction_session:
                obj: Users = (
                    transaction_session.query(Users)
                    .filter(Users.email_id == email_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDUser delete function : {error}")
            raise error
