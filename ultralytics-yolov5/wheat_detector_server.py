import io
import os
from flask import Flask, request
from flask_cors import CORS
from PIL import Image
from wheat_detector import create_task
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/api/photo/upload", methods=['POST'])
def upload():
    file = request.data 
    image = Image.open(io.BytesIO(file))
    if(image.height > image.width):
        image = image.rotate(90)
    image = image.resize((1280, 920), Image.ANTIALIAS)

    now = datetime.now()
    path = "tmp_files/" + now.strftime("%H%M%S") + ".jpg"
    image.save(path)
    
    create_task(path)

    if os.path.isfile(path):
        os.remove(path)

    return {'ok': 'ok'}