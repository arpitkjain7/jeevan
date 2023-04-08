from core.crud.hims_users_crud import CRUDUser
from core.crud.hims_docDetails_crud import CRUDDocDetails
from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hims_appointments_crud import CRUDAppointments
from core.apis.schemas.requests.user_request import Register
from core.controllers.users_controller import UserManagementController

from core import logger

logging = logger(__name__)


def create_admin_user(admin_user_request):
    existing_admin_user = CRUDUser().read(username=admin_user_request.username)
    if not existing_admin_user:
        _ = UserManagementController().register_user_controller(
            request=admin_user_request
        )


def create_sample_doc_record(doc_request):
    existing_doc_record = CRUDDocDetails().read_by_docId(doc_id=1)
    if not existing_doc_record:
        CRUDDocDetails().create(**doc_request)


def create_sample_patient_record(patient_request):
    existing_patient_record = CRUDPatientDetails().read_by_patientId(patient_id=1)
    if not existing_patient_record:
        CRUDPatientDetails().create(**patient_request)


def create_sample_appointment(appointment_request):
    existing_appointment_record = CRUDAppointments().read_by_patientId(patient_id=1)
    if not existing_appointment_record:
        CRUDAppointments().create(**appointment_request)


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
            "doc_name": "DUMMY",
            "doc_specialization": "DUMMY",
            "doc_department": "DUMMY",
            "doc_working_days": "Mon,Tue,Wed",
            "doc_reg_id": "12312",
        }
    )
    create_sample_patient_record(
        patient_request={
            "abha_number": "91126527173630",
            "abha_address": "arpitjain@sbx",
            "mobile_number": "8552012549",
            "name": "DUMMY",
            "gender": "Male",
            "DOB": "10/12/1992",
        }
    )
    create_sample_appointment(
        appointment_request={
            "appointment_date": "2023-09-08",
            "appointment_time": "12:00",
            "doc_id": 1,
            "patient_id": 1,
        }
    )
