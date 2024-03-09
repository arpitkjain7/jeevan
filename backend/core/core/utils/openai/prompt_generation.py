import json
import os
import openai


class PromptGeneration:
    def __init__(self):
        pass

    def prepare_doctor_soap_prompt(self, context, file_struct_path):
        with open(file_struct_path, "r") as fp:
            struct = json.load(fp)
        prompt = f"""You are an NER AI designed to assist in generating detailed Medical SOAP report from Conversation Transcript and any additional information that may be provided.
        Please analyze the following Report Structure json and populate the structured report template with the relevant information extracted.
        DO NOT ADD ANY DATA NOT PRESENT IN CONVERSATION INTO THE REPORT STRUCTURE. STRICTLY REPRODUCE DATA FROM CONVERSATION CONTENT ONLY.
        Conversation Transcript:
        {context}
        Please organize the extracted information according to this detailed report structure:
        Report Structure:
        {json.dumps(struct, indent=4)}"""
        return prompt
