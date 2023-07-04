import json
import re
import os
from flask import Flask, request
from azure.storage.blob import BlobServiceClient
from office365_api import SharePoint

app = Flask(__name__)

FOLDER_DEST = "files"

def save_file(file_n, file_obj):
    blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=azuretestshubham832458;AccountKey=2yEaP59qlgKVv6kEUCA5ARB4wdV3ZRoL2X9zjYCcIxOSYAG1CSBbBlAMPx3uBIe7ilQtSh7purEK+AStvFn8GA==;EndpointSuffix=core.windows.net')
    container_client = blob_service_client.get_container_client('transcript')
    blob_client = container_client.get_blob_client(file_n)
    blob_client.upload_blob(file_obj)


def get_file(file_n, folder):
    file_obj = SharePoint().download_file(file_n, folder)
    save_file(file_n, file_obj)

def get_files(folder):
    files_list = SharePoint()._get_files_list(folder)
    for file in files_list:
        get_file(file.name, folder)

def get_files_by_pattern(keyword, folder):
    files_list = SharePoint()._get_files_list(folder)
    for file in files_list:
        if re.search(keyword, file.name):
            get_file(file.name, folder)

@app.route('/download', methods=['POST'])
def download_files():
    api_input = request.get_json()
    
    if 'filename' in api_input and 'folder' in api_input:
        file_name = api_input['filename']
        folder = api_input['folder']
        
        if file_name is None or file_name == '':
            get_files(folder)
        else:
            get_file(file_name, folder)
    
        return "Files downloaded successfully."
    else:
        return "Invalid API request."

if __name__ == '__main__':
    os.makedirs(FOLDER_DEST, exist_ok=True)  # Create the "files" folder if it doesn't exist
    app.run(host='0.0.0.0', port=5000)
