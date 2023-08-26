from core import create_session, logger
from core.orm_models.hospital_schema.users import Users
from core.orm_models.hospital_schema.userRoles import UserRoles
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
            with create_session() as transaction_session:
                transaction_session.add(user)
                transaction_session.commit()
                transaction_session.refresh(user)
            return user.id
        except Exception as error:
            logging.error(f"Error in CRUDUser create function : {error}")
            raise error

    def read(self, username: str):
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
            with create_session() as transaction_session:
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

    def read_joined(self, username: str):
        """[CRUD function to read_joined a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDUser read_joined request")
            user_details_obj = {}
            with create_session() as transaction_session:
                user_role_list = []
                for user_obj, user_role_obj in (
                    transaction_session.query(Users, UserRoles)
                    .filter(Users.username == username)
                    .filter(UserRoles.user_id == Users.id)
                    .all()
                ):
                    user_details_obj = user_obj.__dict__
                    user_role_dict = user_role_obj.__dict__
                    user_role = user_role_dict.get("user_role").value
                    user_role_list.append(user_role)
                    user_details_obj.update({"user_roles": user_role_list})
            return user_details_obj
        except Exception as error:
            logging.error(f"Error in CRUDUser read_joined function : {error}")
            raise error

    def read_all_old(self):
        """[CRUD function to read_all Users record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all user records]
        """
        try:
            logging.info("CRUDUser read_all request")
            with create_session() as transaction_session:
                obj: Users = transaction_session.query(Users).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDUser read_all function : {error}")
            raise error

    def read_all(self):
        try:
            logging.info("CRUDUser read_all request")
            users_dict = {}
            with create_session() as transaction_session:
                for user_obj, user_role_obj in (
                    transaction_session.query(Users, UserRoles)
                    .filter(UserRoles.user_id == Users.id)
                    .all()
                ):
                    user_id = user_obj.id
                    if user_id not in users_dict:
                        users_dict[user_id] = user_obj.__dict__
                        users_dict[user_id]["user_roles"] = []

                    user_role_dict = user_role_obj.__dict__
                    user_role = user_role_dict.get("user_role").value
                    users_dict[user_id]["user_roles"].append(user_role)

                serialized_users = list(users_dict.values())
                return serialized_users
        except Exception as error:
            logging.error(f"Error in CRUDUser read_all function: {error}")
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
            with create_session() as transaction_session:
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
            with create_session() as transaction_session:
                obj: Users = (
                    transaction_session.query(Users)
                    .filter(Users.username == email_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDUser delete function : {error}")
            raise error
