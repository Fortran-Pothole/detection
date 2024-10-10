import cv2
import numpy as np
from ultralytics import YOLO

# 모델 로드 (이미 학습된 포트홀 탐지 모델을 로드합니다)
model = YOLO('clahe3canny.pt')

# 탐지된 포트홀에 사각형 그리기
def draw_bounding_boxes(frame, results):
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # 좌표 변환
            conf = box.conf[0]  # 신뢰도
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 사각형 그리기
            cv2.putText(frame, f'Pothole {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 실시간 카메라 프레임 처리 및 모델 적용
def process_video():
    cap = cv2.VideoCapture(0)  # 카메라 장치 초기화 (0번 카메라 사용)
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()  # 프레임 읽기
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        # YOLO 모델을 이용해 포트홀 탐지
        results = model.predict(frame)

        # 탐지된 포트홀에 사각형 그리기
        draw_bounding_boxes(frame, results)

        # 결과 출력 (프레임에 포트홀 표시)
        cv2.imshow('Pothole Detection', frame)

        # ESC 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video()
