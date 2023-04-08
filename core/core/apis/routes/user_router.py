from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.user_request import Register, SSO, Login
from core.apis.schemas.responses.user_response import (
    RegisterResponse,
    LoginResponse,
    UserDetails,
)
from core.controllers.user_management_controller import UserManagementController
from commons.auth import decodeJWT
from fastapi.security import OAuth2PasswordRequestForm
from core import logger

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
user_router = APIRouter()


@user_router.post("/v1/user/signUp", response_model=RegisterResponse)
def register_user(register_user_request: Register):
    """[API router to register new user into the system]
    Args:
        register_user_request (Register): [New user details]
    Raises:
        HTTPException: [Unauthorized exception when invalid token is passed]
        error: [Exception in underlying controller]
    Returns:
        [RegisterResponse]: [Register new user response]
    """
    try:
        logging.info("Calling /v1/user/signUp endpoint")
        logging.debug(f"Request: {register_user_request}")

        user_obj = UserManagementController().register_user_controller(
            register_user_request
        )
        if user_obj.get("access_token") is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=user_obj["status"]
            )
        else:
            return RegisterResponse(**user_obj)
    except HTTPException as httperror:
        logging.error(f"Error in /v1/user/signUp endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/user/signUp endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_router.post("/v1/user/signUp/{event_uuid}", response_model=RegisterResponse)
def register_guest_user(event_uuid: str, register_user_request: Register):
    """[API router to register new user into the system]
    Args:
        register_user_request (Register): [New user details]
    Raises:
        HTTPException: [Unauthorized exception when invalid token is passed]
        error: [Exception in underlying controller]
    Returns:
        [RegisterResponse]: [Register new user response]
    """
    try:
        logging.info(f"Calling /v1/user/signUp/{event_uuid} endpoint")
        # logging.debug(f"Request: {register_user_request}")

        user_obj = UserManagementController().register_guest_user_controller(
            event_uuid=event_uuid,
            email_id=register_user_request.email_id,
            password=register_user_request.password,
            name=register_user_request.name,
            phone_number=register_user_request.phone_number,
        )
        if user_obj.get("access_token") is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=user_obj["status"]
            )
        else:
            return RegisterResponse(**user_obj)
    except HTTPException as httperror:
        logging.error(f"Error in /v1/user/signUp/{event_uuid} endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/user/signUp/{event_uuid} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_router.post("/v1/user/signIn", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), event_uuid: str = None
):
    """[API router to login existing user]
    Args:
        form_data (OAuth2PasswordRequestForm, optional): [User details to login the user]. Defaults to Depends().
    Raises:
        error: [Exception in underlying controller]
    Returns:
        [LoginResponse]: [Login response]
    """
    try:
        logging.info("Calling /v1/user/signIn endpoint")
        valid_user = UserManagementController().login_user_controller(
            form_data, event_uuid=event_uuid
        )
        if not valid_user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
        return LoginResponse(**valid_user)
    except HTTPException as httperror:
        logging.error(f"Error in /v1/user/signIn endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/user/signIn endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_router.get("/v1/user/upgrade")
async def upgrade_to_premium(token: str = Depends(oauth2_scheme)):
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/user/upgrade endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            return UserManagementController().upgrade_user_to_premium(user_id=user_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/user/upgrade endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/user/upgrade endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


# @user_router.post("/user/{event_id}/sso")
# async def ssoGuestLogin(email_id: str, name: str, event_id: str):
#     """[API router to login existing user]
#     Args:
#         form_data (OAuth2PasswordRequestForm, optional): [User details to login the user]. Defaults to Depends().
#     Raises:
#         error: [Exception in underlying controller]
#     Returns:
#         [LoginResponse]: [Login response]
#     """
#     try:
#         logging.info(f"Calling /user/{event_id}/sso endpoint")
#         valid_user = UserManagementController().sso_guest_controller(
#             email_id=email_id, name=name, event_id=event_id
#         )
#         if not valid_user:
#             raise HTTPException(
#                 status_code=400, detail="Incorrect username or password"
#             )
#         return valid_user
#     except Exception as error:
#         logging.error(f"Error in /user/{event_id}/sso endpoint: {error}")
#         raise HTTPException(status_code=400, detail="Incorrect username or password")


# @user_router.post("/user/sso")
# async def ssoLogin(sso_data: SSO):
#     """[API router to login existing user]
#     Args:
#         form_data (OAuth2PasswordRequestForm, optional): [User details to login the user]. Defaults to Depends().
#     Raises:
#         error: [Exception in underlying controller]
#     Returns:
#         [LoginResponse]: [Login response]
#     """
#     try:
#         logging.info("Calling /user/sso endpoint")
#         valid_user = UserManagementController().sso_controller(sso_data)
#         if not valid_user:
#             raise HTTPException(
#                 status_code=400, detail="Incorrect username or password"
#             )
#         return valid_user
#     except Exception as error:
#         logging.error(f"Error in /user/sso endpoint: {error}")
#         raise HTTPException(status_code=400, detail="Incorrect username or password")


# @user_router.delete("/user/delete")
# async def delete_user(
#     email: str,
#     token: str = Depends(oauth2_scheme),
# ):
#     """[API router to delete user]
#     Args:
#         user_name (str): [Delete user with provided user_name]
#     Raises:
#         error: [Exception in underlying controller]
#     Returns:
#         [dict]: [Deleted user details]
#     """
#     try:
#         logging.info("Calling /user/delete endpoint")
#         authenticated_user_details = decodeJWT(token=token)
#         if authenticated_user_details:
#             return UserManagementController().delete_user_controller(email=email)
#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid access token",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#     except Exception as error:
#         logging.error(f"Error in /user/update/role endpoint: {error}")
#         raise error


@user_router.get("/v1/user/list")
async def get_all_users(token: str = Depends(oauth2_scheme)):
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/user/list endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            list_of_users = UserManagementController().get_all_users_controller()
            return list_of_users
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/user/list endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/user/list endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_router.get("/v1/user/details")
async def get_user_details(email_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/user/details endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_details = UserManagementController().get_user_controller(
                email_id=email_id
            )
            return user_details
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/user/details endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/user/details endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
