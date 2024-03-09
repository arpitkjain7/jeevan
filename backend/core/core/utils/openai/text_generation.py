import json
import os
import openai


class TextGeneration:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model_name = os.environ.get("OPENAI_MODEL")
        self.temperature = 0.0
        self.max_tokens = 2000

        if self.api_key:
            openai.api_key = self.api_key

    def send_completion_request(
        self, prompt: str, chat: bool = False, stream: bool = False
    ) -> dict:
        response = {}
        if chat:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {
                        "role": "user",
                        "content": "Ensure the report is comprehensive, structured, and strictly adhere to the report Structure. Patient Report json:",
                    },
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=stream,
            )
            response = response.choices[0].message.content
        else:
            response = openai.completions.create(
                model=self.model_name,
                prompt=f"""{prompt}. \nEnsure the report is comprehensive, structured, and strictly adhere to the report Structure. Patient Report json:""",
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=stream,
            )
            response = response.choices[0].text
        return json.loads(response)
