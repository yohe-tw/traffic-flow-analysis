import numpy as np
import cv2 
import torch
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