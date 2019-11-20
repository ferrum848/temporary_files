from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import os
import requests
import numpy as np
import json
import io
from requests_toolbelt import MultipartEncoder


def cvImage2QImage(cvImg):
    height, width, channel = cvImg.shape
    bytesPerLine = 3 * width
    cvImg = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
    qImg = QtGui.QImage(cvImg.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
    return qImg


def check_image_path(image_path):
    return os.path.splitext(image_path)[1] in ['.png', '.jpg', '.jpeg']


def load_image(orig_path):
    orig_path = str(orig_path)
    orig_image = cv2.imread(orig_path)
    return orig_image


def write_bytes(img, ext='.png'):
    #img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2BGR)
    encode_status, img_array = cv2.imencode(ext, img)
    if encode_status is True:
        return img_array.tobytes()
    raise RuntimeError('Can not encode input image')


def img_to_bytes_stream(img_np):
    img_bytes = write_bytes(img_np)
    return io.BytesIO(img_bytes)


def convert_bytes_to_bgra(image_bytes) -> np.ndarray:
    image_np_arr = np.asarray(bytearray(image_bytes), dtype="uint8")
    img = cv2.imdecode(image_np_arr, cv2.IMREAD_UNCHANGED)
    return img


def predict_distr(img, trimap, address):
    content_dict = {}
    content_dict["orig_img"] = ("orig_img", img_to_bytes_stream(img), 'image/*')
    content_dict["trimap_img"] = ("trimap_img", img_to_bytes_stream(trimap), 'image/*')
    content_dict["aux_data"] = json.dumps({'aaa': 'bbb'})

    encoder = MultipartEncoder(fields=content_dict)
    url = os.path.join(address, 'smarttool')

    response = requests.post(url, data=encoder, headers={'Content-Type': encoder.content_type})
    image_bytes = response.content
    predicted_img = convert_bytes_to_bgra(image_bytes)
    predicted_img = cv2.cvtColor(predicted_img, cv2.COLOR_RGBA2BGRA)

    pred_alpha = predicted_img[:, :, 3]
    return pred_alpha