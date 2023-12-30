from core.crud.hims_users_crud import CRUDUser
from commons.auth import encrypt_password, verify_hash_password, signJWT
from fastapi import HTTPException, status
from core.utils.custom.msg91_helper import otpHelper
from core import logger
import random

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
            user_obj = self.CRUDUser.read_by_username(
                username=request_json.get("mobile_number")
            )
            if user_obj:
                return {
                    "access_token": None,
                    "token_type": "bearer",
                    "user_role": request_json.get("user_role"),
                    "status": f"User already exists with provided mobile number",
                }
            else:
                request_json.update(
                    {
                        "password": password_hash,
                        "username": request_json.get("mobile_number"),
                    }
                )
                self.CRUDUser.create(**request_json)
                access_token = signJWT(
                    username=request_json.get("mobile_number"),
                    user_role="dummy",
                    department="dummy",
                    hip_id={"dummy": "dummy"},
                )
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user_role": "dummy",
                    "status": "New user created successfully",
                }
        except Exception as error:
            logging.error(f"Error in register_user_controller function: {error}")
            raise error

    def onboard_user_controller(self, request):
        try:
            logging.info("executing onboard_user_controller function")
            request_json = request.dict()
            user_obj = self.CRUDUser.read_by_username(
                username=request_json.get("mobile_number")
            )
            hip_details = user_obj.get("hip_details", {})
            hip_details = {} if hip_details is None else hip_details
            if user_obj is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=str(error),
                    headers={"WWW-Authenticate": "Bearer"},
                )
            inp_hip_id = request_json.pop("hip_id")
            inp_hip_name = request_json.pop("hip_name")
            hip_details.update({inp_hip_id: inp_hip_name})
            request_json.update(
                {
                    "hip_details": hip_details,
                    "username": request_json.get("mobile_number"),
                }
            )
            self.CRUDUser.update(**request_json)
            access_token = signJWT(
                username=request_json.get("mobile_number"),
                user_role=request_json.get("user_role"),
                department=request_json.get("department"),
                hip_id=hip_details,
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_role": request_json.get("user_role"),
                "status": "New user created successfully",
            }
        except Exception as error:
            logging.error(f"Error in onboard_user_controller function: {error}")
            raise error

    def generate_otp_controller(self, request):
        try:
            logging.info("executing generate_otp_controller function")
            user_obj = self.CRUDUser.read_by_username(username=request.mobile_number)
            if user_obj:
                # TODO: call send OTP function
                otp = random.randint(1000, 9999)
                otp_response = otpHelper().send_otp(
                    mobile_number=user_obj.get("mobile_number"), otp=otp
                )
                self.CRUDUser.update(
                    **{"username": request.mobile_number, "otp": str(otp)}
                )
                return {
                    "status": "success",
                    "details": "OTP generate and sent successfully",
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception as error:
            logging.error(f"Error in generate_otp_controller function: {error}")
            raise error

    def reset_password_controller(self, request):
        try:
            logging.info("executing reset_password_controller function")
            user_obj = self.CRUDUser.read_by_username(username=request.mobile_number)
            if user_obj:
                if request.old_password:
                    if verify_hash_password(
                        plain_password=request.old_password,
                        hashed_password=user_obj.get("password"),
                    ):
                        password_hash = encrypt_password(password=request.new_password)
                        self.CRUDUser.update(
                            **{
                                "username": request.mobile_number,
                                "password": password_hash,
                            }
                        )
                        return {
                            "status": "success",
                            "details": "Password updated successfully",
                        }
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Provided password does not match",
                            headers={"WWW-Authenticate": "Bearer"},
                        )
                if request.otp:
                    if request.otp == user_obj.get("otp"):
                        password_hash = encrypt_password(password=request.new_password)
                        self.CRUDUser.update(
                            **{
                                "username": request.mobile_number,
                                "password": password_hash,
                            }
                        )
                        return {
                            "status": "success",
                            "details": "Password updated successfully",
                        }
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="OTP does not match",
                            headers={"WWW-Authenticate": "Bearer"},
                        )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception as error:
            logging.error(f"Error in reset_password_controller function: {error}")
            raise error

    def verify_otp_controller(self, request):
        try:
            logging.info("executing reset_password_controller function")
            user_obj = self.CRUDUser.read_by_username(username=request.mobile_number)
            if user_obj:
                if request.otp == user_obj.get("otp"):
                    self.CRUDUser.update(
                        **{
                            "username": request.mobile_number,
                            "verified": True,
                        }
                    )
                    return {
                        "status": "success",
                        "details": "OTP verified successfully",
                    }
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="OTP does not match",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception as error:
            logging.error(f"Error in reset_password_controller function: {error}")
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
            user_obj = self.CRUDUser.read_by_username(username=request.username)
            if user_obj:
                if verify_hash_password(
                    plain_password=request.password,
                    hashed_password=user_obj.get("password"),
                ):
                    access_token = signJWT(
                        username=request.username,
                        user_role=user_obj.get("user_role"),
                        department=user_obj.get("department"),
                        hip_id=user_obj.get("hip_details"),
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
            user_obj = self.CRUDUser.read_by_username(username=username)
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
