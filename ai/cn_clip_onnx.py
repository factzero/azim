# -*- coding: utf-8 -*-
import onnxruntime
from PIL import Image
import numpy as np
import torch
import cn_clip.clip as clip
from cn_clip.clip.utils import _MODEL_INFO, image_transform

# 载入ONNX图像侧模型（**请替换${DATAPATH}为实际的路径**）
img_sess_options = onnxruntime.SessionOptions()
img_run_options = onnxruntime.RunOptions()
img_run_options.log_severity_level = 2
img_onnx_model_path="./models/cnclip_vit_l14_336.img.fp32.onnx"
img_session = onnxruntime.InferenceSession(img_onnx_model_path,
                                        sess_options=img_sess_options)

# 预处理图片
model_arch = "ViT-L-14-336" # 这里我们使用的是ViT-L-14-336规模，其他规模请对应修改
preprocess = image_transform(_MODEL_INFO[model_arch]['input_resolution'])
# 示例皮卡丘图片，预处理后得到[1, 3, 分辨率, 分辨率]尺寸的Torch Tensor
image = preprocess(Image.open("examples/pokemon.jpeg")).unsqueeze(0)

# 用ONNX模型计算图像侧特征
image_features = img_session.run(["unnorm_image_features"], {"image": image.cpu().numpy()})[0] # 未归一化的图像特征
image_features = torch.tensor(image_features)
image_features /= image_features.norm(dim=-1, keepdim=True) # 归一化后的Chinese-CLIP图像特征，用于下游任务
print(image_features.shape) # Torch Tensor shape: [1, 特征向量维度]

# 载入ONNX文本侧模型（**请替换${DATAPATH}为实际的路径**）
txt_sess_options = onnxruntime.SessionOptions()
txt_run_options = onnxruntime.RunOptions()
txt_run_options.log_severity_level = 2
txt_onnx_model_path="./models/cnclip_vit_l14_336.txt.fp32.onnx"
txt_session = onnxruntime.InferenceSession(txt_onnx_model_path,
                                        sess_options=txt_sess_options)

# 为4条输入文本进行分词。序列长度指定为52，需要和转换ONNX模型时保持一致（参见转换时的context-length参数）
text = clip.tokenize(["杰尼龟", "妙蛙种子", "小火龙", "皮卡丘"], context_length=52) 

# 用ONNX模型依次计算文本侧特征
text_features = []
for i in range(len(text)):
    one_text = np.expand_dims(text[i].cpu().numpy(),axis=0)
    text_feature = txt_session.run(["unnorm_text_features"], {"text":one_text})[0] # 未归一化的文本特征
    text_feature = torch.tensor(text_feature)
    text_features.append(text_feature)
text_features = torch.squeeze(torch.stack(text_features),dim=1) # 4个特征向量stack到一起
text_features = text_features / text_features.norm(dim=1, keepdim=True) # 归一化后的Chinese-CLIP文本特征，用于下游任务
print(text_features.shape) # Torch Tensor shape: [4, 特征向量维度]

logits_per_image = 100 * image_features @ text_features.t()
probs = logits_per_image.softmax(dim=-1)    
print(probs) 