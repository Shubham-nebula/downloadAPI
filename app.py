import json
import re
import os
from flask import Flask, request
from office365_api import SharePoint

app = Flask(__name__)

FOLDER_DEST = "files"

def save_file(file_n, file_obj):
    file_path = os.path.join(FOLDER_DEST, file_n)
    with open(file_path, 'wb') as f:
        f.write(file_obj)

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
