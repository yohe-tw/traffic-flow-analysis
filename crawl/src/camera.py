import cv2
# 來源串流網址
url = 'https://cctvn.freeway.gov.tw/abs2mjpg/bmjpg?camera=91010'
cap = cv2.VideoCapture(url)             # 讀取來源

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()             # 讀取影片的每一幀
    if not ret:
        print("Cannot receive frame")   # 如果讀取錯誤，印出訊息
        cap = cv2.VideoCapture(url)     # 有時候串流間隔時間較久會中斷，中斷時重新讀取
        continue
    cv2.imshow('oxxostudio', frame)     # 如果讀取成功，顯示該幀的畫面
    if cv2.waitKey(1) == ord('q'):      # 每一毫秒更新一次，直到按下 q 結束
        break
cap.release()                           # 所有作業都完成後，釋放資源
cv2.destroyAllWindows()                 # 結束所有視窗