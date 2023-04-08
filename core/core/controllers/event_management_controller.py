from fastapi import HTTPException, status
from core.crud.events_crud import CRUDEvents
from core.crud.images_crud import CRUDImages
from core.crud.users_crud import CRUDUser
from core.crud.attendees_crud import CRUDAttendees
from core.utils.aws.s3_helper import (
    create_bucket,
    upload_to_s3,
    create_presigned_url,
    delete_s3,
)
from core.utils.aws.lambda_helper import invoke_thumbnail_creation
from core.utils.custom.qrcode_generation import qrcode_generator
from core import logger
import random, string, os
from datetime import datetime, timedelta
import requests

logging = logger(__name__)


class EventManagementController:
    def __init__(self):
        self.CRUDEvents = CRUDEvents()
        self.CRUDAttendees = CRUDAttendees()
        self.CRUDImages = CRUDImages()
        self.CRUDUser = CRUDUser()

    def create_event_controller(self, request, owner_id):
        try:
            logging.info("executing create_event_controller function")
            logging.info("checking user limit")
            event_list = self.CRUDEvents.read_by_owner_id(user_id=owner_id)
            user_role = self.CRUDUser.read(email_id=owner_id)["user_role"]
            if user_role != "HOST":
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="Only Premium users can create Events. Please upgrade to Premium",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if len(event_list) <= 5:
                # pin = str(int(datetime.now().timestamp() * 10000000000))[-4:]
                pin = str(random.randint(1000, 9999))
                idx = str(int(datetime.now().timestamp() * 1000000))
                event_unique_name = request.event_name.replace(" ", "-")
                event_uuid = "".join(
                    random.choices(string.ascii_letters + string.digits, k=16)
                )
                bucket_name = f"albumd-{event_unique_name.lower()}-{idx}"
                bucket_created = create_bucket(
                    bucket_name=bucket_name, region="ap-south-1"
                )
                default_bucket = os.environ["albumdekho_s3"]
                default_cover = os.environ["default_cover"]
                default_cover_presigned = create_presigned_url(
                    bucket_name=default_bucket, key=default_cover, expires_in=604800
                )
                valid_upto = datetime.now() + timedelta(seconds=604800)
                if bucket_created:
                    crud_request = {
                        "event_name": request.event_name,
                        "owner_id": owner_id,
                        "event_uuid": event_uuid,
                        "event_pin": pin,
                        "event_metadata": {
                            "event_date": request.event_date,
                            "event_location": request.event_location,
                            "event_bucket": bucket_name,
                            "coverphoto": default_cover_presigned,
                            "coverphoto_valid_upto": str(valid_upto),
                        },
                    }
                    event_id = self.CRUDEvents.create(**crud_request)
                    return {
                        "event_id": event_id,
                        "event_uuid": event_uuid,
                        "event_name": request.event_name,
                        "owner_id": owner_id,
                        "event_metadata": {
                            "event_date": request.event_date,
                            "event_location": request.event_location,
                            "event_bucket": bucket_name,
                        },
                    }
                else:
                    raise Exception("S3 bucket not created")
            else:
                raise Exception("Event creation limit reached")
        except Exception as error:
            logging.error(f"Error in create_event_controller function: {error}")
            raise error

    def get_qr_controller(self, event_id):
        try:
            event_obj = self.CRUDEvents.read(event_id=event_id)
            event_metadata = event_obj.get("event_metadata")
            qrcode_presigned_url = event_metadata.get("qr_code", None)
            if qrcode_presigned_url:
                qr_valid_upto = event_metadata.get("qr_valid_upto", None)
                qr_valid_upto = datetime.strptime(qr_valid_upto, "%Y-%m-%d %H:%M:%S.%f")
                datetime_now = datetime.now()
                if qr_valid_upto <= datetime_now:
                    event_bucket_name = event_obj["event_metadata"]["event_bucket"]
                    event_name = event_obj["event_name"]
                    s3_key = f"{event_name}/metadata/qr.png"
                    qrcode_presigned_url = create_presigned_url(
                        bucket_name=event_bucket_name, key=s3_key, expires_in=604800
                    )
                    event_metadata.update(
                        {
                            "qr_code": qrcode_presigned_url,
                            "qr_valid_upto": str(valid_upto),
                        }
                    )
                    crud_request = {
                        "event_id": event_id,
                        "event_metadata": event_metadata,
                    }
                    self.CRUDEvents.update(**crud_request)
            else:
                qr_code_location = qrcode_generator(
                    event_uuid=event_obj["event_uuid"],
                    event_bucket=event_metadata["event_bucket"],
                    event_name=event_obj["event_name"],
                )
                qrcode_presigned_url = create_presigned_url(
                    bucket_name=event_metadata["event_bucket"],
                    key=qr_code_location["s3_key"],
                    expires_in=604800,
                )
                valid_upto = datetime.now() + timedelta(seconds=604800)
                event_metadata.update(
                    {
                        "qr_code": qrcode_presigned_url,
                        "qr_valid_upto": str(valid_upto),
                    }
                )
                crud_request = {
                    "event_id": event_id,
                    "event_metadata": event_metadata,
                }
                self.CRUDEvents.update(**crud_request)
            return {"qr_code": qrcode_presigned_url}
        except Exception as error:
            logging.error(f"Error in get_qr_controller function: {error}")
            raise error

    def publish_event_controller(self, event_id, event_status):
        try:
            logging.info("executing publish_event_controller function")
            event_obj = self.CRUDEvents.read(event_id=event_id)
            if event_obj:
                if (
                    event_status.upper() == "ACTIVE"
                    or event_status.upper() == "INACTIVE"
                ):
                    crud_request = {
                        "event_id": event_id,
                        "event_status": event_status.upper(),
                    }
                    self.CRUDEvents.update(**crud_request)
                    event_uuid = event_obj.get("event_uuid")
                    logging.info(f"{event_uuid=}")
                    return {
                        "event_id": event_id,
                        "event_uuid": event_uuid,
                        "event_status": event_status.upper(),
                    }
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid value for event status",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as error:
            logging.error(f"Error in publish_event_controller function: {error}")
            raise error

    def get_event_by_user_controller(self, user_id: str):
        try:
            logging.info("executing get_event_by_user_controller function")
            owner_list, active_event_list, inactive_event_list, guest_list = (
                [],
                [],
                [],
                [],
            )
            owner_obj = self.CRUDEvents.read_by_owner_id(user_id=user_id)
            owner_list.extend(
                {
                    "event_id": obj["id"],
                    "event_name": obj["event_name"],
                    "event_metadata": obj["event_metadata"],
                    "event_status": obj["event_status"],
                }
                for obj in owner_obj
            )
            attendee_obj = self.CRUDAttendees.read_by_user_id(user_id=user_id)
            for obj in attendee_obj:
                if obj.get("status") == "ACTIVE":
                    active_event_list.append(obj.get("event_id"))
                else:
                    inactive_event_list.append(obj.get("event_id"))
            if active_event_list:
                active_guest_obj = self.CRUDEvents.read_multiple(
                    event_list=active_event_list
                )
                for obj in active_guest_obj:
                    guest_list.append(
                        {
                            "event_id": obj["id"],
                            "event_name": obj["event_name"],
                            "event_metadata": obj["event_metadata"],
                            "event_status": obj["event_status"],
                            "user_status": "ACTIVE",
                        }
                    )
            if inactive_event_list:
                inactive_guest_obj = self.CRUDEvents.read_multiple(
                    event_list=inactive_event_list
                )
                for obj in inactive_guest_obj:
                    guest_list.append(
                        {
                            "event_id": obj["id"],
                            "event_name": obj["event_name"],
                            "event_status": obj["event_status"],
                            "user_status": "INACTIVE",
                        }
                    )

            return {"owner_list": owner_list, "guest_list": guest_list}
        except Exception as error:
            logging.error(f"Error in get_event_controller function: {error}")
            raise error

    def get_event_controller(self, event_id: str):
        try:
            logging.info("executing get_event_controller function")
            return self.CRUDEvents.read(event_id=event_id)
        except Exception as error:
            logging.error(f"Error in get_event_controller function: {error}")
            raise error

    def get_event_by_uuid_controller(self, event_uuid: str):
        try:
            logging.info("executing get_event_by_uuid_controller function")
            event_obj = self.CRUDEvents.read_by_uuid(event_uuid=event_uuid)
            return event_obj
        except Exception as error:
            logging.error(f"Error in get_event_by_uuid_controller function: {error}")
            raise error

    def get_event_metadata_by_uuid_controller(self, event_uuid: str):
        try:
            logging.info("executing get_event_metadata_by_uuid_controller function")
            event_obj = self.CRUDEvents.read_by_uuid(event_uuid=event_uuid)
            event_metadata = event_obj["event_metadata"]
            coverphoto_url = event_metadata["coverphoto"]
            coverphoto_valid_upto = event_metadata.get("coverphoto_valid_upto", None)
            if coverphoto_valid_upto:
                coverphoto_valid_upto = datetime.strptime(
                    coverphoto_valid_upto, "%Y-%m-%d %H:%M:%S.%f"
                )
            if coverphoto_valid_upto <= datetime.now():
                event_bucket_name = event_metadata["event_bucket"]
                s3_key = "/".join(
                    coverphoto_url.split(event_bucket_name)[-1]
                    .split("?")[0]
                    .split("/")[1:]
                )
                coverphoto_url = create_presigned_url(
                    bucket_name=event_bucket_name, key=s3_key, expires_in=604800
                )
                valid_upto = datetime.now() + timedelta(seconds=604800)
                event_metadata.update(
                    {
                        "coverphoto": coverphoto_url,
                        "coverphoto_valid_upto": str(valid_upto),
                    }
                )
                crud_request = {
                    "event_id": event_obj["id"],
                    "event_metadata": event_metadata,
                }
                self.CRUDEvents.update(**crud_request)
            return {
                "event_name": event_obj["event_name"],
                "event_coverphoto": coverphoto_url,
                "event_date": str(event_obj["event_metadata"]["event_date"]),
            }
        except Exception as error:
            logging.error(
                f"Error in get_event_metadata_by_uuid_controller function: {error}"
            )
            raise error

    def activate_event_controller(self, event_uuid: str, user_id: str, pass_code: str):
        try:
            logging.info("executing activate_event_controller function")
            logging.debug(f"{event_uuid=}")
            logging.debug(f"{user_id=}")
            logging.debug(f"{pass_code=}")
            event_obj = self.CRUDEvents.read_by_uuid(event_uuid=event_uuid)
            logging.debug(f"{event_obj=}")
            if event_obj:
                if pass_code == event_obj.get("event_pin"):
                    logging.debug("valid pin")
                    self.CRUDAttendees.update(
                        **{
                            "user_id": user_id,
                            "event_id": event_obj.get("id"),
                            "status": "ACTIVE",
                        }
                    )
                    return event_obj
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Invalid event pin",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event does not exist",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as error:
            logging.error(f"Error in activate_event_controller function: {error}")
            raise error

    def add_image_controller(
        self, user_id: str, event_id: str, data: bytes, file_name: str
    ):
        try:
            logging.info("executing add_image_controller function")
            event_obj = self.CRUDEvents.read(event_id=event_id)
            event_bucket_name = event_obj.get("event_metadata").get("event_bucket")
            event_name = event_obj.get("event_name").translate(
                str.maketrans("", "", string.punctuation)
            )
            s3_key = f"{event_name}/base_image/{file_name}"
            thumbnails_s3_key = f"{event_name}/thumbnail/{file_name}"
            event_obj = self.CRUDEvents.read(event_id=event_id)
            event_owner = event_obj.get("owner_id")
            _ = upload_to_s3(
                bucket_name=event_bucket_name, byte_data=data, file_name=s3_key
            )
            invoke_thumbnail_creation(bucket_name=event_bucket_name, s3_key=s3_key)
            presigned_url = create_presigned_url(
                bucket_name=event_bucket_name, key=s3_key, expires_in=604800
            )
            thumbnail_presigned_url = create_presigned_url(
                bucket_name=event_bucket_name, key=thumbnails_s3_key, expires_in=604800
            )
            valid_upto = datetime.now() + timedelta(seconds=604800)
            s3_location = f"s3://{event_bucket_name}/{s3_key}"
            existing_img_obj = self.CRUDImages.read_by_key(s3_location)
            if existing_img_obj:
                self.CRUDImages.update(
                    **{
                        "image_id": existing_img_obj.get("id"),
                        "s3_url": presigned_url,
                        "thumbnail_url": thumbnail_presigned_url,
                    }
                )
            else:
                if user_id == event_owner:
                    approved_flag = True
                else:
                    approved_flag = False
                crud_request = {
                    "owner_id": user_id,
                    "event_id": event_id,
                    "s3_location": s3_location,
                    "s3_url": presigned_url,
                    "thumbnail_url": thumbnail_presigned_url,
                    "approved": approved_flag,
                    "valid_upto": valid_upto,
                }
                self.CRUDImages.create(**crud_request)
        except Exception as error:
            logging.error(f"Error in add_image_controller function: {error}")
            raise error

    def add_image_urls_controller(self, event_id: str, files: str, user_id: str):
        try:
            logging.info("executing add_image_urls_controller function")
            logging.info(f"{event_id=}")
            logging.info(f"{files=}")
            event_obj = self.CRUDEvents.read(event_id=event_id)
            logging.info(f"{event_obj=}")
            event_bucket_name = event_obj.get("event_metadata").get("event_bucket")
            event_name = event_obj.get("event_name")
            file_list_str = files.files
            for file_loc in file_list_str.split(","):
                file_loc = file_loc.strip()
                file_name = file_loc.split("/")[-1]
                s3_key = f"{event_name}/base_image/{file_name}"
                thumbnails_s3_key = f"{event_name}/thumbnail/{file_name}"
                event_obj = self.CRUDEvents.read(event_id=event_id)
                event_owner = event_obj.get("owner_id")
                file_url = f"https:{file_loc}"
                r = requests.get(file_url, allow_redirects=True)
                logging.info(f"{r.status_code=}")
                _ = upload_to_s3(
                    bucket_name=event_bucket_name, byte_data=r.content, file_name=s3_key
                )
                invoke_thumbnail_creation(bucket_name=event_bucket_name, s3_key=s3_key)
                presigned_url = create_presigned_url(
                    bucket_name=event_bucket_name, key=s3_key, expires_in=604800
                )
                thumbnail_presigned_url = create_presigned_url(
                    bucket_name=event_bucket_name,
                    key=thumbnails_s3_key,
                    expires_in=604800,
                )
                valid_upto = datetime.now() + timedelta(seconds=604800)
                s3_location = f"s3://{event_bucket_name}/{s3_key}"
                existing_img_obj = self.CRUDImages.read_by_key(s3_location)
                if existing_img_obj:
                    self.CRUDImages.update(
                        **{
                            "image_id": existing_img_obj.get("id"),
                            "s3_url": presigned_url,
                            "thumbnail_url": thumbnail_presigned_url,
                        }
                    )
                else:
                    if user_id == event_owner:
                        approved_flag = True
                    else:
                        approved_flag = False
                    crud_request = {
                        "owner_id": user_id,
                        "event_id": event_id,
                        "s3_location": s3_location,
                        "s3_url": presigned_url,
                        "thumbnail_url": thumbnail_presigned_url,
                        "approved": approved_flag,
                        "valid_upto": valid_upto,
                    }
                    self.CRUDImages.create(**crud_request)
        except Exception as error:
            logging.error(f"Error in add_image_urls_controller function: {error}")
            raise error

    def add_cover_photo(self, event_id: str, user_id: str, data: bytes, file_name: str):
        try:
            logging.info("executing add_cover_photo function")
            event_obj = self.CRUDEvents.read(event_id=event_id)
            event_bucket_name = event_obj.get("event_metadata").get("event_bucket")
            event_name = event_obj.get("event_name").translate(
                str.maketrans("", "", string.punctuation)
            )
            s3_key = f"{event_name}/base_image/{file_name}"
            thumbnails_s3_key = f"{event_name}/thumbnail/{file_name}"
            event_obj = self.CRUDEvents.read(event_id=event_id)
            event_owner = event_obj.get("owner_id")
            _ = upload_to_s3(
                bucket_name=event_bucket_name, byte_data=data, file_name=s3_key
            )
            invoke_thumbnail_creation(bucket_name=event_bucket_name, s3_key=s3_key)
            presigned_url = create_presigned_url(
                bucket_name=event_bucket_name, key=s3_key, expires_in=604800
            )
            thumbnail_presigned_url = create_presigned_url(
                bucket_name=event_bucket_name, key=thumbnails_s3_key, expires_in=604800
            )
            valid_upto = datetime.now() + timedelta(seconds=604800)
            event_metadata = event_obj.get("event_metadata")
            event_metadata.update(
                {
                    "coverphoto": thumbnail_presigned_url,
                    "coverphoto_valid_upto": str(valid_upto),
                }
            )
            self.CRUDEvents.update(
                **{"event_id": event_id, "event_metadata": event_metadata}
            )
            return {"status": "SUCCESS", "message": "Coverphoto added successfully"}
        except Exception as error:
            logging.error(f"Error in add_cover_photo function: {error}")
            raise error

    def get_event_images_controller(self, event_id: str, user_id: str):
        try:
            logging.info("executing get_event_images_controller function")
            all_images, user_images = [], []
            event_obj = self.CRUDEvents.read(event_id=event_id)
            all_image_obj = self.CRUDImages.read_by_eventId(event_id=event_id)
            for obj in all_image_obj:
                image_valid_upto = obj.get("valid_upto")
                presigned_url = obj.get("s3_url")
                thumbnail_presigned_url = obj.get("thumbnail_url")
                datetime_now = datetime.now()
                if image_valid_upto <= datetime_now:
                    event_bucket_name = (
                        obj.get("s3_location").split("//")[-1].split("/")[0]
                    )
                    s3_key = "/".join(
                        obj.get("s3_location").split("//")[-1].split("/")[1:]
                    )
                    presigned_url = create_presigned_url(
                        bucket_name=event_bucket_name, key=s3_key, expires_in=604800
                    )
                    thumbnails_s3_key = s3_key.replace("base_image", "thumbnail")
                    thumbnail_presigned_url = create_presigned_url(
                        bucket_name=event_bucket_name,
                        key=thumbnails_s3_key,
                        expires_in=604800,
                    )
                    valid_upto = datetime.now() + timedelta(seconds=604800)
                    self.CRUDImages.update(
                        **{
                            "image_id": obj.get("id"),
                            "s3_url": presigned_url,
                            "thumbnail_url": thumbnail_presigned_url,
                            "valid_upto": valid_upto,
                        }
                    )
                if user_id == event_obj.get("owner_id"):
                    all_images.append(
                        {
                            "image_id": obj.get("id"),
                            "s3_url": presigned_url,
                            "thumbnail_url": thumbnail_presigned_url,
                            "s3_location": obj.get("s3_location"),
                            "owner_id": obj.get("owner_id"),
                            "annotations": obj.get("annotations"),
                        }
                    )
                if obj.get("annotations") is not None:
                    if user_id in obj.get("annotations"):
                        user_images.append(
                            {
                                "image_id": obj.get("id"),
                                "s3_url": presigned_url,
                                "thumbnail_url": thumbnail_presigned_url,
                                "s3_location": obj.get("s3_location"),
                                "owner_id": obj.get("owner_id"),
                                "annotations": obj.get("annotations"),
                            }
                        )
            return {"all_images": all_images, "user_images": user_images}
        except Exception as error:
            logging.error(f"Error in get_event_controller function: {error}")
            raise error

    def get_event_images_for_approval_controller(self, event_id: str, user_id: str):
        try:
            logging.info("executing get_event_images_for_approval_controller function")
            all_images = []
            approval_images = self.CRUDImages.read_by_eventId(
                event_id=event_id, approval_flag=False
            )
            for obj in approval_images:
                image_valid_upto = obj.get("valid_upto")
                presigned_url = obj.get("s3_url")
                thumbnail_presigned_url = obj.get("thumbnail_url")
                datetime_now = datetime.now()
                if image_valid_upto <= datetime_now:
                    event_bucket_name = (
                        obj.get("s3_location").split("//")[-1].split("/")[0]
                    )
                    s3_key = "/".join(
                        obj.get("s3_location").split("//")[-1].split("/")[1:]
                    )
                    presigned_url = create_presigned_url(
                        bucket_name=event_bucket_name, key=s3_key, expires_in=604800
                    )
                    thumbnails_s3_key = s3_key.replace("base_image", "thumbnail")
                    thumbnail_presigned_url = create_presigned_url(
                        bucket_name=event_bucket_name,
                        key=thumbnails_s3_key,
                        expires_in=604800,
                    )
                    valid_upto = datetime.now() + timedelta(seconds=604800)
                    self.CRUDImages.update(
                        **{
                            "image_id": obj.get("id"),
                            "s3_url": presigned_url,
                            "thumbnail_url": thumbnail_presigned_url,
                            "valid_upto": valid_upto,
                        }
                    )
                all_images.append(
                    {
                        "image_id": obj.get("id"),
                        "s3_url": presigned_url,
                        "thumbnail_url": thumbnail_presigned_url,
                        "s3_location": obj.get("s3_location"),
                        "owner_id": obj.get("owner_id"),
                        "annotations": obj.get("annotations"),
                    }
                )
            return {"images": all_images}
        except Exception as error:
            logging.error(
                f"Error in get_event_images_for_approval_controller function: {error}"
            )
            raise error

    def get_event_images_for_approval_controller(self, event_id: str, user_id: str):
        try:
            logging.info("executing get_event_images_for_approval_controller function")
            all_images = []
            approval_images = self.CRUDImages.read_by_eventId(
                event_id=event_id, approval_flag=False
            )
            for obj in approval_images:
                image_valid_upto = obj.get("valid_upto")
                presigned_url = obj.get("s3_url")
                thumbnail_presigned_url = obj.get("thumbnail_url")
                datetime_now = datetime.now()
                if image_valid_upto <= datetime_now:
                    event_bucket_name = (
                        obj.get("s3_location").split("//")[-1].split("/")[0]
                    )
                    s3_key = "/".join(
                        obj.get("s3_location").split("//")[-1].split("/")[1:]
                    )
                    presigned_url = create_presigned_url(
                        bucket_name=event_bucket_name, key=s3_key, expires_in=604800
                    )
                    thumbnails_s3_key = s3_key.replace("base_image", "thumbnail")
                    thumbnail_presigned_url = create_presigned_url(
                        bucket_name=event_bucket_name,
                        key=thumbnails_s3_key,
                        expires_in=604800,
                    )
                    valid_upto = datetime.now() + timedelta(seconds=604800)
                    self.CRUDImages.update(
                        **{
                            "image_id": obj.get("id"),
                            "s3_url": presigned_url,
                            "thumbnail_url": thumbnail_presigned_url,
                            "valid_upto": valid_upto,
                        }
                    )
                all_images.append(
                    {
                        "image_id": obj.get("id"),
                        "s3_url": presigned_url,
                        "thumbnail_url": thumbnail_presigned_url,
                        "s3_location": obj.get("s3_location"),
                        "owner_id": obj.get("owner_id"),
                        "annotations": obj.get("annotations"),
                    }
                )
            return {"images": all_images}
        except Exception as error:
            logging.error(
                f"Error in get_event_images_for_approval_controller function: {error}"
            )
            raise error

    def delete_image(self, image_id: str):
        try:
            logging.info("executing delete_image function")
            image_obj = self.CRUDImages.read(image_id=image_id)
            image_s3_location = image_obj.get("s3_location")
            event_bucket_name = image_s3_location.split("//")[-1].split("/")[0]
            s3_key = "/".join(image_s3_location.split("//")[-1].split("/")[1:])
            thumbnail_s3_key = s3_key.replace("base_image", "thumbnail")
            delete_s3(bucket_name=event_bucket_name, key=s3_key)
            delete_s3(bucket_name=event_bucket_name, key=thumbnail_s3_key)
            self.CRUDImages.delete(image_id=image_id)
            return {"status": "SUCCESS", "message": "Image deleted successfully"}
        except Exception as error:
            logging.error(
                f"Error in get_event_images_for_approval_controller function: {error}"
            )
            raise error

    def approve_image(self, image_id: str):
        try:
            logging.info("executing approve_image function")
            self.CRUDImages.update(**{"image_id": image_id, "approved": True})
            return {"status": "SUCCESS", "message": "Image approved"}
        except Exception as error:
            logging.error(f"Error in approve_image function: {error}")
            raise error

    def approve_all_images(self, event_id: str, owner_id: str):
        try:
            logging.info("executing approve_all_images function")
            image_obj_list = self.CRUDImages.read_by_userId_eventId(
                event_id=event_id, user_id=owner_id
            )
            for obj in image_obj_list:
                image_id = obj.get("id")
                self.CRUDImages.update(**{"image_id": image_id, "approved": True})
            return {"status": "SUCCESS", "message": "Images approved"}
        except Exception as error:
            logging.error(f"Error in approve_all_images function: {error}")
            raise error

    def get_validity_status(self, event_uuid: str, user_id: str):
        try:
            logging.info("executing get_validity_status function")
            event_published = False
            attendee_activated = False
            selfi_uploaded = False
            event_obj = self.CRUDEvents.read_by_uuid(event_uuid=event_uuid)
            if event_obj:
                logging.info(f"{event_obj=}")
                if event_obj["event_status"] == "ACTIVE":
                    event_published = True
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Event does not exist",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user_obj = self.CRUDUser.read(email_id=user_id)
            if user_obj:
                logging.info(f"{user_obj=}")
                if (
                    user_obj["base_image_location"] is not None
                    and user_obj["base_image_location"] != ""
                ):
                    selfi_uploaded = True
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User does not exist",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            attendee_obj = self.CRUDAttendees.read(
                user_id=user_id, event_id=event_obj["id"]
            )
            if attendee_obj:
                logging.info(f"{attendee_obj=}")
                if attendee_obj["status"] == "ACTIVE":
                    attendee_activated = True
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Attendee does not exist",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return {
                "event_published": event_published,
                "selfi_uploaded": selfi_uploaded,
                "attendee_activated": attendee_activated,
            }
        except Exception as error:
            logging.error(f"Error in get_validity_status function: {error}")
            raise error
