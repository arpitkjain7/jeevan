from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.user_request import Register, RoleAssignment
from core.apis.schemas.responses.user_response import (
    RegisterResponse,
    LoginResponse,
    UserResponse,
)
from core.controllers.users_controller import UserManagementController
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
        # if user_obj.get("access_token") is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST, detail=user_obj["status"]
        #     )
        # else:
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


@user_router.post("/v1/user/roleAssignment")
def role_assignment(role_assignment_request: RoleAssignment):
    try:
        logging.info("Calling /v1/user/roleAssignment endpoint")
        logging.debug(f"Request: {role_assignment_request}")

        return UserManagementController().assign_user_role_controller(
            request=role_assignment_request
        )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/user/roleAssignment endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/user/roleAssignment endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_router.post("/v1/user/signIn", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
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
        valid_user = UserManagementController().login_user_controller(form_data)
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
            return UserManagementController().get_all_users_controller()
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


@user_router.get("/v1/user/details", response_model=UserResponse)
async def get_user_details(username: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/user/details endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_details = UserManagementController().get_user_controller(
                username=username
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
