import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt
from .segment_anything import sam_model_registry, SamPredictor
from .segment_anything.utils.onnx import SamOnnxModel

import onnxruntime
from onnxruntime.quantization import QuantType
from onnxruntime.quantization.quantize import quantize_dynamic

import urllib.request
from io import BytesIO


def get_embedding(img_url):
    checkpoint = "static/models/sam_vit_h_4b8939.pth"
    model_type = "vit_h"
    sam = sam_model_registry[model_type](checkpoint=checkpoint)
    sam.to(device='cuda')
    predictor = SamPredictor(sam)

    resp = urllib.request.urlopen(img_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")

    # Decode the image
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    predictor.set_image(image)
    image_embedding = predictor.get_image_embedding().cpu().numpy()
    np.save("static/dist/assets/data/embedding.npy", image_embedding)

