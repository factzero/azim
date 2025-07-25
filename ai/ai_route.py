# -*- coding: utf-8 -*-
import yaml
from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from search_clip import CNCLIP, get_similarity


ai_router = APIRouter(prefix="/ai", tags=["AI Operation"])

with open("ai_config.yaml", "r") as f:
    config = yaml.safe_load(f)
    
img_feature_cfg = config["Image_feature"]

ai_clip = CNCLIP(img_feature_cfg["img_mode_path"], img_feature_cfg["txt_mode_path"], img_feature_cfg["model_arch"])

class ImgInput(BaseModel):
    url: Optional[str] = None
    path: Optional[str] = None


class TextInput(BaseModel):
    txt: str
    

class FeaturesInput(BaseModel):
    feature1: list
    feature2: list


import time

@ai_router.post("/img_feature")
async def encode_image(input: ImgInput):
    print("img_feature: ", input.url, input.path)
    start_time = time.perf_counter()
    if input.url:
        img_feature = ai_clip.encode_image_url(input.url)
    elif input.path:
        img_feature = ai_clip.encode_image_path(input.path)
    else:
        print("img_feature: no url or path")
    elapsed_time = (time.perf_counter() - start_time)  # in seconds
    
    print(f"Time taken to encode image: {elapsed_time:.2f} s")
    
    return {"feature": img_feature.tolist()}


@ai_router.post("/txt_feature")
async def encode_image(input: TextInput):
    print("txt_feature: ", input.txt)
    txt_feature = ai_clip.encode_text(input.txt)
    return {"feature": txt_feature.tolist()}


@ai_router.post("/get_similarity")
async def encode_image(input: FeaturesInput):
    sim = get_similarity(input.feature1, input.feature2)
    print("get_similarity: ", sim)
    
    return {"sim": sim.item()/100.0}