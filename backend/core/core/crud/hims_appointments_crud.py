from core import session, logger
from core.orm_models.hims_appointments import Appointments
from core.orm_models.hims_slots import Slots
from core.orm_models.hims_docDetails import DocDetails
from core.orm_models.hims_patientDetails import PatientDetails
from core.orm_models.hims_hipDetails import HIPDetail
from datetime import datetime
from pytz import timezone
from core.utils.custom.patient_helper import calculate_age
from sqlalchemy import func, case
from datetime import datetime

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

    def read(self, appointment_id: int):
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
                for appointment_obj, slot_obj in (
                    transaction_session.query(Appointments, Slots)
                    .filter(Appointments.id == appointment_id)
                    .filter(Slots.slot_id == Appointments.slot_id)
                    .all()
                ):
                    if appointment_obj is not None:
                        appointment_obj.__dict__.update(
                            {"slot_details": slot_obj.__dict__}
                        )
                        return appointment_obj.__dict__
                    return None
        except Exception as error:
            logging.error(f"Error in CRUDAppointments read function : {error}")
            raise error

    def count_all_appointments(self, hip_id: str):
        try:
            logging.info("CRUDAppointments count_all_appointments request")
            with session() as transaction_session:
                count = (
                    transaction_session.query(Appointments)
                    .filter(Appointments.hip_id == hip_id)
                    .count()
                )
            return count
        except Exception as error:
            logging.error(
                f"Error in CRUDAppointments count_all_appointments function : {error}"
            )
            raise error

    def count_appointments_status(self, hip_id: str):
        try:
            logging.info("CRUDAppointments count_appointments_status request")
            with session() as transaction_session:
                counts = (
                    transaction_session.query(
                        func.count(
                            case(
                                (Appointments.consultation_status == "Completed", 1),
                                else_=None,
                            )
                        ).label("completed_count"),
                        func.count(
                            case(
                                (Appointments.consultation_status == "InProgress", 1),
                                else_=None,
                            )
                        ).label("inprogress_count"),
                        func.count(
                            case(
                                (Appointments.consultation_status == "Scheduled", 1),
                                else_=None,
                            )
                        ).label("scheduled_count"),
                    )
                    .filter(Appointments.hip_id == hip_id)
                    .first()
                )

            return {
                "completed_count": counts.completed_count,
                "inprogress_count": counts.inprogress_count,
                "scheduled_count": counts.scheduled_count,
            }
        except Exception as error:
            logging.error(
                f"Error in CRUDAppointments count_appointments_status function : {error}"
            )
            raise error

    def count_appointments_type(self, hip_id: str):
        try:
            logging.info("CRUDAppointments count_appointments_type request")
            with session() as transaction_session:
                counts = (
                    transaction_session.query(
                        func.count(
                            case(
                                (Appointments.appointment_type == "first visit", 1),
                                else_=None,
                            )
                        ).label("first_visit_count"),
                        func.count(
                            case(
                                (
                                    Appointments.appointment_type == "follow-up visit",
                                    1,
                                ),
                                else_=None,
                            )
                        ).label("follow_up_count"),
                    )
                    .filter(Appointments.hip_id == hip_id)
                    .first()
                )

            return {
                "first_visit_count": counts.first_visit_count,
                "follow_up_count": counts.follow_up_count,
            }
        except Exception as error:
            logging.error(
                f"Error in CRUDAppointments count_appointments_type function : {error}"
            )
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
                    .order_by(Slots.start_time.asc())
                    .all()
                ):
                    start_time = slot_obj.start_time.strftime("%H:%M")
                    end_time = slot_obj.end_time.strftime("%H:%M")
                    patient_obj_dict = patient_obj.__dict__
                    patient_dob = patient_obj_dict.get("DOB")
                    if patient_dob:
                        dob = datetime.strptime(patient_dob, "%Y-%m-%d")
                        age_in_years, age_in_months = calculate_age(dob=dob)
                        patient_obj_dict["age_in_years"] = age_in_years
                        patient_obj_dict["age_in_months"] = age_in_months
                    else:
                        patient_yob = patient_obj_dict.get("year_of_birth", None)
                        today = datetime.today()
                        age_in_years = today.year - int(patient_yob)
                        patient_obj_dict["age_in_years"] = age_in_years
                    appointment_obj.__dict__.update(
                        {
                            "slot_time": str(f"{start_time}" + " - " + f"{end_time}"),
                            "patient_details": patient_obj_dict,
                            "doc_details": doctor_obj.__dict__,
                            "slot_details": slot_obj.__dict__,
                        },
                    )
                    joined_result.append(appointment_obj)
            if joined_result is not None:
                return joined_result
            return []
        except Exception as error:
            logging.error(f"Error in CRUDAppointments read_all function : {error}")
            raise error

    def read_appointments_by_date(self, hip_id: str, appointment_date: str):
        try:
            logging.info("CRUDAppointments read_appointments_by_date request")
            with session() as transaction_session:
                joined_result = []
                for appointment_obj, patient_obj, doctor_obj, slot_obj in (
                    transaction_session.query(
                        Appointments, PatientDetails, DocDetails, Slots
                    )
                    .filter(Appointments.hip_id == hip_id)
                    .filter(Appointments.appointment_date == appointment_date)
                    .filter(PatientDetails.id == Appointments.patient_id)
                    .filter(DocDetails.id == Appointments.doc_id)
                    .filter(Slots.slot_id == Appointments.slot_id)
                    .order_by(Slots.start_time.asc())
                    .all()
                ):
                    appointment_obj_dict = appointment_obj.__dict__
                    patient_obj_dict = patient_obj.__dict__
                    start_time = slot_obj.start_time.strftime("%H:%M")
                    end_time = slot_obj.end_time.strftime("%H:%M")
                    patient_dob = patient_obj_dict.get("DOB")
                    if patient_dob:
                        dob = datetime.strptime(patient_dob, "%Y-%m-%d")
                        age_in_years, age_in_months = calculate_age(dob=dob)
                        patient_obj_dict["age_in_years"] = age_in_years
                        patient_obj_dict["age_in_months"] = age_in_months
                    else:
                        patient_yob = patient_obj_dict.get("year_of_birth", None)
                        today = datetime.today()
                        age_in_years = today.year - int(patient_yob)
                        patient_obj_dict["age_in_years"] = age_in_years
                    appointment_obj_dict.update(
                        {
                            "patient_details": patient_obj_dict,
                            "slot_time": str(f"{start_time}" + " - " + f"{end_time}"),
                            "doc_details": doctor_obj.__dict__,
                        }
                    )
                    joined_result.append(appointment_obj_dict)
            if joined_result is not None:
                return joined_result
            return []
            #         pass
            #     obj: Appointments = (
            #         transaction_session.query(Appointments)
            #         .filter(Appointments.hip_id == hip_id)
            #         .filter(Appointments.appointment_date == appointment_date)
            #         .all()
            #     )
            # if obj is not None:
            #     return [row.__dict__ for row in obj]
            # return []
        except Exception as error:
            logging.error(
                f"Error in CRUDAppointments read_appointments_by_date function : {error}"
            )
            raise error

    def read_followups_by_date(self, hip_id: str, followup_date: str):
        try:
            logging.info("CRUDAppointments read_followups_by_date request")
            with session() as transaction_session:
                joined_result = []
                for appointment_obj, patient_obj, doctor_obj in (
                    transaction_session.query(Appointments, PatientDetails, DocDetails)
                    .filter(Appointments.hip_id == hip_id)
                    .filter(Appointments.followup_date == followup_date)
                    .filter(PatientDetails.id == Appointments.patient_id)
                    .filter(DocDetails.id == Appointments.doc_id)
                    .all()
                ):
                    patient_obj_dict = patient_obj.__dict__
                    patient_dob = patient_obj_dict.get("DOB")
                    if patient_dob:
                        dob = datetime.strptime(patient_dob, "%Y-%m-%d")
                        age_in_years, age_in_months = calculate_age(dob=dob)
                        patient_obj_dict["age_in_years"] = age_in_years
                        patient_obj_dict["age_in_months"] = age_in_months
                    else:
                        patient_yob = patient_obj_dict.get("year_of_birth", None)
                        today = datetime.today()
                        age_in_years = today.year - int(patient_yob)
                        patient_obj_dict["age_in_years"] = age_in_years
                    appointment_obj = appointment_obj.__dict__
                    appointment_op_obj = {
                        "id": appointment_obj.get("id"),
                        "appointment_date": appointment_obj.get("appointment_date"),
                        "followup_date": appointment_obj.get("followup_date"),
                        "patient_details": patient_obj_dict,
                        "doc_details": doctor_obj.__dict__,
                    }
                    joined_result.append(appointment_op_obj)
            if joined_result is not None:
                return joined_result
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDAppointments read_followups_by_date function : {error}"
            )
            raise error

    def read_all_followups_by_date(self, followup_date: str):
        try:
            logging.info("CRUDAppointments read_all_followups_by_date request")
            with session() as transaction_session:
                joined_result = []
                for appointment_obj, patient_obj, doctor_obj, hip_obj in (
                    transaction_session.query(
                        Appointments, PatientDetails, DocDetails, HIPDetail
                    )
                    .filter(Appointments.followup_date == followup_date)
                    .filter(PatientDetails.id == Appointments.patient_id)
                    .filter(DocDetails.id == Appointments.doc_id)
                    .filter(HIPDetail.hip_id == Appointments.hip_id)
                    .all()
                ):
                    patient_obj_dict = patient_obj.__dict__
                    appointment_obj_dict = appointment_obj.__dict__
                    doctor_obj_dict = doctor_obj.__dict__
                    hip_obj_dict = hip_obj.__dict__
                    details_obj = {
                        "appointment_date": appointment_obj_dict.get(
                            "appointment_date"
                        ).strftime("%Y-%m-%d"),
                        "followup_date": appointment_obj_dict.get(
                            "followup_date"
                        ).strftime("%Y-%m-%d"),
                        "patient_name": patient_obj_dict.get("name"),
                        "patient_contact_number": patient_obj_dict.get("mobile_number"),
                        "doctor_name": doctor_obj_dict.get("doc_name"),
                        "hip_name": hip_obj_dict.get("name"),
                        "hip_id": hip_obj_dict.get("hip_id"),
                        "hip_contact_number": hip_obj_dict.get("hip_contact_number"),
                    }
                    joined_result.append(details_obj)
            if joined_result is not None:
                return joined_result
            return []
        except Exception as error:
            logging.error(
                f"Error in CRUDAppointments read_all_followups_by_date function : {error}"
            )
            raise error

    def update(self, **kwargs):
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
                    .filter(Appointments.id == kwargs.get("id"))
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
