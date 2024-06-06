import numpy as np
import cv2 
from ultralytics import YOLO
import torch
import time
from crawl import jsondata
from argparse import ArgumentParser
from draw import Drawline
import json

# check if gpu if available
def check_gpu():
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
        print(f'GPU is available, using {torch.cuda.get_device_name(0)}.')
    else:
        device = torch.device("cpu")
        print(f'GPU is unavailable, using cpu instead.')
    return device

def draw_speed(frame, avg_speed, pred_speed):
    frame = cv2.copyMakeBorder(frame, 50, 0, 0, 0, cv2.BORDER_CONSTANT, (0, 0, 0))
    cv2.putText(img=frame, text=f"avg_speed: {avg_speed} km/hr", org=(0, 20), fontFace=0, fontScale=0.5, color=(0, 255, 0), thickness=1)
    cv2.putText(img=frame, text=f"pred_speed: {np.array(pred_speed).mean().astype('int')} km/hr", org=(0, 45), fontFace=0, fontScale=0.5, color=(0, 255, 0), thickness=1)
    return frame
    

def write_json(output, data):
    with open(output, 'w') as file:
        json.dump(data, file, indent=4)

def read_json(output):
    with open(output, 'r') as file:
        return json.load(file)

def _parse_argument():
    parser = ArgumentParser()
    parser.add_argument("--videoshow", type=bool, default=True)
    parser.add_argument("--videosave", type=bool, default=True)
    parser.add_argument("--videosavedir", type=str, default="./")
    parser.add_argument("--jsonsave", type=bool, default=True)
    parser.add_argument("--jsonsavedir", type=str, default="./")
    parser.add_argument("--drawline", type=bool, default=True)
    args = parser.parse_args()
    return args

def predict_speed(args, data, device):
    url = data["iphone_videourl"]
    speed = data["speed"]
    pred_speed = [speed]

    cap = cv2.VideoCapture(url)
    _, image = cap.read()

    data = read_json('point_r.json')
    line = Drawline(url, data[url])
    
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
        line.paste_line(annotated_frame)
        if results[0].boxes.id == None:
            annotated_frame = draw_speed(annotated_frame, speed, pred_speed)
            cv2.imshow('video', annotated_frame)
            if cv2.waitKey(1) == ord('q'):
                break
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
                    if line.line_1_intersect(track["point"][-1], track["point"][-2]):
                        track["parse"] = time.time()
                elif track["parse"] == -1: # stop detect
                    pass
                else: # detect if vehicle enter the second line
                    if line.line_2_intersect(track["point"][-1], track["point"][-2]):
                        pred_speed.append(21.6 / (time.time() - track['parse']))
                        print(f"velosity: {pred_speed[-1]} km/hr", end="")
                        if abs(pred_speed[-1] - speed) > 40:
                            pred_speed.pop()
                            print(" out of speed threshold, delete...")
                            pass
                        print("")
                        if len(pred_speed) > 30:
                            pred_speed.pop(0)
                        track["parse"] = -1
        
        annotated_frame = draw_speed(annotated_frame, speed, pred_speed)
        cv2.imshow('video', annotated_frame)
        cv2.imwrite('video/output.png', annotated_frame)
        if cv2.waitKey(1) == ord('q'):
            break



def main():
    args = _parse_argument()
    device = check_gpu()
    datas = jsondata.get_json_data(1, 1800, 10000)
    datas.pop(3)
    datas.pop(3)
    datas.pop(3)
    print(len(datas))
    for data in datas:
        predict_speed(args, data, device)
    

if __name__ == "__main__":
    main()
