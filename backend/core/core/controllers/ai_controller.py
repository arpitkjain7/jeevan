from core import logger
from core.utils.aws.s3_helper import upload_object
from core.utils.openai.whisper import WhisperHelper
from core.utils.openai.text_generation import TextGeneration
from core.utils.openai.prompt_generation import PromptGeneration
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from core.utils.openai.summary_generation import consolidate_summaries
import os
from datetime import datetime

logging = logger(__name__)


class AIController:
    def __init__(self):
        self.s3_bucket = os.environ["s3_location"]
        self.CRUDPatientMedicalRecord = CRUDPatientMedicalRecord()

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
            with open(audio_file_path, "wb") as f:
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
            file_name = os.path.basename(audio_file_path)
            logging.info("Uploading audio file to s3")
            logging.info(f"PATIENT_DATA/{patient_id}/{pmr_id}/{file_name}")
            upload_object(
                file_name=audio_file_path,
                bucket_name=self.s3_bucket,
                object_name=f"PATIENT_DATA/{patient_id}/{pmr_id}/{file_name}",
            )
            logging.info("Deleting audio file from local")
            os.remove(audio_file_path)
            logging.info("Generating SOAP")
            transcription_str = transcription_result.get("transcription")
            prompt = PromptGeneration().prepare_doctor_soap_prompt(
                context=transcription_str,
                file_struct_path="/app/audio_data/SOAP_doctor_format.json",
            )
            new_clinical_notes = TextGeneration().send_completion_request(
                prompt=prompt, chat=True
            )
            pmr_obj = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
            existing_clinical_notes = pmr_obj.get("summarised_notes")
            existing_clinical_transcript = pmr_obj.get("raw_transcripts")
            now = datetime.now()
            timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
            if existing_clinical_notes:
                consolidated_summary_notes = consolidate_summaries(
                    dict1=existing_clinical_notes, dict2=new_clinical_notes
                )
            else:
                consolidated_summary_notes = new_clinical_notes
            if existing_clinical_transcript:
                existing_clinical_transcript.update({timestamp_str: transcription_str})
                consolidated_transcripts = existing_clinical_transcript
            else:
                consolidated_transcripts = {timestamp_str: transcription_str}
            self.CRUDPatientMedicalRecord.update(
                **{
                    "id": pmr_id,
                    "summarised_notes": consolidated_summary_notes,
                    "raw_transcripts": consolidated_transcripts,
                }
            )
            return consolidated_summary_notes
        except Exception as error:
            logging.error(f"Error in AIController.whisper_transcribe function: {error}")
            raise error

    def update_summary(self, request):
        try:
            logging.info("Calling AIController.update_summary controller")
            request_dict = request.dict()
            logging.debug(f"Request: {request_dict}")
            pmr_id = request_dict.get("pmr_id")
            del request_dict["pmr_id"]
            pmr_id = self.CRUDPatientMedicalRecord.update(
                **{"id": pmr_id, "summarised_notes": request_dict}
            )
            return {"pmr_id": pmr_id, "status": "success"}
        except Exception as error:
            logging.error(f"Error in AIController.update_summary function: {error}")
            raise error
