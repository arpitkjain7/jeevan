from core import session, logger
from core.orm_models.hims_template import Template
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDTemplate:
    def create(self, **kwargs):
        """[CRUD function to create a new User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDTemplate create request")
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
            template_details = Template(**kwargs)
            with session() as transaction_session:
                transaction_session.add(template_details)
                transaction_session.commit()
                transaction_session.refresh(template_details)
            return template_details.template_id
        except Exception as error:
            logging.error(f"Error in CRUDTemplate create function : {error}")
            raise error

    def read(self, template_id: int):
        """[CRUD function to read a User record]

        Args:
            template_id (int): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDTemplate read request")
            with session() as transaction_session:
                obj: Template = (
                    transaction_session.query(Template)
                    .filter(Template.template_id == template_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDTemplate read function : {error}")
            raise error

    def read_by_template_id(self, template_id: str):
        """[CRUD function to read a User record]

        Args:
            template_id (int): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDTemplate read request")
            with session() as transaction_session:
                obj: Template = (
                    transaction_session.query(Template)
                    .filter(Template.template_id == template_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDTemplate read function : {error}")
            raise error

    def read_all(self):
        """[CRUD function to read_all Users record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [list]: [all user records]
        """
        try:
            logging.info("CRUDTemplate read_all request")
            with session() as transaction_session:
                obj: Template = transaction_session.query(Template).all()
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDTemplate read_all function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDTemplate update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: Template = (
                    transaction_session.query(Template)
                    .filter(Template.template_id == kwargs.get("template_id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDTemplate update function : {error}")
            raise error

    def delete(self, template_id: int):
        """[CRUD function to delete a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDTemplate delete function")
            with session() as transaction_session:
                obj: Template = (
                    transaction_session.query(Template)
                    .filter(Template.template_id == template_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDTemplate delete function : {error}")
            raise error
