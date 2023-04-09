from core import session, logger
from core.orm_models.hrp_gatewayInteraction import GatewayInteration
from datetime import datetime

logging = logger(__name__)


class CRUDGatewayInteration:
    def create(self, **kwargs):
        """[CRUD function to create a new User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDUser create request")
            kwargs.update(
                {
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            gatway_obj = GatewayInteration(**kwargs)
            with session() as transaction_session:
                transaction_session.add(gatway_obj)
                transaction_session.commit()
                transaction_session.refresh(gatway_obj)
        except Exception as error:
            logging.error(f"Error in CRUDUser create function : {error}")
            raise error

    def read(self, request_id: str):
        """[CRUD function to read a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDUser read request")
            with session() as transaction_session:
                obj: GatewayInteration = (
                    transaction_session.query(GatewayInteration)
                    .filter(GatewayInteration.request_id == request_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDUser read function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDUser update function")
            kwargs.update({"updated_at": datetime.now()})
            with session() as transaction_session:
                obj: GatewayInteration = (
                    transaction_session.query(GatewayInteration)
                    .filter(GatewayInteration.request_id == kwargs.get("request_id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDUser update function : {error}")
            raise error

    def delete(self, session_parameter: str):
        pass
