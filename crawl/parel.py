import requests
import json
import cv2
import numpy as np
from tqdm import tqdm
from jsondata import get_json_data

highwayid = 1
route = (0, 10000)
fps = 10.0

data = get_json_data(highwayid, route[0], route[1])
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

for each in data:

    url = each["iphone_videourl"]
    each["cap"] = cv2.VideoCapture(url)
    
    if not each["cap"].isOpened():
        print("Cannot open camera")
        exit()
    ret, frame = each["cap"].read()   
    if ret:
        w = frame.shape[1]   
        h = frame.shape[0]   
        each["mp4"] = cv2.VideoWriter(f'./video/{each["web_title"]}-speed-{each["speed"]}.mp4', fourcc, fps, (w, h))
    else:
        break


while True:
    for each in data:
        ret, frame = each["cap"].read()    
        if ret: 
            each["mp4"].write(frame)
        else:
            each["mp4"] = cv2.VideoWriter(f'./video/{each["web_title"]}.mp4', fourcc, fps, (w, h))
            break
        
        # key = cv2.waitKey(100)
    
    