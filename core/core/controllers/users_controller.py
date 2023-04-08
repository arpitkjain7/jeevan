from core.crud.hims_users_crud import CRUDUser
from commons.auth import encrypt_password, verify_hash_password, signJWT
from core import logger

logging = logger(__name__)


class UserManagementController:
    def __init__(self):
        self.CRUDUser = CRUDUser()

    def register_user_controller(self, request):
        """[Controller to register new user]

        Args:
            request ([dict]): [create new user request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing register new user function")
            request_json = request.dict()
            password_hash = encrypt_password(password=request_json.get("password"))
            user_obj = self.CRUDUser.read(username=request_json.get("username"))
            if user_obj is not None:
                return {
                    "access_token": None,
                    "token_type": "bearer",
                    "user_role": request_json.get("user_role"),
                    "status": "User already exists",
                }
            else:
                request_json.update({"password": password_hash})
                self.CRUDUser.create(**request_json)
                access_token = signJWT(
                    email=request_json.get("username"),
                    user_role=request_json.get("user_role"),
                    department=request_json.get("department"),
                )
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user_role": request_json.get("user_role"),
                    "status": "New user created successfully",
                }
        except Exception as error:
            logging.error(f"Error in register_user_controller function: {error}")
            raise error

    def login_user_controller(self, request):
        """[Controller for user login]

        Args:
            request ([dict]): [user login details]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing login user function")
            user_obj = self.CRUDUser.read(username=request.username)
            if user_obj:
                if verify_hash_password(
                    plain_password=request.password,
                    hashed_password=user_obj.get("password"),
                ):
                    access_token = signJWT(
                        email=request.username,
                        user_role=user_obj.get("user_role"),
                        department=user_obj.get("department"),
                    )
                    logging.info(f"{user_obj=}")
                    del user_obj["password"]
                    user_obj.update(
                        {"access_token": access_token, "token_type": "bearer"}
                    )
                    return user_obj
                else:
                    return None
            else:
                return None
        except Exception as error:
            logging.error(f"Error in login_user_controller function: {error}")
            raise error

    def get_all_users_controller(self):
        """[Controller to get all users]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [list]: [list of all the users in the system]
        """
        try:
            logging.info("executing get_all_users_controller function")
            user_list = self.CRUDUser.read_all()
            user_list_new = []
            for user_obj in user_list:
                user_obj.pop("password")
                user_list_new.append(user_obj)
            return user_list_new
        except Exception as error:
            logging.error(f"Error in get_all_users_controller function: {error}")
            raise {"error": "Invalid username or password"}

    def get_user_controller(self, username: str):
        """[Get User Details]

        Args:
            username (str): [Username of the user]

        Returns:
            [dict]: [User details]
        """
        try:
            logging.info("executing get_all_users_controller function")
            user_obj = self.CRUDUser.read(username=username)
            del user_obj["password"]
            return user_obj
        except Exception as error:
            logging.error(f"Error in get_all_users_controller function: {error}")
            raise {"error": "Invalid username or password"}

    def delete_user_controller(self, email: str):
        """[Controller to delete a user]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [deleted user details]
        """
        try:
            logging.info("executing delete_user_controller function")
            response = self.CRUDUser.delete(email_id=email)
            return response
        except Exception as error:
            logging.error(f"Error in delete_user_controller function: {error}")
            raise {"error": "Invalid username or password"}
