from fastapi import APIRouter, HTTPException, status, Depends
from core import logger
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from datetime import datetime, timezone, timedelta
from core.utils.aws.s3_helper import upload_file
import json
from core.utils.openai.whisper import WhisperHelper
from core.utils.openai.text_generation import TextGeneration
from core.utils.openai.prompt_generation import PromptGeneration
import os

logging = logger(__name__)


class AIController:
    def __init__(self):
        self.s3_bucket = os.environ["s3_location"]

    def whisper_transcribe(
        self,
        pmr_id: str,
        patient_id: str,
        audio_file_data: bytes,
        audio_file_name: str,
        translate: bool,
    ):
        try:
            logging.info("executing AIController.whisper_transcribe function")
            audio_file_folder_path = f"/app/audio_data/{patient_id}/{pmr_id}"
            os.makedirs(audio_file_folder_path, exist_ok=True)
            audio_file_path = f"{audio_file_folder_path}/{audio_file_name}"
            logging.info("Saving audio file to local")
            with open(audio_file_name, "wb") as f:
                f.write(audio_file_data)
            if translate:
                logging.info("Translating file using whisper")
                transcription_result = WhisperHelper().translate(
                    file_path=audio_file_path
                )
            else:
                logging.info("Trancribing file using whisper")
                transcription_result = WhisperHelper().transcribe(
                    file_path=audio_file_path
                )
            object_name = os.path.basename(audio_file_path)
            logging.info("Uploading audio file to s3")
            upload_file(
                file_name=audio_file_path,
                bucket=self.s3_bucket,
                object_name=f"PATIENT_DATA/{patient_id}/{pmr_id}/{object_name}",
            )
            logging.info("Deleting audio file from local")
            os.remove(audio_file_path)
            logging.info("Generating SOAP")
            prompt = PromptGeneration().prepare_doctor_soap_prompt(
                context=transcription_result.get("transcription"),
                file_struct_path="/app/audio_data/SOAP_doctor_format.json",
            )
            completion_result = TextGeneration().send_completion_request(prompt=prompt)
            return completion_result
        except Exception as error:
            logging.error(f"Error in AIController.whisper_transcribe function: {error}")
            raise error
