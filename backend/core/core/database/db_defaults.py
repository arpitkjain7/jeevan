from core.crud.hims_users_crud import CRUDUser
from core.crud.hims_docDetails_crud import CRUDDocDetails
from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hims_appointments_crud import CRUDAppointments
from core.crud.hims_hip_crud import CRUDHIP
from core.apis.schemas.requests.user_request import Register
from core.controllers.users_controller import UserManagementController
import uuid
from core import logger

logging = logger(__name__)
patient_id = "111-111-111-111"


def create_admin_user(admin_user_request):
    existing_admin_user = CRUDUser().read(username=admin_user_request.username)
    if not existing_admin_user:
        _ = UserManagementController().register_user_controller(
            request=admin_user_request
        )


def create_sample_doc_record(doc_request):
    existing_doc_record = CRUDDocDetails().read_by_docId(doc_id=2)
    if not existing_doc_record:
        CRUDDocDetails().create(**doc_request)


def create_sample_patient_record(patient_request):
    existing_patient_record = CRUDPatientDetails().read_by_patientId(
        patient_id=patient_id
    )
    if not existing_patient_record:
        CRUDPatientDetails().create(**patient_request)


def create_sample_appointment(appointment_request):
    existing_appointment_record = CRUDAppointments().read_by_patientId(
        patient_id=patient_id, hip_id="123123"
    )
    if not existing_appointment_record:
        CRUDAppointments().create(**appointment_request)


def create_sample_hip(hip_request):
    existing_hip_record = CRUDHIP().read(hip_ip=hip_request["hip_id"])
    if not existing_hip_record:
        CRUDHIP().create(**hip_request)


def main():
    admin_user_request = Register(
        username="admin@lobster.com",
        name="admin",
        hip_name="Jeevan Healthcare",
        hip_id="123123",
        password="P@ssw0rd",
        user_role="ADMIN",
        department="IT",
    )
    create_admin_user(admin_user_request=admin_user_request)
    create_sample_doc_record(
        doc_request={
            "doc_name": "Dr Arpit Jain",
            "hip_id": "123123",
            "doc_specialization": "DUMMY",
            "doc_department": "DUMMY",
            "doc_working_days": "Mon,Tue,Wed",
            "doc_licence_no": "12312",
            "avg_consultation_time": "15",
        }
    )
    create_sample_patient_record(
        patient_request={
            "id": patient_id,
            "abha_number": "DUMMY",
            "abha_address": "DUMMY@sbx",
            "mobile_number": "1111111111",
            "name": "DUMMY",
            "gender": "Male",
            "DOB": "10/12/1992",
        }
    )
    # create_sample_appointment(
    #     appointment_request={
    #         "appointment_time": "12:00",
    #         "doc_id": 1,
    #         "patient_id": patient_id,
    #     }
    # )
    create_sample_hip(
        hip_request={
            "hip_id": "123123",
            "name": "ABC Healthcare",
            "hip_uid": "ABC",
            "hip_address": "DUMMY",
        }
    )
