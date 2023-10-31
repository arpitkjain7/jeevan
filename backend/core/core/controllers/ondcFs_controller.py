from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core import logger
from datetime import datetime, timezone, timedelta
import base64
import json
from cryptography.hazmat.primitives import serialization
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from flask import Flask, request

import uuid


logging = logger(__name__)


class OndcFsController:
    def __init__(self):
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()

    def decrypt(self, enc_public_key, enc_private_key, cipherstring):
        private_key = serialization.load_der_private_key(
            base64.b64decode(enc_private_key), password=None
        )
        logging.info(f"{private_key=}")
        public_key = serialization.load_der_public_key(base64.b64decode(enc_public_key))
        logging.info(f"{public_key=}")
        shared_key = private_key.exchange(public_key)
        logging.info(f"{shared_key=}")
        cipher = AES.new(shared_key, AES.MODE_ECB)
        logging.info(f"{cipher=}")
        ciphertxt = base64.b64decode(cipherstring)
        logging.info(f"{ciphertxt=}")
        return unpad(cipher.decrypt(ciphertxt), AES.block_size).decode("utf-8")

    def on_subscribe_decypt(self, ondc_public_key, enc_private_key, request):
        try:
            logging.info("executing on_subscribe_decypt function")
            logging.info(f"{request.subscriber_id=}")
            question = request.challenge
            logging.info(f"{question=}")
            answer = self.decrypt(ondc_public_key, enc_private_key, question)
            logging.info(f"{answer=}")
            return {"answer": answer}
        except Exception as error:
            logging.error(
                f"Error in OndcFsController.on_subscribe_decypt function: {error}"
            )
            raise error
