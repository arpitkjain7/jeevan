from core import session, logger
from core.orm_models.annotations import Annotations
from datetime import datetime

logging = logger(__name__)


class CRUDAnnotations:
    def create(self, **kwargs):
        """[CRUD function to create a new Annotations record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDAnnotations create request")
            kwargs.update(
                {
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            annotation = Annotations(**kwargs)
            with session() as transaction_session:
                transaction_session.add(annotation)
                transaction_session.commit()
                transaction_session.refresh(annotation)
            return annotation.id
        except Exception as error:
            logging.error(f"Error in CRUDAnnotations create function : {error}")
            raise error

    def read(self, annotation_id: int):
        """[CRUD function to read a Annotations record]

        Args:
            pricing_id (str): [Annotations Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Annotations record matching the criteria]
        """
        try:
            logging.info("CRUDAnnotations read request")
            with session() as transaction_session:
                obj: Annotations = (
                    transaction_session.query(Annotations)
                    .filter(Annotations.id == annotation_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDAnnotations read function : {error}")
            raise error

    def read_by_user_id(self, user_id: str):
        """[CRUD function to read a Annotations record]

        Args:
            cognitive_service (str): [Annotations Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Annotations record matching the criteria]
        """
        try:
            logging.info("CRUDAnnotations read_by_user_id request")
            with session() as transaction_session:
                obj: Annotations = (
                    transaction_session.query(Annotations)
                    .filter(Annotations.user_id == user_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(
                f"Error in CRUDAnnotations read_by_user_id function : {error}"
            )
            raise error

    def read_by_event_id(self, event_id: str):
        """[CRUD function to read a Annotations record]

        Args:
            cognitive_service (str): [Annotations Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Annotations record matching the criteria]
        """
        try:
            logging.info("CRUDAnnotations read_by_user_id request")
            with session() as transaction_session:
                obj: Annotations = (
                    transaction_session.query(Annotations)
                    .filter(Annotations.event_id == event_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(
                f"Error in CRUDAnnotations read_by_event_id function : {error}"
            )
            raise error

    def read_by_event_user_id(self, event_id: str, user_id: str):
        """[CRUD function to read a Annotations record]

        Args:
            cognitive_service (str): [Annotations Id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Annotations record matching the criteria]
        """
        try:
            logging.info("CRUDAnnotations read_by_user_id request")
            with session() as transaction_session:
                obj: Annotations = (
                    transaction_session.query(Annotations)
                    .filter(Annotations.event_id == event_id)
                    .filter(Annotations.user_id == user_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(
                f"Error in CRUDAnnotations read_by_event_user_id function : {error}"
            )
            raise error

    def update(self, **kwargs):
        pass

    def delete(self):
        pass
