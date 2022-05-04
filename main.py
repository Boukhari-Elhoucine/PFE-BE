
from flask import Flask,request,send_file
from PIL import Image
from segmentation import segment
import io
import cv2
import numpy as np

import matplotlib.pyplot as plt

app = Flask(__name__)
@app.route('/')
def index():
    return "hello"
@app.route("/process",methods=["POST"])
def process():
    if "file" not in request.files:
        return  "file not found"
    file = request.files["file"]
    img = Image.open(file)
    im_array = np.array(img)
    image = cv2.cvtColor(np.array(im_array),cv2.COLOR_BGR2GRAY)
    result = segment(image)
    cv2.imwrite("result.png",255*result)
    return "worked"

if __name__ == "__main__":

    app.run(debug=True)
