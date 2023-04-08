from core import session, logger
from core.orm_models.images import Images
from datetime import datetime

logging = logger(__name__)


class CRUDImages:
    def create(self, **kwargs):
        """[CRUD function to create a new Images record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDImages create request")
            kwargs.update(
                {
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            images = Images(**kwargs)
            with session() as transaction_session:
                transaction_session.add(images)
                transaction_session.commit()
                transaction_session.refresh(images)
        except Exception as error:
            logging.error(f"Error in CRUDImages create function : {error}")
            raise error

    def read_by_userId(self, user_id: int):
        """[CRUD function to read_by_userId a Image record]

        Args:
            user_id (int): [Images id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Images record matching the criteria]
        """
        try:
            logging.info("CRUDImages read_by_userId request")
            with session() as transaction_session:
                obj: Images = (
                    transaction_session.query(Images)
                    .filter(Images.owner_id == user_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDImages read_by_userId function : {error}")
            raise error

    def read_by_eventId(self, event_id: int, approval_flag: bool = True):
        """[CRUD function to read_by_eventId a Image record]

        Args:
            event_id (int): [Images id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Images record matching the criteria]
        """
        try:
            logging.info("CRUDImages read_by_eventId request")
            with session() as transaction_session:
                obj: Images = (
                    transaction_session.query(Images)
                    .filter(Images.event_id == event_id)
                    .filter(Images.approved == approval_flag)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDImages read_by_eventId function : {error}")
            raise error

    def read_by_key(self, image_key: str):
        """[CRUD function to read_by_eventId a Image record]

        Args:
            event_id (int): [Images id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Images record matching the criteria]
        """
        try:
            logging.info("CRUDImages read_by_eventId request")
            with session() as transaction_session:
                obj: Images = (
                    transaction_session.query(Images)
                    .filter(Images.s3_location == image_key)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDImages read_by_eventId function : {error}")
            raise error

    def read(self, image_id: str):
        """[CRUD function to read_by_eventId a Image record]

        Args:
            event_id (int): [Images id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Images record matching the criteria]
        """
        try:
            logging.info("CRUDImages read request")
            with session() as transaction_session:
                obj: Images = (
                    transaction_session.query(Images)
                    .filter(Images.id == image_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDImages read function : {error}")
            raise error

    def read_by_userId_eventId(self, event_id: int, user_id: int):
        """[CRUD function to read_by_eventId a Image record]

        Args:
            event_id (int): [Images id to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [Images record matching the criteria]
        """
        try:
            logging.info("CRUDImages read_by_eventId request")
            with session() as transaction_session:
                obj: Images = (
                    transaction_session.query(Images)
                    .filter(Images.event_id == event_id)
                    .filter(Images.owner_id == user_id)
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDImages read_by_eventId function : {error}")
            raise error

    def read_multiple(self, image_list: list):
        try:
            logging.info("CRUDImages read_multiple request")
            with session() as transaction_session:
                obj: Images = (
                    transaction_session.query(Images)
                    .filter(Images.id.in_(image_list))
                    .all()
                )
            if obj is not None:
                return [row.__dict__ for row in obj]
            else:
                return []
        except Exception as error:
            logging.error(f"Error in CRUDImages read_multiple function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a Images record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDImages update function")
            kwargs.update({"updated_at": datetime.now()})
            image_id = kwargs.get("image_id")
            del kwargs["image_id"]
            with session() as transaction_session:
                obj: Images = (
                    transaction_session.query(Images)
                    .filter(Images.id == image_id)
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDImages update function : {error}")
            raise error

    def delete(self, image_id: int):
        try:
            logging.info("CRUDImages delete function")
            with session() as transaction_session:
                obj: Images = (
                    transaction_session.query(Images)
                    .filter(Images.id == image_id)
                    .first()
                )
                transaction_session.delete(obj)
                transaction_session.commit()
                return obj.__dict__
        except Exception as error:
            logging.error(f"Error in CRUDImages delete function : {error}")
            raise error
