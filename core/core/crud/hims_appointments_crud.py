from core import session, logger
from core.orm_models.hims_appointments import Appointments
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
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            appointment = Appointments(**kwargs)
            with session() as transaction_session:
                transaction_session.add(appointment)
                transaction_session.commit()
                transaction_session.refresh(appointment)
        except Exception as error:
            logging.error(f"Error in CRUDAppointments create function : {error}")
            raise error

    def read_by_docId(self, doc_id: str):
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
                    .filter(Appointments.doc_id == doc_id)
                    .order_by(Appointments.date_of_appointment.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDAppointments read function : {error}")
            raise error

    def read_by_patientId(self, patient_id: str):
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
                    .order_by(Appointments.date_of_appointment.desc())
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDAppointments read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Users record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all user records]
        """
        try:
            logging.info("CRUDAppointments read_all request")
            with session() as transaction_session:
                obj: Appointments = transaction_session.query(Appointments).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            return []
        except Exception as error:
            logging.error(f"Error in CRUDAppointments read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDAppointments update function")
            kwargs.update({"updated_at": datetime.now()})
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
