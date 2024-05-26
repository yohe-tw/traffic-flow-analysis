import numpy as np
import cv2 
from ultralytics import YOLO
import torch
from collections import defaultdict
import time
from crawl import jsondata


if torch.cuda.is_available():
    device = torch.device("cuda:0")
    print(f'GPU is available, using {torch.cuda.get_device_name(0)}.')
else:
    device = torch.device("cpu")
    print(f'GPU is unavailable, using cpu instead.')

# Making The Blank Image

data = jsondata.get_json_data(1, 0, 50)
url = data[0]["iphone_videourl"]
speed = data[0]["speed"]
pred_speed = []

cap = cv2.VideoCapture(url)
_, image = cap.read()


line = []


drawing = False
# Adding Function Attached To Mouse Callback
def draw(event,x,y,flags,params):
    global ix,iy,drawing
    # Left Mouse Button Down Pressed
    if(event==1):
        line.append((x, y))
        drawing = True
    if(event==0 and drawing):
        print("event4")
        image_cp = np.copy(image)
        cv2.line(image_cp, pt1=line[-1], pt2=(x, y), color=(255, 0, 0), thickness=2)
        cv2.imshow("Window",image_cp)
        cv2.waitKey(20)
    if(event==4):
        drawing = False
        line.append((x, y))
        cv2.line(image, pt1=line[-1], pt2=line[-2], color=(255, 0, 0), thickness=2)


cv2.namedWindow("Window")
cv2.setMouseCallback("Window",draw)
image_cp = np.copy(image)
cv2.imshow("Window",image_cp)
while len(line) < 4:
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()


def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)






showdata = np.full((100, 500, 3), 0.)
cv2.putText(img=showdata, text=f"avg_speed: {speed} km/hr", org=(0, 40), fontFace=0, fontScale=1, color=(0, 255, 0), thickness=2)
cv2.imshow("speed_predition", showdata)

def draw_speed(avg_speed, pred_speed):
    showdata = np.full((100, 500, 3), 0.)
    cv2.putText(img=showdata, text=f"avg_speed: {avg_speed} km/hr", org=(0, 40), fontFace=0, fontScale=1, color=(0, 255, 0), thickness=2)
    cv2.putText(img=showdata, text=f"pred_speed: {np.array(pred_speed).mean().astype('int')} km/hr", org=(0, 90), fontFace=0, fontScale=1, color=(0, 255, 0), thickness=2)
    cv2.imshow("speed_predition", showdata)

model = YOLO('yolov8m.pt')
track_history = {}
while True:
    #capture frame by frame
    ret, frame = cap.read()
    if not ret:
        cap = cv2.VideoCapture(url)
        continue
    results = model.track(frame, persist=True, device=device, classes=[2, 5, 7], verbose=False)# 2 - car, 5 - bus, 7 - trunk
    # print(results[0])
    boxes = results[0].boxes.xywh.cpu()
    classids = results[0].boxes.cls.int().cpu().tolist()
    annotated_frame = results[0].plot()
    cv2.line(annotated_frame, pt1=line[0], pt2=line[1], color=(0, 0, 255), thickness=2)
    cv2.line(annotated_frame, pt1=line[2], pt2=line[3], color=(255, 0, 0), thickness=2)
    if results[0].boxes.id == None:
        cv2.imshow('video', annotated_frame)
        cv2.waitKey(10)
        continue
    track_ids = results[0].boxes.id.int().cpu().tolist()
    
    for box, track_id, classids in zip(boxes, track_ids, classids):
        x, y, w, h = box
        if str(track_id) not in track_history:
            track_history[f"{track_id}"] = {"point" : [], "parse" : 0}
        track = track_history[f"{track_id}"]
        track["point"].append((float(x), float(y)))  # x, y center point
        if len(track["point"]) > 30:  # retain 90 tracks for 90 frames
            track["point"].pop(0)

        # Draw the tracking lines
        points = np.hstack(track["point"]).astype(np.int32).reshape((-1, 1, 2))
        cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 0), thickness=3)
        if len(track["point"]) > 1:
            if track["parse"] == 0: # detect if vehicle enter the first line
                if intersect(track["point"][-1], track["point"][-2], line[0], line[1]):
                    print(f"intersect1: {track_id}")
                    track["parse"] = time.time()
            elif track["parse"] == -1: # stop detect
                pass
            else: # detect if vehicle enter the second line
                if intersect(track["point"][-1], track["point"][-2], line[2], line[3]):
                    print(f"intersect2: {track_id}")
                    pred_speed.append(18 / (time.time() - track['parse']))
                    print(f"velosity: {pred_speed[-1]} km/hr")
                    if pred_speed[-1] > 120:
                        pred_speed.pop()
                        pass
                    track["parse"] = -1
                    draw_speed(speed, pred_speed)
    
    
    
    cv2.imshow('video', annotated_frame)
    cv2.waitKey(10)
