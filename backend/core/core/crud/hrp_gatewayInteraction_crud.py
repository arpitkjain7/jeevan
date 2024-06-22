from core import session, logger
from core.orm_models.hrp_gatewayInteraction import GatewayInteraction
from datetime import datetime
from pytz import timezone

logging = logger(__name__)


class CRUDGatewayInteraction:
    def create(self, **kwargs):
        """[CRUD function to create a new User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDGatewayInteraction create request")
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
            gatway_obj = GatewayInteraction(**kwargs)
            with session() as transaction_session:
                transaction_session.add(gatway_obj)
                transaction_session.commit()
                transaction_session.refresh(gatway_obj)
        except Exception as error:
            logging.error(f"Error in CRUDGatewayInteraction create function : {error}")
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
            logging.info("CRUDGatewayInteraction read request")
            with session() as transaction_session:
                obj: GatewayInteraction = (
                    transaction_session.query(GatewayInteraction)
                    .filter(GatewayInteraction.request_id == request_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDGatewayInteraction read function : {error}")
            raise error

    def read_by_transId(self, transaction_id: str, request_type: str):
        """[CRUD function to read a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDGatewayInteraction read_by_txnId request")
            with session() as transaction_session:
                obj: GatewayInteraction = (
                    transaction_session.query(GatewayInteraction)
                    .filter(GatewayInteraction.transaction_id == transaction_id)
                    .filter(GatewayInteraction.request_type == request_type)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDGatewayInteraction read function : {error}")
            raise error

    def read_by_transId_v1(self, transaction_id: str):
        """[CRUD function to read a User record]

        Args:
            user_name (str): [User name to filter the record]

        Raises:
            error: [Error returned from the DB layer]

        Returns:
            [dict]: [user record matching the criteria]
        """
        try:
            logging.info("CRUDGatewayInteraction read_by_txnId request")
            with session() as transaction_session:
                obj: GatewayInteraction = (
                    transaction_session.query(GatewayInteraction)
                    .filter(GatewayInteraction.transaction_id == transaction_id)
                    .first()
                )
            if obj is not None:
                return obj.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f"Error in CRUDGatewayInteraction read function : {error}")
            raise error

    def update(self, **kwargs):
        """[CRUD function to update a User record]

        Raises:
            error: [Error returned from the DB layer]
        """
        try:
            logging.info("CRUDGatewayInteraction update function")
            kwargs.update(
                {
                    "updated_at": datetime.now(timezone("Asia/Kolkata")).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                }
            )
            with session() as transaction_session:
                obj: GatewayInteraction = (
                    transaction_session.query(GatewayInteraction)
                    .filter(GatewayInteraction.request_id == kwargs.get("request_id"))
                    .update(kwargs, synchronize_session=False)
                )
                transaction_session.commit()
        except Exception as error:
            logging.error(f"Error in CRUDGatewayInteraction update function : {error}")
            raise error

    def delete(self, session_parameter: str):
        pass
