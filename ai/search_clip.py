# -*- coding: utf-8 -*-
import onnxruntime
import torch
from PIL import Image
import numpy as np
import cn_clip.clip as clip
from cn_clip.clip.utils import _MODEL_INFO, image_transform
import requests
from io import BytesIO


def get_similarity(image_features, text_features):
    '''
    计算图像和文本之间的相似度
    '''
    image_features = torch.as_tensor(image_features)
    text_features = torch.as_tensor(text_features)
    print("image_features.shape: ", image_features.shape)
    print("text_features.shape: ", text_features.shape)
    
    logits_per_image = 100 * image_features @ text_features.t()
    
    return logits_per_image


class CNCLIP:
    def __init__(self, img_onnx_path, text_onnx_path, model_arch='ViT-L-14-336'):
        # 载入ONNX图像侧模型
        img_sess_options = onnxruntime.SessionOptions()
        img_run_options = onnxruntime.RunOptions()
        img_run_options.log_severity_level = 2
        self.img_session = onnxruntime.InferenceSession(img_onnx_path,
                                                sess_options=img_sess_options)
        
        # 载入ONNX文本侧模型
        txt_sess_options = onnxruntime.SessionOptions()
        txt_run_options = onnxruntime.RunOptions()
        txt_run_options.log_severity_level = 2
        self.txt_session = onnxruntime.InferenceSession(text_onnx_path,
                                                sess_options=txt_sess_options)
        
        self.model_arch = model_arch
        
    def preprocess(self, image_path):
        # 预处理图片
        preprocess = image_transform(_MODEL_INFO[self.model_arch]['input_resolution'])
        # 示例皮卡丘图片，预处理后得到[1, 3, 分辨率, 分辨率]尺寸的Torch Tensor
        image = preprocess(Image.open(image_path)).unsqueeze(0)
        
        return image

    def encode_image(self, image_path):
        image = self.preprocess(image_path)
        # 用ONNX模型计算图像侧特征
        image_features = self.img_session.run(["unnorm_image_features"], {"image": image.cpu().numpy()})[0] # 未归一化的图像特征
        image_features = torch.tensor(image_features)
        image_features /= image_features.norm(dim=-1, keepdim=True) # 归一化后的Chinese-CLIP图像特征，用于下游任务
        
        return image_features
    
    
    def encode_image_url(self, url):
        response = requests.get(url)
        preprocess = image_transform(_MODEL_INFO[self.model_arch]['input_resolution'])
        image = preprocess(Image.open(BytesIO(response.content))).unsqueeze(0)
        # 用ONNX模型计算图像侧特征
        image_features = self.img_session.run(["unnorm_image_features"], {"image": image.cpu().numpy()})[0] # 未归一化的图像特征
        image_features = torch.tensor(image_features)
        image_features /= image_features.norm(dim=-1, keepdim=True) # 归一化后的Chinese-CLIP图像特征，用于下游任务
        
        return image_features
    
    
    def encode_image_path(self, image_path):
        image = self.preprocess(image_path)
        # 用ONNX模型计算图像侧特征
        image_features = self.img_session.run(["unnorm_image_features"], {"image": image.cpu().numpy()})[0] # 未归一化的图像特征
        image_features = torch.tensor(image_features)
        image_features /= image_features.norm(dim=-1, keepdim=True) # 归一化后的Chinese-CLIP图像特征，用于下游任务
        
        return image_features

    def encode_text(self, text):
        # 为输入文本进行分词。序列长度指定为52，需要和转换ONNX模型时保持一致（参见转换时的context-length参数）
        text = clip.tokenize(text, context_length=52)
        # 用ONNX模型依次计算文本侧特征
        text_features = []
        for i in range(len(text)):
            one_text = np.expand_dims(text[i].cpu().numpy(),axis=0)
            text_feature = self.txt_session.run(["unnorm_text_features"], {"text":one_text})[0] # 未归一化的文本特征
            text_feature = torch.tensor(text_feature)
            text_features.append(text_feature)
        text_features = torch.squeeze(torch.stack(text_features),dim=1) # 特征向量stack到一起
        text_features = text_features / text_features.norm(dim=1, keepdim=True) # 归一化后的Chinese-CLIP文本特征，用于下游任务

        return text_features
        
        
if __name__ == '__main__':
    test_clip = CNCLIP("./models/cnclip_vit_l14_336.img.fp32.onnx", 
                       "./models/cnclip_vit_l14_336.txt.fp32.onnx",
                       "ViT-L-14-336")
    # image_features = test_clip.encode_image("./examples/pokemon.jpeg")
    image_features = test_clip.encode_image_url("https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg")
    text_features = test_clip.encode_text(["杰尼龟", "妙蛙种子", "小火龙", "皮卡丘", "树上有只鸟"])
    logits_per_image = get_similarity(image_features, text_features)
    print(logits_per_image)
    probs = logits_per_image.softmax(dim=-1)
    print(probs)
    image_features = test_clip.encode_image_path("./examples/pokemon.jpeg")
    logits_per_image = get_similarity(image_features, text_features)
    print(logits_per_image)
    probs = logits_per_image.softmax(dim=-1)
    print(probs)