import cv2
import numpy as np
from tqdm import tqdm
from jsondata import get_json_data
import os

highwayid = 1
route = (0, 5000)
fps, wait_time = 10.0, 100
fourcc = cv2.VideoWriter_fourcc(*'vp80')

data = get_json_data(highwayid, route[0], route[1])

if not os.path.exists('video'):
    os.makedirs('video')

for each in tqdm(data):
    
    url = each["iphone_videourl"]
    cap = cv2.VideoCapture(url)
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
                mp4 = cv2.VideoWriter(f'./video/{each["web_title"]}-speed-{each["speed"]}.webm', fourcc, fps, (w, h))
            mp4.write(frame)
        else:
            # print("Cannot receive frame")   # 如果讀取錯誤，印出訊息
            break
        
        key = cv2.waitKey(wait_time)
    cap.release()
    