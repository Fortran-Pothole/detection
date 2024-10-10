import cv2
from ultralytics import YOLO

# YOLO 모델 불러오기
model = YOLO('../clahe3canny.pt')

# GStreamer를 사용하여 카메라 스트림 받기 (libcamera와 함께 사용 가능)
cap = cv2.VideoCapture('libcamera-hello --stream')

while True:
    # 카메라로부터 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # YOLO 모델로 추론
    results = model(frame)

    # 결과에서 바운딩 박스 그리기
    for result in results.xyxy[0]:
        x1, y1, x2, y2, conf, class_id = result
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        label = f'Pothole {conf:.2f}'
        cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 결과 화면에 표시
    cv2.imshow('Pothole Detection', frame)

    # 'q'를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
