import requests
import json
import cv2
import numpy as np
from tqdm import tqdm

highwayid = 1
route = (0, 10000)
fps = 10.0


res = requests.get('https://1968.freeway.gov.tw/api/getRoadInformation', params={'action': "roadinfo", 'freewayid': highwayid,'from_milepost': route[0],'end_milepost': route[1], 'cctv' : True})
# print(res.json())

data = res.json()
cctv = data["response"]["cctv"]
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

for each in cctv:

    url = each["iphone_videourl"]
    each["cap"] = cv2.VideoCapture(url)
    
    if not each["cap"].isOpened():
        print("Cannot open camera")
        exit()
    ret, frame = each["cap"].read()   
    if ret:
        w = frame.shape[1]   
        h = frame.shape[0]   
        each["mp4"] = cv2.VideoWriter(f'./video/{each["web_title"]}.mp4', fourcc, fps, (w, h))
    else:
        break


while True:
    for each in cctv:
        ret, frame = each["cap"].read()    
        if ret: 
            each["mp4"].write(frame)
        else:
            each["mp4"] = cv2.VideoWriter(f'./video/{each["web_title"]}.mp4', fourcc, fps, (w, h))
            break
        
        # key = cv2.waitKey(100)
    
    