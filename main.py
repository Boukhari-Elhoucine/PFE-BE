from segmentation import chanves
from flask import Flask,request,send_file
from PIL import Image
from segmentation import chanves
import io
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
    im_array = np.array(Image.open(file))
    result = chanves(im_array[:,:,0])
    image = Image.fromarray(result.astype("uint8"))
    file_object = io.BytesIO()
    image.save(file_object,"PNG")
    file_object.seek(0)
    return send_file(file_object,mimetype="image/PNG")

if __name__ == "__main__":

    app.run(debug=True)
