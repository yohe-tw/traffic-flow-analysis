from ultralytics import YOLO
import cv2
import torch


if torch.cuda.is_available():
    device = torch.device("cuda:0")
    print(f'GPU is available, using {torch.cuda.get_device_name(0)}.')
else:
    device = torch.device("cpu")
    print(f'GPU is unavailable, using cpu instead.')


# capture video/ video path
cap = cv2.VideoCapture("https://cctvn.freeway.gov.tw/abs2mjpg/bmjpg?camera=10000")
model = YOLO('yolov8n.pt')

#read until video is completed
while True:
    #capture frame by frame
    ret, frame = cap.read()
    if not ret:
        cap = cv2.VideoCapture("https://cctvn.freeway.gov.tw/abs2mjpg/bmjpg?camera=10000")
        continue
    results = model.track(frame, persist=True, device=device)
    print(len(results))
    # print(result)
    # cv2.imshow('video', frame)
    #for r in results:
        #print(r.boxes)
    
    annotated_frame = results[0].plot()
    cv2.imshow('video', annotated_frame)
    cv2.waitKey(1)
    
    
