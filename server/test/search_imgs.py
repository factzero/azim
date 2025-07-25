import os
import sys
sys.path.append(os.getcwd())

import requests


response = requests.post("http://127.0.0.1:9981/img/search", json={"txt": "树上有只鸟"})
print("response: ", response)
if (response.status_code == 200):
    data = response.json()['images']
    print(data)