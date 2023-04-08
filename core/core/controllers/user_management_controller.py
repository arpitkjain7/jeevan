from core.crud.users_crud import CRUDUser
from core.crud.attendees_crud import CRUDAttendees
from core.crud.events_crud import CRUDEvents
from commons.auth import encrypt_password, verify_hash_password, signJWT
from core import logger

logging = logger(__name__)


class UserManagementController:
    def __init__(self):
        self.CRUDUser = CRUDUser()
        self.CRUDAttendees = CRUDAttendees()
        self.CRUDEvents = CRUDEvents()

    def register_guest_user_controller(
        self, event_uuid, email_id, password, name, phone_number
    ):
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
            password_hash = encrypt_password(password=password)
            user_obj = self.CRUDUser.read(email_id=email_id)
            event_obj = self.CRUDEvents.read_by_uuid(event_uuid=event_uuid)
            if event_obj is None:
                raise Exception("Invalid Event Id")
            # if user_obj is not None:

            #     attendee_obj = self.CRUDAttendees.read(
            #         user_id=email_id, event_id=event_obj["id"]
            #     )
            #     if attendee_obj is None:
            #         attendee_request = {
            #             "user_id": email_id,
            #             "event_id": event_obj["id"],
            #             "status": "INACTIVE",
            #         }
            #         self.CRUDAttendees.create(**attendee_request)
            #     access_token = signJWT(
            #         email=email_id, user_role=user_obj.get("user_role")
            #     )
            #     return {"access_token": access_token, "token_type": "bearer"}
            if user_obj is not None:
                return {"access_token": None, "status": "User already exists"}
            else:
                user_request = {
                    "password": password_hash,
                    "name": name,
                    "email_id": email_id,
                    "phone_number": phone_number,
                    "user_role": "GUEST",
                }
                self.CRUDUser.create(**user_request)
                attendee_request = {
                    "user_id": email_id,
                    "event_id": event_obj["id"],
                    "status": "INACTIVE",
                }
                self.CRUDAttendees.create(**attendee_request)
                access_token = signJWT(email=email_id, user_role="GUEST")
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user_role": "GUEST",
                }
        except Exception as error:
            logging.error(f"Error in register_user_controller function: {error}")
            raise error

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
            password_hash = encrypt_password(password=request.password)
            user_obj = self.CRUDUser.read(email_id=request.email_id)
            if user_obj is not None:
                return {"access_token": None, "status": "User already exists"}
            else:
                user_request = {
                    "password": password_hash,
                    "name": request.name,
                    "email_id": request.email_id,
                    "phone_number": request.phone_number,
                    "user_role": "NEWUSER",
                }
                self.CRUDUser.create(**user_request)
                access_token = signJWT(email=request.email_id, user_role="NEWUSER")
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user_role": "NEWUSER",
                }
        except Exception as error:
            logging.error(f"Error in register_user_controller function: {error}")
            raise error

    def login_user_controller(self, request, event_uuid):
        """[Controller for user login]

        Args:
            request ([dict]): [user login details]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        # try:
        logging.info("executing login user function")
        user_obj = self.CRUDUser.read(email_id=request.username)
        if user_obj:
            if verify_hash_password(
                plain_password=request.password,
                hashed_password=user_obj.get("password"),
            ):
                access_token = signJWT(
                    email=request.username, user_role=user_obj.get("user_role")
                )
                if event_uuid:
                    event_obj = self.CRUDEvents.read_by_uuid(event_uuid=event_uuid)
                    if event_obj is None:
                        raise Exception("Invalid Event Id")
                    attendee_obj = self.CRUDAttendees.read(
                        user_id=request.username, event_id=event_obj["id"]
                    )
                    if attendee_obj is None:
                        attendee_request = {
                            "user_id": request.username,
                            "event_id": event_obj["id"],
                            "status": "INACTIVE",
                        }
                        self.CRUDAttendees.create(**attendee_request)
                return {
                    "email": user_obj.get("email_id"),
                    "name": user_obj.get("name"),
                    "user_id": user_obj.get("id"),
                    "user_role": user_obj.get("user_role"),
                    "access_token": access_token,
                    "token_type": "bearer",
                }
            else:
                return None
        else:
            return None
        # except Exception as error:
        #     logging.error(f"Error in login_user_controller function: {error}")
        #     raise error

    def sso_guest_controller(self, email_id, name, event_id):
        """[Controller for user login]

        Args:
            request ([dict]): [user login details]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing sso controller function")
            user_obj = self.CRUDUser.read(email_id=email_id)
            if user_obj:
                attendee_request = {
                    "user_id": email_id,
                    "event_id": event_id,
                    "status": "INACTIVE",
                }
                self.CRUDAttendees.create(**attendee_request)
                access_token = signJWT(
                    email=email_id, user_role=user_obj.get("user_role")
                )
                return {
                    "email": user_obj.get("email_id"),
                    "name": user_obj.get("name"),
                    "user_id": user_obj.get("id"),
                    "access_token": access_token,
                    "token_type": "bearer",
                }
            else:
                user_request = {"name": name, "email_id": email_id}
                self.CRUDUser.create(**user_request)
                attendee_request = {
                    "user_id": email_id,
                    "event_id": event_id,
                    "status": "INACTIVE",
                }
                self.CRUDAttendees.create(**attendee_request)
                access_token = signJWT(email=email_id, user_role="NEWUSER")
                return {"access_token": access_token, "token_type": "bearer"}
        except Exception as error:
            logging.error(f"Error in sso_controller function: {error}")
            raise error

    def sso_controller(self, request):
        """[Controller for user login]

        Args:
            request ([dict]): [user login details]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing sso controller function")
            user_obj = self.CRUDUser.read(email_id=request.email_id)
            if user_obj:
                access_token = signJWT(
                    email=request.email_id, user_role=user_obj.get("user_role")
                )
                return {
                    "email": user_obj.get("email_id"),
                    "name": user_obj.get("name"),
                    "user_id": user_obj.get("id"),
                    "access_token": access_token,
                    "token_type": "bearer",
                }
            else:
                user_request = {"name": request.name, "email_id": request.email_id}
                self.CRUDUser.create(**user_request)
                access_token = signJWT(email=request.email_id, user_role="NEWUSER")
                return {"access_token": access_token, "token_type": "bearer"}
        except Exception as error:
            logging.error(f"Error in sso_controller function: {error}")
            raise error

    # def forgot_password_controller(self, request):
    #     try:
    #         logging.info("executing forgot password function")
    #         user_obj = self.CRUDUser.read(email_id=request.email_id)
    #         password_hash = encrypt_password(password=request.new_password)
    #         if user_obj:
    #             update_request = {
    #                 "user_name": request.email_id,
    #                 "password": password_hash,
    #             }
    #             self.CRUDUser.update(**update_request)
    #             return {"status": "Password Updated"}
    #         else:
    #             return {"status": "User doesn't exist"}
    #     except Exception as error:
    #         logging.error(f"Error in forgot_password_controller function: {error}")
    #         raise error

    # def update_password_controller(self, request):
    #     try:
    #         logging.info("executing update password function")
    #         user_obj = self.CRUDUser.read(email_id=request.email_id)
    #         password_hash = encrypt_password(password=request.new_password)
    #         if user_obj:
    #             if verify_hash_password(
    #                 plain_password=request.old_password,
    #                 hashed_password=user_obj.get("password"),
    #             ):
    #                 update_request = {
    #                     "user_name": request.email_id,
    #                     "password": password_hash,
    #                 }
    #                 self.CRUDUser.update(**update_request)
    #                 return {"status": "Password Updated"}
    #             else:
    #                 return {"status": "Current password doesn't match"}
    #         else:
    #             return {"status": "Username does not exist"}
    #     except Exception as error:
    #         logging.error(f"Error in update_password_controller function: {error}")
    #         raise error

    def get_all_users_controller(self):
        """[Controller to get all users]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [list]: [list of all the users in the system]
        """
        try:
            logging.info("executing get_all_users_controller function")
            return self.CRUDUser.read_all()
        except Exception as error:
            logging.error(f"Error in get_all_users_controller function: {error}")
            raise {"error": "Invalid username or password"}

    def upgrade_user_to_premium(self, user_id: str):
        try:
            logging.info("executing upgrade_user_to_premium function")
            user_obj = self.CRUDUser.read(email_id=user_id)
            user_role = user_obj.get("user_role")
            if user_role == "HOST":
                return user_obj
            update_req = {"email_id": user_id, "user_role": "HOST"}
            self.CRUDUser.update(**update_req)
            user_obj.update({"user_role": "HOST"})
            return user_obj
        except Exception as error:
            logging.error(f"Error in upgrade_user_to_premium function: {error}")
            raise {"error": "Invalid username or password"}

    def get_user_controller(self, email_id: str):
        """[Get User Details]

        Args:
            username (str): [Username of the user]

        Returns:
            [dict]: [User details]
        """
        try:
            logging.info("executing get_all_users_controller function")
            return self.CRUDUser.read(email_id=email_id)
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
