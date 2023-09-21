import cv2
import json


def read_qr_code(filename):
    """Read an image and read the QR code.

    Args:
        filename (string): Path to file

    Returns:
        qr (string): Value from QR code
    """

    try:
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = detect.detectAndDecodeMulti(img)
        # value, points, straight_qrcode = detect.detectAndDecode(img)
        # print(retval)
        # print(decoded_info)
        # print(points)
        # print(straight_qrcode)
        print(type(decoded_info[0]))
        json_obj = json.loads(decoded_info[0])
        print(type(json_obj))
        return json_obj
    except:
        return


print(
    read_qr_code(
        filename="/Users/arpitjain/Documents/projects/jeevanhealthcare/documents/test-data/arpit-abha-card.png"
    )
)
