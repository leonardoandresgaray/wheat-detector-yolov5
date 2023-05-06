import io
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
from wheat_detector import detect_file_path
from datetime import datetime

TMP_PATH = "tmp_files/"
app = Flask(__name__)
CORS(app)

@app.route("/api/photo/upload", methods=['POST'])
def upload_file():
    path = save_file(request.data) 
    
    detection = detect_file_path(path)

    # Remove temporal file
    if os.path.isfile(path):
        os.remove(path)

    return jsonify(detection)

@app.route("/api/photo/detect", methods=['POST'])
def detect_fil():
    path = save_file(request.data) 
    
    detection = detect_file_path(path)

    # Remove temporal file
    if os.path.isfile(path):
        os.remove(path)

    return jsonify(detection)

def save_file(file):
    image = Image.open(io.BytesIO(file))
    if(image.height > image.width):
        image = image.rotate(90)
    image = image.resize((1280, 920), Image.ANTIALIAS)

    now = datetime.now()
    path = TMP_PATH + now.strftime("%H%M%S") + ".jpg"
    image.save(path)

    return path

@app.route("/image", methods=['GET'])
def image():
    image_path = request.args.get('path')
    return send_file(image_path, mimetype='image/jpg')