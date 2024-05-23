import requests
import json
import cv2
import numpy as np
from tqdm import tqdm
from jsondata import get_json_data

highwayid = 1
route = (0, 10000)

data = get_json_data(highwayid, route[0], route[1])

for each in tqdm(data):
    
    url = each["iphone_videourl"]
    cap = cv2.VideoCapture(url)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    init = False
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()             # 讀取影片的每一幀
        if ret:
            if not init:
                # print('init')
                init = True          
                w = frame.shape[1]   
                h = frame.shape[0]   
                mp4 = cv2.VideoWriter(f'./video/{each["web_title"]}-speed-{each["speed"]}.mp4', fourcc, 10.0, (w, h))
            mp4.write(frame)
        else:
            # print("Cannot receive frame")   # 如果讀取錯誤，印出訊息
            break
        
        key = cv2.waitKey(100)
    cap.release()
    