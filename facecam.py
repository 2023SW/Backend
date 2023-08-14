import cv2
import time

# 웹캠에서 영상을 읽어온다
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # WIDTH
cap.set(4, 480)  # HEIGHT

# 얼굴 인식 캐스케이드 파일 읽는다
face_cascade = cv2.CascadeClassifier('C:\\Users\\user\\workspace\\haarcascade_frontalface.xml')

# 인식 시간을 기록하기 위한 변수
last_recognition_time = time.time()

while True:
    # frame 별로 capture 한다
    ret, frame = cap.read()

    # 10초마다 얼굴을 인식한다
    if time.time() - last_recognition_time >= 10:
        last_recognition_time = time.time()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # 10초마다 인식된 얼굴 갯수를 출력
        print("Number of faces detected in the last 10 seconds:", len(faces))

        # 인식된 얼굴에 사각형을 출력한다
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 화면에 출력한다
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
