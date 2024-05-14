import cv2
import time
url = 'https://cctvn.freeway.gov.tw/abs2mjpg/bmjpg?camera=91010'
cap = cv2.VideoCapture(url)
init = False     # 建立空影片只需一次，所以使用一個變數做判斷

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()      # 讀取影片的每一幀
    if ret:
        if not init:
            init = True          # 第一次先建立空影片
            w = frame.shape[1]   # 取得影片寬度
            h = frame.shape[0]   # 取得影片高度
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')   # 設定影片的格式為 MJPG
            out = cv2.VideoWriter('output.mp4', fourcc, 10.0, (w,  h))  # 產生空的影片，一秒 10 格
        out.write(frame)  # 寫入影片
        # print('ok')
    else:
        print("Cannot receive frame")   # 如果讀取錯誤，印出訊息
        cap = cv2.VideoCapture(url)
        continue
    key = cv2.waitKey(100)
    if key == ord('q'):                 # 每一毫秒更新一次，直到按下 q 結束
        break
    elif key == ord('a'):               # 按下 a 儲存當下影格
        cv2.imwrite(f'test{time.time_ns()}.jpg', frame)  # 存成 jpg，取得當下時間作為檔名
    # cv2.imshow('oxxostudio', frame)     # 如果讀取成功，顯示該幀的畫面

cap.release()                           # 所有作業都完成後，釋放資源
cv2.destroyAllWindows()                 # 結束所有視窗