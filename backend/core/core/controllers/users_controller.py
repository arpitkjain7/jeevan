from core.crud.hims_users_crud import CRUDUser
from core.crud.hims_userRole_crud import CRUDUserRoles
from commons.auth import encrypt_password, verify_hash_password, signJWT
from core import logger

logging = logger(__name__)


class UserManagementController:
    def __init__(self):
        self.CRUDUser = CRUDUser()
        self.CRUDUserRoles = CRUDUserRoles()

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
            user_obj = self.CRUDUser.read_joined(username=request_json.get("username"))
            logging.debug(f"{user_obj=}")
            inp_hip_id = request_json.pop("hip_id")
            inp_hip_name = request_json.pop("hip_name")
            if len(user_obj) > 0:
                hip_details = user_obj.get("hip_details")
                hip_list = list(hip_details.keys())
                access_token = signJWT(
                    email=user_obj.get("username"),
                    user_roles=user_obj.get("user_roles"),
                    department=user_obj.get("department"),
                    hip_id=hip_details,
                )
                if inp_hip_id in hip_list:
                    return {
                        "user_id": user_obj.get("id"),
                        "access_token": access_token,
                        "token_type": "bearer",
                        "user_roles": user_obj.get("user_roles"),
                        "status": "User already exists",
                    }
                else:
                    hip_details.update({inp_hip_id: inp_hip_name})
                    request_json.update(
                        {"password": password_hash, "hip_details": hip_details}
                    )
                    self.CRUDUser.update(**request_json)
                    return {
                        "user_id": user_obj.get("id"),
                        "access_token": access_token,
                        "token_type": "bearer",
                        "user_roles": user_obj.get("user_roles"),
                        "status": "User onboarded successfully",
                    }
            else:
                request_json.update(
                    {
                        "password": password_hash,
                        "hip_details": {inp_hip_id: inp_hip_name},
                    }
                )
                user_id = self.CRUDUser.create(**request_json)
                user_role_request = {"user_id": user_id, "user_role": "STAFF"}
                self.CRUDUserRoles.create(**user_role_request)
                access_token = signJWT(
                    email=request_json.get("username"),
                    user_roles=["STAFF"],
                    department=request_json.get("department"),
                    hip_id={inp_hip_id: inp_hip_name},
                )
                return {
                    "user_id": user_id,
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user_roles": ["STAFF"],
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
            user_obj = self.CRUDUser.read_joined(username=request.username)
            logging.info(f"{user_obj=}")
            if len(user_obj) > 0:
                if verify_hash_password(
                    plain_password=request.password,
                    hashed_password=user_obj.get("password"),
                ):
                    access_token = signJWT(
                        email=request.username,
                        user_roles=user_obj.get("user_roles"),
                        department=user_obj.get("department"),
                        hip_id=user_obj.get("hip_details"),
                    )
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
            logging.info(f"{user_list=}")
            user_list_new = []
            for user_obj in user_list:
                logging.info(f"{user_obj=}")
                user_obj.pop("password")
                user_list_new.append(user_obj)
            return user_list_new
        except Exception as error:
            logging.error(f"Error in get_all_users_controller function: {error}")
            raise error

    def get_user_controller(self, username: str):
        """[Get User Details]

        Args:
            username (str): [Username of the user]

        Returns:
            [dict]: [User details]
        """
        try:
            logging.info("executing get_user_controller function")
            user_obj = self.CRUDUser.read_joined(username=username)
            if len(user_obj) > 0:
                del user_obj["password"]
                return user_obj
            raise Exception("Invalid username")
        except Exception as error:
            logging.error(f"Error in get_user_controller function: {error}")
            raise error

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

    def assign_user_role_controller(self, request):
        try:
            logging.info("executing assign_user_role_controller function")
            request_json = request.dict()
            user_obj = self.CRUDUser.read_joined(username=request_json.get("username"))
            print(f"{user_obj=}")
            if len(user_obj) > 0:
                user_roles = user_obj.get("user_roles")
                role_delta_list = list(set(request_json.get("role")) - set(user_roles))
                print(f"{role_delta_list=}")
                for user_role in role_delta_list:
                    crud_request = {
                        "user_id": user_obj.get("id"),
                        "user_role": user_role,
                    }
                    self.CRUDUserRoles.create(**crud_request)
                    user_roles.append(user_role)
                return {
                    "user_id": user_obj["id"],
                    "username": user_obj["username"],
                    "user_roles": user_roles,
                }
            raise Exception("User not found")
        except Exception as error:
            logging.error(f"Error in assign_user_role_controller function: {error}")
            raise error
