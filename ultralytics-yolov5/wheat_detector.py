import detect
import os 

# Define the URL where Label Studio is accessible and the API key for your user account
LABEL_STUDIO_URL = 'http://localhost:8080'
API_KEY = 'dba3aa2a85021ed9982b9e14ca3e55605da66a3b'

# Import the SDK and the client module
from label_studio_sdk import Client


def run():
    result = detect.run(
        imgsz=(1280,1280),
        conf_thres=0.5,
        hide_labels=True, 
        weights="runs/train/exp/weights/best.pt",
        source="../images/1280/IMG_20230422_105651.jpg",
        view_img=True)
    
    print(result)

def connect_label_studio():
    # Connect to the Label Studio API and check the connection
    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    ls.check_connection()
    projects = ls.get_projects()

    project = ls.get_project(4)
    print(project.title)

    task = project.import_tasks(os.path.join('C:\\Users\\leona\\OneDrive\\Escritorio\\Posgrado\\wheat-detector-yolov5\\images\\1280', 'IMG_20230422_105651.jpg'))
    
    project.create_annotation(
        task[0], 
        result=[{
            "image_rotation": 0,
            "value": {
                "x": 43.98682042833607,
                "y": 2.417582417582418,
                "width": 7.578253706754529,
                "height": 7.2527472527472545,
                "rotation": 0,
                "rectanglelabels": [
                    "good"
                ]
            },
            "from_name": "label",
            "to_name": "image",
            "type": "rectanglelabels",
            "origin": "manual"
        }])

if __name__ == '__main__':
    connect_label_studio()