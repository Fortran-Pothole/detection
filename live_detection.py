import cv2
from ultralytics import YOLO

# YOLO 모델 불러오기
model = YOLO('clahe3canny.pt')  # .pt 파일 경로 입력

# 카메라에서 실시간 영상 스트림 받기
cap = cv2.VideoCapture(0)

while True:
    # 카메라로부터 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 모델로 추론
    results = model.predict(frame)  # 프레임을 입력하여 예측

    # 결과에서 바운딩 박스 그리기
    for result in results:
        x1, y1, x2, y2, conf, class_id = result  # 바운딩 박스 좌표와 클래스, 신뢰도 추출
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # 초록색 바운딩 박스
        label = f'Pothole {conf:.2f}'
        cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # 레이블

    # 결과 화면에 표시
    cv2.imshow('Pothole Detection', frame)

    # 'q'를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
