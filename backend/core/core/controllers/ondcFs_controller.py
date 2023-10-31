from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core import logger
from datetime import datetime, timezone, timedelta
import os
import uuid
import json
import time
import os
import base64
import datetime
import json
import nacl.encoding
import nacl.hash
from nacl.signing import SigningKey
from cryptography.hazmat.primitives import serialization
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from flask import Flask, request
import requests
import uuid
import multiprocessing
import threading
import pytz


logging = logger(__name__)


class OndcFsController:
    def __init__(self):
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()

    def decrypt(enc_public_key, enc_private_key, cipherstring):
        private_key = serialization.load_der_private_key(
            base64.b64decode(enc_private_key), password=None
        )
        public_key = serialization.load_der_public_key(base64.b64decode(enc_public_key))
        shared_key = private_key.exchange(public_key)
        cipher = AES.new(shared_key, AES.MODE_ECB)
        ciphertxt = base64.b64decode(cipherstring)
        return unpad(cipher.decrypt(ciphertxt), AES.block_size).decode("utf-8")

    def on_subscribe_decypt(self, request):
        try:
            logging.info("executing  on_subscribe_decypt function")
            ondc_public_key = (
                "MCowBQYDK2VuAyEAduMuZgmtpjdCuxv+Nc49K0cB6tL/Dj3HZetvVN7ZekM="
            )
            enc_private_key = (
                "MC4CAQAwBQYDK2VuBCIEIAixt1l8nWtgbAHV714v09pRXapX6oFi2/uN9Vkp5mFD"
            )
            logging.info(f"{request.subscriber_id=}")
            logging.info(f"{request.challenge=}")
            answer = self.decrypt(ondc_public_key, enc_private_key, request.challenge)
            logging.info(f"{answer=}")
            return {"answer": answer}
        except Exception as error:
            logging.error(
                f"Error in OndcFsController.on_subscribe_decypt function: {error}"
            )
            raise error
