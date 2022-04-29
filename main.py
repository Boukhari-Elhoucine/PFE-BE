from segmentation import chanves
from flask import Flask,request

app = Flask(__name__)
@app.route('/')
def index():
    return "hello"
@app.route("/process",methods=["POST"])
def process():
    if "file" not in request.files:
        return  "file not found"
    file = request.files["file"]
    print(file.filename)
    return "file found"

if __name__ == "__main__":
    app.run(debug=True)