from core.crud.users_crud import CRUDUser
from core.apis.schemas.requests.user_request import Register
from core.controllers.user_management_controller import UserManagementController

from core import logger

logging = logger(__name__)


def create_admin_user(admin_user_request):
    existing_admin_user = CRUDUser().read(email_id=admin_user_request.email_id)
    if not existing_admin_user:
        _ = UserManagementController().register_user_controller(
            request=admin_user_request
        )
    else:
        pass


def main():
    admin_user_request = Register(
        email_id="admin@fmf.com",
        name="admin",
        password="P@ssw0rd",
        user_role="admin",
        phone_number=123456789,
    )
    create_admin_user(admin_user_request=admin_user_request)
