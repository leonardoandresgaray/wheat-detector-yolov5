import shutil
import zipfile
import os
from label_studio_sdk import Client

# Define the URL where Label Studio is accessible and the API key for your user account
LABEL_STUDIO_URL = 'http://localhost:8080'
# API_KEY = '631e560fab681593d71905198a1f284b94c8a40d'
API_KEY = 'dba3aa2a85021ed9982b9e14ca3e55605da66a3b'
PROJECT = 9
ZIP_FILE_PATH = '..\\datasets\\wheat001.zip'
EXPORT_PATH = '..\\datasets\\wheat001'

# Connect to the Label Studio API and check the connection
ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
ls.check_connection()

def export():
    project = ls.get_project(PROJECT)

    response = project.make_request(
        method='GET', url=f'/api/projects/{project.id}/export', params={
            'exportType': 'YOLO'
        }
    )

    with open(ZIP_FILE_PATH, 'wb') as f:
        f.write(response.content)
    f.close()

    shutil.rmtree(EXPORT_PATH)

    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
        zip_ref.extractall(EXPORT_PATH)

    os.remove(ZIP_FILE_PATH)

if __name__ == '__main__':
    export()