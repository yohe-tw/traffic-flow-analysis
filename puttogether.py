import numpy as np
import cv2 
from ultralytics import YOLO
import time
from crawl import jsondata
from argparse import ArgumentParser
from draw import Drawline
import util

def _parse_argument():
    parser = ArgumentParser()
    parser.add_argument("--jsonwritefile", type=str, default="point_w.json")
    parser.add_argument("--jsonreadfile", type=str, default="point_r.json")
    parser.add_argument("--drawline", type=bool, default=False)
    args = parser.parse_args()
    return args

def predict_speed(args, data, device):
    url = data["iphone_videourl"]
    speed = data["speed"]
    pred_speed = [speed]

    cap = cv2.VideoCapture(url)
    _, image = cap.read()

    
    
    return image
    
    



def main():
    args = _parse_argument()
    device = util.check_gpu()

    datas = jsondata.get_json_data(1, 0, 11000)

    datas = [datas[1], datas[9], datas[17]]

    print(f'check for {len(datas)} video')
    images = []
    grid_size = (3, 1)
    for data in datas:
        images.append(predict_speed(args, data, device))

    height, width, _ = images[0].shape
    
    # Create a new blank image with appropriate size
    grid_height = grid_size[1] * height
    grid_width = grid_size[0] * width
    grid_image = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)
    
    # Paste images into the grid
    for idx, img in enumerate(images):
        row = idx // grid_size[0]
        col = idx % grid_size[0]
        y_offset = row * height
        x_offset = col * width
        grid_image[y_offset:y_offset + height, x_offset:x_offset + width] = img
    cv2.imwrite('window.png', grid_image)
    
    

if __name__ == "__main__":
    main()
