import detect
from label_studio_sdk import Client

# Define the URL where Label Studio is accessible and the API key for your user account
LABEL_STUDIO_URL = 'http://localhost:8080'
API_KEY = 'dba3aa2a85021ed9982b9e14ca3e55605da66a3b'
PROJECT = 8

CATEGORIES = {
    "0": "bueno",
    "1": "danado",
    "2": "impureza",
    "3": "partido",
    "4": "quemado"
}

# Connect to the Label Studio API and check the connection
ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
ls.check_connection()

def detect_file_path(path):
    labels = []
    result = detect.run(
        imgsz=(1280,1280),
        conf_thres=0.5,
        hide_labels=True, 
        weights="../wheat_detector/weights/best.pt",
        source=path,
        save_txt=True,
        nosave=False)
    
    for line in result["lines"]:
        values = line.split(" ")
        json = {
            "image_rotation": 0,
            "from_name": "label",
            "to_name": "image",
            "type": "rectanglelabels",
            "origin": "manual"
        }

        w = float(values[3]) * 100
        h = float(values[4]) * 100
        x = (float(values[1]) * 100) - w/2
        y = (float(values[2]) * 100) - h/2
        json["value"] = {
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "rotation": 0,
            "rectanglelabels": [
                CATEGORIES[values[0]]
            ]
        }

        labels.append(json)
    
    project = ls.get_project(PROJECT)

    task_id = project.import_tasks(path)
    project.create_annotation(
        task_id[0], 
        result = labels)
    
    task = project.get_task(task_id[0])

    return {
        "task": task,
        "path": result["path"].replace("\\","/")
    }

# def getTasksFromProject():
#     projects = ls.get_projects()
#     project = ls.get_project(3)
#     tasks = project.get_tasks()
#     for task in tasks:
#         if (len(task['annotations']) == 0):
#             labels = []
#             image_name = re.sub(r'\/data\/upload\/.*\-', '', task["data"]["image"])
            
#             results = detect.run(
#                 imgsz=(1280,1280),
#                 conf_thres=0.5,
#                 hide_labels=True, 
#                 weights="./wheat_detector/weights/best.pt",
#                 source="./images/1280/" + image_name,
#                 save_txt=True,
#                 nosave=True)
            
#             for result in results:
#                 values = result.split(" ")
#                 json = {
#                     "image_rotation": 0,
#                     "from_name": "label",
#                     "to_name": "image",
#                     "type": "rectanglelabels",
#                     "origin": "manual",
#                     "original_width": 1280,
#                     "original_height": 960,
#                     "id": uuid.uuid4().hex[:10]
#                 }

#                 w = float(values[3]) * 100
#                 h = float(values[4]) * 100
#                 x = (float(values[1]) * 100) - w/2
#                 y = (float(values[2]) * 100) - h/2
#                 json["value"] = {
#                     "x": x,
#                     "y": y,
#                     "width": w,
#                     "height": h,
#                     "rotation": 0,
#                     "rectanglelabels": [
#                         categories[values[0]]
#                     ]
#                 }

#                 labels.append(json)
            
#             project.create_annotation(task["id"], result = labels)

#if __name__ == '__main__':
    #run()
    #getTasksFromProject()