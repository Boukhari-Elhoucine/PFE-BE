
from flask import Flask,request,send_file,jsonify
from PIL import Image
from segmentation import chanvese
from multiprocessing import Process
import io
from base64 import encodebytes
import cv2
import numpy as np

import matplotlib.pyplot as plt

app = Flask(__name__)
@app.route('/')
def index():
    return "hello"

def get_response_image(image_path):

    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

@app.route("/process",methods=["POST"])
def process():
    if "file" not in request.files:
        return  "file not found"
    file = request.files["file"]
    iters = int(request.form.get("iters"))
    alpha = float(request.form.get("alpha"))
    img = Image.open(file)
    im_array = np.array(img)
    image = cv2.cvtColor(np.array(im_array),cv2.COLOR_BGR2GRAY)
    mask =  cv2.GaussianBlur(image,(5,5),cv2.BORDER_DEFAULT)
    mask = cv2.equalizeHist(mask)
    p = Process(target=chanvese,args=(image,mask,iters,alpha,0,'r',True))
    p.start()
    p.join()
   # result = segment(image)
    #res_n=cv2.normalize(result,dst=None,alpha=0,beta=255,norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_8U)
    #out_image = Image.fromarray(res_n)
    #buff = io.BytesIO()
    #out_image.save(buff, format="PNG")
    #image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    #return image_string
    encoded_images = []
    for path in ['./levelset_start.png','./levelset_end.png']:
        encoded_images.append(get_response_image(path))
    return jsonify({'result':encoded_images})

if __name__ == "__main__":

    app.run(debug=False)
