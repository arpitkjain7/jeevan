import os
import uuid
import json
import subprocess
import re
from merkle_json import MerkleJson
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
import base64

dirname = "/app/fidelius-cli-1.2.0/data"
binPath = "/app/fidelius-cli-1.2.0/bin/fidelius-cli"


def execFideliusCli(args):
    fideliusCommand = [binPath] + args
    result = subprocess.run(fideliusCommand, stdout=subprocess.PIPE, encoding="UTF-8")
    try:
        return json.loads(result.stdout)
    except:
        print(f'ERROR · execFideliusCli · Command: {" ".join(args)}\n{result.stdout}')


def getEcdhKeyMaterial():
    result = execFideliusCli(["gkm"])
    return result


def writeParamsToFile(*params):
    fileContents = "\n".join(params)
    filePath = os.path.join(dirname, "temp", f"{str(uuid.uuid4())}.txt")
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    f = open(filePath, "a")
    f.write(fileContents)
    f.close()
    return filePath


def removeFileAtPath(filePath):
    os.remove(filePath)


def encryptData(encryptParams):
    paramsFilePath = writeParamsToFile(
        "e",
        encryptParams["stringToEncrypt"],
        encryptParams["senderNonce"],
        encryptParams["requesterNonce"],
        encryptParams["senderPrivateKey"],
        encryptParams["requesterPublicKey"],
    )
    result = execFideliusCli(["-f", paramsFilePath])
    removeFileAtPath(paramsFilePath)
    return result


def decryptData(decryptParams):
    paramsFilePath = writeParamsToFile(
        "d",
        decryptParams["encryptedData"],
        decryptParams["requesterNonce"],
        decryptParams["senderNonce"],
        decryptParams["requesterPrivateKey"],
        decryptParams["senderPublicKey"],
    )
    result = execFideliusCli(["-f", paramsFilePath])
    removeFileAtPath(paramsFilePath)
    return json.dumps(result)


def encrypt_data(
    stringToEncrypt: str, senderKeyMaterial: dict, requesterKeyMaterial: dict
):
    # requesterKeyMaterial = {
    #     "publicKey": "BHX+PzGQKYrecFuDqYNQohtcCobHSoLXiJ82QU/+uKHpUJ1jZ7Bv8Dl2Pq2FdjC9gOyCxCzAz7QcAC1EkA/D024=",
    #     "nonce": "lIEBhv1ILTRtfNvBsUV3qLJqWlhuHvIiXXJ6v9KusQw=",
    # }
    encryptionResult = encryptData(
        {
            "stringToEncrypt": stringToEncrypt,
            "senderNonce": senderKeyMaterial["nonce"],
            "requesterNonce": requesterKeyMaterial["nonce"],
            "senderPrivateKey": senderKeyMaterial["privateKey"],
            "requesterPublicKey": requesterKeyMaterial["dhPublicKey"]["keyValue"],
        }
    )
    return {"encryptedData": encryptionResult["encryptedData"]}


def generateChecksum(json_data: dict):
    mj = MerkleJson()
    checksum = mj.hash(json_data)
    return checksum


def rsa_encryption(data_to_encrypt: str):
    public_key = open("/app/core/utils/custom/publickey.txt", "r").read()
    public_key = serialization.load_pem_public_key(
        public_key.encode(), backend=default_backend()
    )
    encrypted_data = public_key.encrypt(data_to_encrypt.encode(), padding.PKCS1v15())
    base64_encrypted_data = base64.b64encode(encrypted_data)
    return base64_encrypted_data.decode()


def rsa_encryption_oaep(data_to_encrypt: str):
    public_key = open("/app/core/utils/custom/publickey.txt", "r").read()
    public_key = serialization.load_pem_public_key(
        public_key.encode(), backend=default_backend()
    )
    oaep_padding = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None
    )

    encrypted_data = public_key.encrypt(data_to_encrypt.encode(), oaep_padding)

    base64_encrypted_data = base64.b64encode(encrypted_data)
    return base64_encrypted_data.decode("utf-8")
