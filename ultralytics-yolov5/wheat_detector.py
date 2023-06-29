import detect
from label_studio_sdk import Client

# Define the URL where Label Studio is accessible and the API key for your user account
LABEL_STUDIO_URL = 'http://localhost:8080'
API_KEY = '631e560fab681593d71905198a1f284b94c8a40d'
PROJECT = 9

CATEGORIES = {
    "0": "bueno",
    "1": "da\u00f1ado",
    "2": "impureza",
    "3": "partido",
    "4": "quemado"
}

# Connect to the Label Studio API and check the connection
ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
ls.check_connection()

def detect_file_path(path, upload=False):
    report = {}
    labels = []

    for key in CATEGORIES:
        report[CATEGORIES[key]] = 0

    result = detect.run(
        imgsz=(3000,4000),
        conf_thres=0.2,
        hide_labels=False, 
        weights="../wheat_detector/weights/best.pt",
        source=path,
        save_txt=True,
        nosave=False,
        max_det=10000)
    
    result = filter_overlaped_areas(result)

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
        
        report[CATEGORIES[values[0]]]+=1

        labels.append(json)
    
    task = None

    if(upload):
        project = ls.get_project(PROJECT)

        task_id = project.import_tasks(path)
        project.create_annotation(
            task_id[0], 
            result = labels)
        
        task = project.get_task(task_id[0])

    return {
        "task": task,
        "path": result["path"].replace("\\","/"),
        "report": report
    }

def filter_overlaped_areas(result):
    lines = []
    boxes = []
    index = 0
    for line in result["lines"]:
        values = line.split(" ")

        w = float(values[3]) * 100
        h = float(values[4]) * 100
        x1 = (float(values[1]) * 100) - w/2
        y1 = (float(values[2]) * 100) - h/2
        x2 = x1 + w
        y2 = y1 + h

        boxes.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'line': line, 'index': index})
        index += 1

    print(len(boxes))
    for box1 in boxes:
        for box2 in boxes:
            iou = get_iou(box1, box2)
            if( iou>0.30 and box1['index'] != box2['index'] ):
                boxes.remove(box2)
                break    

    for box1 in boxes:
        lines.append(box1['line'])
    
    print(len(boxes))
    result['lines'] = lines

    return result

def get_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou