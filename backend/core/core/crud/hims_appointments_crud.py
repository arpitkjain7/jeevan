from core import session, logger
from core.orm_models.hims_appointments import Appointments
from core.orm_models.hims_slots import Slots
from core.orm_models.hims_docDetails import DocDetails
from core.orm_models.hims_patientDetails import PatientDetails
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDAppointments:
    def create(self, **kwargs):
        """[CRUD function to create a new Appointment record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDAppointments create request")
            kwargs.update(
                {
                    "created_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    ),
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    ),
                }
            )
            appointment = Appointments(**kwargs)
            with session() as transaction_session:
                transaction_session.add(appointment)
                transaction_session.commit()
                transaction_session.refresh(appointment)
            return appointment.id
        except Exception as error:
            logging.error(f"Error in CRUDAppointments create function : {error}")
            raise error

    def read_by_docId(self, doc_id: str, hip_id: str):
        """[CRUD function to read a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDAppointments read request")
            with session() as transaction_session:
                joined_result = []
                for appointment_obj, slot_obj, patient_obj in (
                    transaction_session.query(Appointments, Slots, PatientDetails)
                    .filter(Appointments.doc_id == doc_id)
                    .filter(Appointments.hip_id == hip_id)
                    .filter(Slots.slot_id == Appointments.slot_id)
                    .filter(PatientDetails.id == Appointments.patient_id)
                    .all()
                ):
                    start_time = slot_obj.start_time.strftime("%H:%M")
                    end_time = slot_obj.end_time.strftime("%H:%M")
                    appointment_obj.__dict__.update(
                        {
                            "patient_name": patient_obj.name,
                            "slot_time": str(f"{start_time}" + " - " + f"{end_time}"),
                        }
                    )
                    appointment_obj.__dict__.update({"slot_details": slot_obj.__dict__})
                    joined_result.append([appointment_obj])
                return joined_result
            #     obj: Appointments = (
            #         transaction_session.query(Appointments)
            #         .filter(Appointments.doc_id == doc_id)
            #         .filter(Appointments.hip_id == hip_id)
            #         .all()
            #     )
            # if obj is not None:
            #     return [row.__dict__ for row in obj]
            # return []
        except Exception as error:
            logging.error(f"Error in CRUDAppointments read function : {error}")
            raise error

    def read_by_patientId(self, patient_id: str, hip_id: str):
        """[CRUD function to read a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDAppointments read request")
            with session() as transaction_session:
                obj: Appointments = (
                    transaction_session.query(Appointments)
                    .filter(Appointments.patient_id == patient_id)
                    .filter(Appointments.hip_id == hip_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDAppointments read function : {error}")
            raise error

    def read_all(self, hip_id: str):
        """[CRUD function to read_all Users record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all user records]
        """
        try:
            logging.info("CRUDAppointments read_all request")
            with session() as transaction_session:
                joined_result = []
                for appointment_obj, doctor_obj, patient_obj, slot_obj in (
                    transaction_session.query(
                        Appointments, DocDetails, PatientDetails, Slots
                    )
                    .filter(Appointments.hip_id == hip_id)
                    .filter(DocDetails.id == Appointments.doc_id)
                    .filter(PatientDetails.id == Appointments.patient_id)
                    .filter(Slots.slot_id == Appointments.slot_id)
                    .all()
                ):
                    start_time = slot_obj.start_time.strftime("%H:%M")
                    end_time = slot_obj.end_time.strftime("%H:%M")
                    appointment_obj.__dict__.update(
                        {
                            "slot_time": str(f"{start_time}" + " - " + f"{end_time}"),
                            "patient_details": patient_obj,
                            "doc_details": doctor_obj,
                            "slot_details": slot_obj,
                        },
                    )
                    # appointment_obj.__dict__.update(
                    #     {"doc_details": doctor_obj},
                    # )
                    joined_result.append(appointment_obj)
            if joined_result is not None:
                return joined_result
            return []
        except Exception as error:
            logging.error(f"Error in CRUDAppointments read_all function : {error}")
            raise error

    def update(self, id, **kwargs):
        """[CRUD function to update a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDAppointments update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: Appointments = (
                    transaction_session.query(Appointments)
                    .filter(Appointments.id == id)
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDAppointments update function : {error}")
            raise error

    def delete(self, appointment_id: int):
        """[CRUD function to delete a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDAppointments delete function")
            with session() as transaction_session:
                obj: Appointments = (
                    transaction_session.query(Appointments)
                    .filter(Appointments.id == appointment_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDAppointments delete function : {error}")
            raise error
