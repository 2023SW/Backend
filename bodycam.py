import cv2

# 웹캠에서 영상을 읽어온다
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # WIDTH
cap.set(4, 480)  # HEIGHT

# 전신 인식 캐스케이드 파일 읽는다
body_cascade = cv2.CascadeClassifier('C:\\Users\\user\\workspace\\haarcascade_fullbody.xml')

while True:
    # frame 별로 capture 한다
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bodies = body_cascade.detectMultiScale(gray, 1.1, 3)

    # 인식된 전신 갯수를 출력
    print("Number of bodies detected:", len(bodies))

    # 인식된 전신에 사각형을 출력한다
    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 화면에 출력한다
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
