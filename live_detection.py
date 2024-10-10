from ultralytics import YOLO
import cv2

# YOLO 모델 로드
model = YOLO('../clahe3canny.pt')  # .pt 파일 경로

# libcamera로 캡처한 이미지 불러오기
image = cv2.imread('image.jpg')

# YOLO 모델로 이미지 추론
results = model(image)

# 바운딩 박스 그리기
for result in results.xyxy[0]:  # xyxy 좌표 형식
    x1, y1, x2, y2, conf, cls = result
    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    label = f'Pothole {conf:.2f}'
    cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 결과 이미지 출력
cv2.imshow('Pothole Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
