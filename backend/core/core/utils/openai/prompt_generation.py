import json
import os
import openai


class PromptGeneration:
    def __init__(self):
        pass

    def prepare_doctor_soap_prompt(self, context, file_struct_path):
        with open(file_struct_path, "r") as fp:
            struct = json.load(fp)
        prompt = f"""You are an medical analyser designed to assist in generating detailed Medical SOAP report from doctor patient conversation provided in context.
        Output should be in the following report structured report template with the relevant information extracted from the context provided.
        Report Structure:
        {json.dumps(struct, indent=4)}
        The output should be strictly extracted from the context provided below. Do not add any details that is not provided in the context. If context is not relevant, provide blank report as output.
        Context:
        {context}"""
        return prompt
