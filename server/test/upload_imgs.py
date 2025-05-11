import os
import sys
sys.path.append(os.getcwd())

import requests
from utils import get_file_modify_time


url = "http://127.0.0.1:9981/img/upload"

folder_path = "D:/80dataset/testImages"
store_folder_path = "F:/images_test"
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.bmp'):
        file_path = os.path.join(folder_path, filename)
        
        file_time = get_file_modify_time(file_path)
        print(file_time)

        with open(file_path, 'rb') as img:
            name_img_file = os.path.basename(file_path)
            files = {'file': (name_img_file, img, 'image/jpeg')}
            modify_time = os.path.getmtime(file_path)
            data = {'mod_time': str(modify_time)}
            response = requests.post(url, files=files, data=data)
        print(response.status_code)
        print(response.json())
