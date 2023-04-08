from core.crud.events_crud import CRUDEvents
from core.crud.images_crud import CRUDImages
from core.crud.users_crud import CRUDUser
from core.crud.attendees_crud import CRUDAttendees
from core.crud.annotations_crud import CRUDAnnotations
from core.utils.aws.s3_helper import create_bucket, upload_to_s3, create_presigned_url
from core.utils.aws.rekog_helper import compare_faces
from core import logger
import secrets, os
from datetime import datetime
from datetime import datetime, timedelta
import requests

logging = logger(__name__)


class AnnotationController:
    def __init__(self):
        self.CRUDUser = CRUDUser()
        self.CRUDEvents = CRUDEvents()
        self.CRUDAttendees = CRUDAttendees()
        self.CRUDImages = CRUDImages()
        self.CRUDAnnotations = CRUDAnnotations()
        self.default_bucket = os.environ.get("albumdekho_s3")

    def add_user_selfi(self, user_id: str, data: bytes, file_name: str):
        try:
            logging.info("executing add_user_selfi function")
            s3_key = f"user_data/{user_id}/selfi/{file_name}"
            logging.info(f"{s3_key=}")
            _ = upload_to_s3(
                bucket_name=self.default_bucket, byte_data=data, file_name=s3_key
            )
            crud_request = {
                "email_id": user_id,
                "base_image_location": f"s3://{self.default_bucket}/{s3_key}",
            }
            self.CRUDUser.update(**crud_request)
            return {"status": "SUCCESS", "message": "Image uploaded successfully"}
        except Exception as error:
            logging.error(f"Error in add_user_selfi function: {error}")
            raise error

    def check_user_validity(self, user_id: str):
        try:
            user_obj = self.CRUDUser.read(email_id=user_id)
            if user_obj["base_image_location"]:
                return True
            return False
        except Exception as error:
            logging.error(f"Error in check_user_validity function: {error}")
            raise error

    def check_event_validity(self, user_id: str, event_id: str):
        try:
            attendee_obj = self.CRUDAttendees.read(user_id=user_id, event_id=event_id)
            event_obj = self.CRUDEvents.read(event_id=event_id)
            if (
                attendee_obj
                and attendee_obj.get("status") == "ACTIVE"
                and event_obj.get("event_status") == "ACTIVE"
            ):
                return True
            return False
        except Exception as error:
            logging.error(f"Error in check_validity function: {error}")
            raise error

    def start_annotation(self, event_id: str, user_id: str):
        try:
            logging.info("executing start_annotation function")
            event_image_list = [
                obj.get("id")
                for obj in self.CRUDImages.read_by_eventId(event_id=event_id)
            ]
            logging.info(f"{event_image_list=}")
            existing_annotation_list = [
                obj.get("image_id")
                for obj in self.CRUDAnnotations.read_by_event_user_id(
                    event_id=event_id, user_id=user_id
                )
            ]
            logging.info(f"{existing_annotation_list=}")
            existing_annotation_set = set(existing_annotation_list)
            logging.info(f"{existing_annotation_set=}")
            event_image_set = set(event_image_list)
            logging.info(f"{event_image_set=}")
            annotation_delta_set = event_image_set - existing_annotation_set
            logging.info(f"{annotation_delta_set=}")
            annotation_image_list = self.CRUDImages.read_multiple(
                image_list=list(annotation_delta_set)
            )
            logging.info(f"{annotation_image_list=}")
            source_image_location = self.CRUDUser.read(email_id=user_id)[
                "base_image_location"
            ]
            for image in annotation_image_list:
                target_image_location = image.get("s3_location")
                target_image_location = target_image_location.replace(
                    "base_image", "thumbnail"
                )
                matched_faces = compare_faces(
                    sourceFileKey=source_image_location,
                    targetFileKey=target_image_location,
                )
                annotation_request = {
                    "image_id": image["id"],
                    "event_id": image["event_id"],
                    "user_id": user_id,
                    "annotation_metadata": {"faceMatch": matched_faces},
                }
                self.CRUDAnnotations.create(**annotation_request)
                if len(matched_faces) == 0:
                    continue
                existing_annotations = image["annotations"]
                logging.info(f"{existing_annotations=}")
                logging.info(f"{type(existing_annotations)=}")
                if existing_annotations:
                    existing_annotations.append(user_id)
                    annotation_req = {
                        "image_id": image["id"],
                        "annotations": existing_annotations,
                    }
                else:
                    new_annotations = [user_id]
                    annotation_req = {
                        "image_id": image["id"],
                        "annotations": new_annotations,
                    }
                self.CRUDImages.update(**annotation_req)
        except Exception as error:
            logging.error(f"Error in start_annotation function: {error}")
            raise error
