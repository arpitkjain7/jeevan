from core.utils.custom.encryption_helper import getEcdhKeyMaterial
import json


class DataTransferController:
    def __init__(self):
        pass

    def generate_key(self):
        try:
            print("Generating encryption key1")
            generated_keys = getEcdhKeyMaterial()
            print(f"{generated_keys=}")
            print(f"{type(generated_keys)=}")
            return generated_keys
        except Exception as error:
            print(f"Error in DataTransferController.generate_key function: {error}")
            raise error
