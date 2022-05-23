
from flask import Flask,request,send_file
from PIL import Image
from segmentation import chanvese
from multiprocessing import Process
import io
import base64
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
    iters = int(request.form.get("iters"))
    alpha = float(request.form.get("alpha"))
    img = Image.open(file)
    im_array = np.array(img)
    image = cv2.cvtColor(np.array(im_array),cv2.COLOR_BGR2GRAY)
    mask =  cv2.GaussianBlur(image,(5,5),cv2.BORDER_DEFAULT)
    mask = cv2.equalizeHist(mask)
    #chanvese(image,mask,max_its=1000,alpha=0.2,display=True)
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
    return "test"

if __name__ == "__main__":

    app.run(debug=True)
