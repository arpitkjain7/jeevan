from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.controllers.listOfData_controller import ListOfComplaintsController
from core.controllers.listOfData_controller import ListOfDiagnosisController
from core.controllers.listOfData_controller import ListOfMedicalTestsController
from core.controllers.listOfData_controller import ListOfMedicinesController
from core.controllers.listOfData_controller import ListOfPrecautionsController, Common
from commons.auth import decodeJWT
from fastapi.security import OAuth2PasswordRequestForm
from core import logger

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
listOfData_router = APIRouter()
common_router = APIRouter()

"""listOfComplaint_router = APIRouter()
listOfDiagnosis_router = APIRouter()
listOfMedicalTests_router = APIRouter()
listOfMedicines_router = APIRouter()
"""


@listOfData_router.post("/v1/listOfComplaints/create")
def add_complaint(complaint: str, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfComplaints/create")
        logging.debug(f"Request: {complaint}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfComplaintsController().add_complaint_controller(complaint)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/listOfComplaints/create endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfComplaints/create endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.get("/v1/listOfComplaints/getAll")
def get_all_complaint(token: str = Depends(oauth2_scheme)):
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/listOfComplaints/getAll endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfComplaintsController().get_all_complaints_controller()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/listOfComplaints/getAll endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfComplaints/getAll endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.post("/v1/listOfComplaints/delete")
def delete_complaint(complaint_id: int, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfComplaints/delete")
        logging.debug(f"Request: {complaint_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfComplaintsController().delete_complaint_controller(
                complaint_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/listOfComplaints/delete endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfComplaints/delete endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.post("/v1/listOfDiagnosis/addDisease")
def add_disease(disease: str, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfComplaints/create")
        logging.debug(f"Request: {disease}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfDiagnosisController().add_disease_controller(disease)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/listOfDiagnosis/create endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfDiagnosis/create endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.get("/v1/listOfDiagnosis/getAllDiseases")
def get_all_diseases(token: str = Depends(oauth2_scheme)):
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/listOfDiagnosis/getAllDiseases endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfDiagnosisController().get_all_diseases_controller()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfDiagnosis/getAllDiseases endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfDiagnosis/getAllDiseases endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.post("/v1/listOfDiagnosis/deleteDisease")
def delete_disease(disease_id: int, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfDiagnosis/deleteDisease")
        logging.debug(f"Request: {disease_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfDiagnosisController().delete_disease_controller(disease_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfDiagnosis/deleteDisease endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfDiagnosis/deleteDisease endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.post("/v1/listOfMedicalTests/addMedicalTest")
def add_medical_test(medicalTest: str, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfMedicalTests/addMedicalTest")
        logging.debug(f"Request: {medicalTest}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicalTestsController().add_medicalTest_controller(
                medicalTest
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfMedicalTests/addMedicalTest endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/listOfMedicalTests/addMedicalTest endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.get("/v1/listOfMedicalTest/getAllTests")
def get_all_medical_tests(token: str = Depends(oauth2_scheme)):
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/listOfMedicalTest/getAllTests endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicalTestsController().get_all_tests_controller()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfMedicalTest/getAllTests endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfMedicalTest/getAllTests endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.post("/v1/listOfMedicalTest/deleteTest")
def delete_medical_test(test_id: int, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfMedicalTest/deleteTest")
        logging.debug(f"Request: {test_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicalTestsController().delete_test_controller(test_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfMedicalTest/deleteTest endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfMedicalTest/deleteTest endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.post("/v1/listOfMedicines/addMedicine")
def add_medicine(name: str, company: str, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfMedicine/addMedicine")
        logging.debug(f"Request: {name}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicinesController().add_medicine_controller(
                name,
                company,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/listOfMedicines/addMedicine endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfMedicines/addMedicine endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.get("/v1/listOfMedicines/getAllMedicines")
def get_all_medicines(token: str = Depends(oauth2_scheme)):
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/listOfMedicines/getAllMedicines endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicinesController().get_all_medicines_controller()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfMedicines/getAllMedicines endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfMedicines/getAllMedicines endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.post("/v1/listOfMedicines/deleteMedicine")
def delete_medicine(medicine_id: int, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfMedicines/deleteMedicine")
        logging.debug(f"Request: {medicine_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicinesController().delete_medicine_controller(medicine_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfMedicines/deleteMedicine endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfMedicines/deleteMedicine endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.post("/v1/listOfPrecautions/addInstruction")
def add_instruction(instruction: str, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfPrecautions/addInstruction")
        logging.debug(f"Request: {instruction}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfPrecautionsController().add_instruction_controller(instruction)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfPrecautions/addInstruction endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/listOfPrecautions/addInstruction endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfData_router.get("/v1/listOfPrecautions/getAllInstructions")
def get_all_instructions(token: str = Depends(oauth2_scheme)):
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/listOfPrecautions/getAllInstructions endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfPrecautionsController().get_all_instructions_controller()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfPrecautions/getAllInstructions endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/listOfPrecautions/getAllInstructions endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


# Changes made till here, need to update below function .


@listOfData_router.post("/v1/listOfPrecautions/deleteInstruction")
def delete_instruction(instruction_id: int, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfPrecautions/deleteInstruction")
        logging.debug(f"Request: {instruction_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfPrecautionsController().delete_instruction_controller(
                instruction_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfPrecautions/deleteInstruction endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/listOfPrecautions/deleteInstruction endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.get("/v1/checkAbhaAvailability")
def check_available_health_id(health_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/checkAbhaAvailability endpoint")
        logging.debug(f"Request: {health_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().abha_availability(health_id=health_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/checkAbhaAvailability endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/aadhaar/abhaRegistration endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


# below API is not showing in API lists


@common_router.post("/v1/deepLinkNotify")
def deep_link_notify(mobile_no: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/deepLinkNotify endpoint")
        logging.debug(f"Request: {mobile_no=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().deep_link_notify(mobile_no=mobile_no)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/deepLinkNotify endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/deepLinkNotify endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
