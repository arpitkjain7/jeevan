import openai
import os


class WhisperHelper:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.temperature = 0.0

    def translate(self, file_path: str, prompt: str = None):
        try:
            audio_file = open(file_path, "rb")
            translation = openai.audio.translations.create(
                model="whisper-1",
                file=audio_file,
                prompt=prompt,
                temperature=self.temperature,
            )
            return {"transcription": translation.text}
        except Exception as error:
            raise error

    def transcribe(self, file_path: str, prompt: str = None):
        try:
            audio_file = open(file_path, "rb")
            transcription = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                prompt=prompt,
                temperature=self.temperature,
            )
            return {"transcription": transcription.text}
        except Exception as error:
            raise error
