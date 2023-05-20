# Label Studio
python label_studio/manage.py runserver

# Label Studio React recompiling
cd label-studio-local
npx webpack --watch

# Wheat Detector Server
python -m flask --app ultralytics-yolov5/wheat_detector_server run --debug