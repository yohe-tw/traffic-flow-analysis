import numpy as np
import cv2 


class Drawline:
    def __init__(self, url : str, line : list):
        self.url = url
        self.line = line.copy()
        self.drawing = False
    def ccw(self,A,B,C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    # Return true if line segments AB and CD intersect
    def intersect(self, A, B, C, D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)
    
    def draw(self, event, x, y, flag, param):
        # Left Mouse Button Down Pressed
        if(event==1):
            self.line.append((x, y))
            self.drawing = True
        if(event==0 and self.drawing):
            image_cp = np.copy(self.image)
            cv2.line(image_cp, pt1=self.line[-1], pt2=(x, y), color=(255, 0, 0), thickness=2)
            cv2.imshow("Draw line",image_cp)
            cv2.waitKey(20)
        if(event==4):
            self.drawing = False
            self.line.append((x, y))
            cv2.line(self.image, pt1=self.line[-1], pt2=self.line[-2], color=(0, 0, 255), thickness=2)

    def start_draw(self, image):
        if len(self.line) == 4:
            print('already drew line.')
            return
        cv2.namedWindow("Draw line")
        cv2.setMouseCallback("Draw line",self.draw)
        image_cp = np.copy(image)
        self.image = image_cp
        cv2.imshow("Draw line",image_cp)
        while len(self.line) < 4:
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        return

    def line_1_intersect(self, A, B):
        return self.intersect(A, B, self.line[0], self.line[1])
    
    def line_2_intersect(self, A, B):
        return self.intersect(A, B, self.line[2], self.line[3])
    
    def paste_line(self, img):
        cv2.line(img, pt1=self.line[0], pt2=self.line[1], color=(0, 0, 255), thickness=2)
        cv2.line(img, pt1=self.line[2], pt2=self.line[3], color=(255, 0, 0), thickness=2)


    
