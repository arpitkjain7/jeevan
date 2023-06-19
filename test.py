import os
import uuid
import json
import subprocess
import re
from merkle_json import MerkleJson

dirname = "/Users/arpitjain/Documents/projects/jeevanhealthcare/jeevan/fidelius-cli-1.2.0/data"
binPath = "/Users/arpitjain/Documents/projects/jeevanhealthcare/jeevan/fidelius-cli-1.2.0/bin/fidelius-cli"


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
    return result


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


print(getEcdhKeyMaterial())
