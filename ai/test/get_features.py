import os
import sys
sys.path.append(os.getcwd())

import requests

# img_response = requests.post("http://127.0.0.1:9988" + "/ai/img_feature", 
#                              json={"url": "http://localhost:9981/img/get-img/f817c093f7e5405bbd2b7a07e0c2d517"})

img_response = requests.post("http://127.0.0.1:9988/ai/img_feature", 
                             json={"url": "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"})
# print("img feature: ", img_response.json())
img_feature = img_response.json()["feature"]
print("img feature: ", img_feature)

# txt_response = requests.post("http://127.0.0.1:9988/ai/txt_feature", json={"text": "皮卡丘"})
# # print("txt feature: ", txt_response.json())
# txt_feature = txt_response.json()["feature"]

# sim = requests.post("http://127.0.0.1:9988/ai/get_similarity", 
#                     json={"feature1": img_feature, "feature2": txt_feature})
# print("similarity: ", "皮卡丘 ", sim.json())

# txt_response = requests.post("http://127.0.0.1:9988/ai/txt_feature", json={"text": "树上有只鸟"})
# # print("txt feature: ", txt_response.json())
# txt_feature = txt_response.json()["feature"]

# sim = requests.post("http://127.0.0.1:9988/ai/get_similarity", 
#                     json={"feature1": img_feature, "feature2": txt_feature})
# print("similarity: ", "树上有只鸟 ", sim.json())