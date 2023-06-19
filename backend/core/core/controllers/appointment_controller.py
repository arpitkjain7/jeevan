from core.crud.hims_appointments_crud import CRUDAppointments
from core.crud.hims_slots_crud import CRUDSlots
from core.crud.hims_docDetails_crud import CRUDDocDetails
from core import logger
from datetime import datetime, timezone, timedelta
import os
from dateutil import parser

logging = logger(__name__)


class AppointmentsController:
    def __init__(self):
        self.CRUDAppointments = CRUDAppointments()
        self.CRUDDocDetails = CRUDDocDetails()
        self.CRUDSlots = CRUDSlots()
        self.gateway_url = os.environ["gateway_url"]

    def create_appointment(self, request):
        try:
            logging.info("executing  create_appointment function")
            logging.info(f"{request=}")
            appointment_start = datetime.strptime(
                request.appointment_start, "%Y-%m-%d %H:%M:%S"
            )
            appointment_date = appointment_start.date()
            doc_id = request.doc_id
            patient_id = request.patient_id
            appointment_type = request.appointment_type
            if request.appointment_end is None:
                doc_obj = self.CRUDDocDetails.read_by_docId(doc_id=doc_id)
                logging.info(f"{doc_obj=}")
                avg_consultation_duration = doc_obj.get("avg_consultation_time")
                logging.info(f"{avg_consultation_duration=}")
                appointment_end = appointment_start + timedelta(
                    minutes=int(avg_consultation_duration)
                )
            else:
                appointment_end = datetime.strptime(
                    request.appointment_end, "%Y-%m-%d %H:%M:%S"
                )
            create_slots_crud_request = {
                "doc_id": doc_id,
                "patient_id": patient_id,
                "date": appointment_date,
                "start_time": appointment_start.time(),
                "end_time": appointment_end.time(),
                "status": "Scheduled",
            }
            slot_id = self.CRUDSlots.create(**create_slots_crud_request)
            create_appointment_request = {
                "hip_id": request.hip_id,
                "doc_id": doc_id,
                "appointment_type": appointment_type,
                "patient_id": patient_id,
                "slot_id": slot_id,
            }
            appointment_id = self.CRUDAppointments.create(**create_appointment_request)
            return {"appointment_id": appointment_id}
        except Exception as error:
            logging.error(
                f"Error in AppointmentsController.create_appointment function: {error}"
            )
            raise error

    def get_appointment_by_doc_id(self, doc_id, hip_id):
        try:
            logging.info("executing  get_appointment_by_doc_id function")
            logging.info(f"{doc_id=}")
            logging.info(f"{hip_id=}")
            return self.CRUDAppointments.read_by_docId(doc_id=doc_id, hip_id=hip_id)
        except Exception as error:
            logging.error(
                f"Error in AppointmentsController.get_appointment_by_doc_id function: {error}"
            )
            raise error

    def get_slots(self, doc_id, appointment_date, hip_id):
        try:
            logging.info("executing get_slots function")
            logging.info(f"{appointment_date=}")
            appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
            logging.info(f"{hip_id=}")
            return self.CRUDSlots.read_by_doc_id(
                doc_id=doc_id, appointment_date=appointment_date
            )
        except Exception as error:
            logging.error(
                f"Error in AppointmentsController.get_slots function: {error}"
            )
            raise error

    def delete_slots(self, slot_id):
        try:
            logging.info("executing delete_slots function")
            logging.info(f"{slot_id=}")
            return self.CRUDSlots.delete(slot_id=slot_id)
        except Exception as error:
            logging.error(
                f"Error in AppointmentsController.delete_slots function: {error}"
            )
            raise error

    def update_slots(self, request):
        try:
            logging.info("executing update_slots function")
            logging.info(f"{request=}")
            appointment_start = datetime.strptime(
                request.appointment_start, "%Y-%m-%d %H:%M:%S"
            )
            appointment_date = appointment_start.date()
            slot_obj = self.CRUDSlots.read(slot_id=request.slot_id)
            if request.appointment_end is None:
                doc_obj = self.CRUDDocDetails.read_by_docId(doc_id=slot_obj["doc_id"])
                avg_consultation_duration = doc_obj.get("avg_consultation_time")
                logging.info(f"{avg_consultation_duration=}")
                appointment_end = appointment_start + timedelta(
                    minutes=int(avg_consultation_duration)
                )
            else:
                appointment_end = datetime.strptime(
                    request.appointment_end, "%Y-%m-%d %H:%M:%S"
                )
            update_slots_crud_request = {
                "slot_id": request.slot_id,
                "date": appointment_date,
                "start_time": appointment_start.time(),
                "end_time": appointment_end.time(),
            }
            self.CRUDSlots.update(**update_slots_crud_request)
            return update_slots_crud_request
        except Exception as error:
            logging.error(
                f"Error in AppointmentsController.update_slots function: {error}"
            )
            raise error
