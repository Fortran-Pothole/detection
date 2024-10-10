import cv2
import numpy as np
from ultralytics import YOLO
from libcamera import CameraManager, Transform
import time

# 모델 로드 (이미 학습된 포트홀 탐지 모델을 로드합니다)
model = YOLO('pothole_detection_model.pt')

# 카메라 초기화 및 설정
def initialize_camera():
    camera_manager = CameraManager()
    cameras = camera_manager.cameras
    if not cameras:
        print("카메라를 찾을 수 없습니다.")
        return None
    camera = cameras[0]
    
    # 카메라 설정
    camera_config = camera.generate_configuration([libcamera.StreamRole.VideoRecording])
    stream_config = camera_config.at(0)
    stream_config.size.width = 1920
    stream_config.size.height = 1080
    stream_config.pixel_format = 'BGR888'
    
    camera.configure(camera_config)
    return camera

# 탐지된 포트홀에 사각형 그리기
def draw_bounding_boxes(frame, results):
    for result in results:
        # 탐지된 박스가 있으면 그리기
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # 좌표 변환
            conf = box.conf[0]  # 신뢰도
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 사각형 그리기
            cv2.putText(frame, f'Pothole {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 실시간 카메라 프레임 처리 및 모델 적용
def process_video():
    camera = initialize_camera()
    if camera is None:
        return

    camera.start()
    count = 0
    
    try:
        while True:
            frame = np.empty((camera.configuration.at(0).size.height, camera.configuration.at(0).size.width, 3), dtype=np.uint8)
            camera.capture_frame(frame)  # 프레임 캡처
            
            # YOLO 모델을 이용해 포트홀 탐지
            results = model.predict(frame)
            
            # 탐지된 포트홀에 사각형 그리기
            draw_bounding_boxes(frame, results)
            
            # 프레임 출력
            cv2.imshow('Pothole Detection', frame)
            
            # ESC 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == 27:
                break

            count += 1

    except KeyboardInterrupt:
        print("사용자에 의해 종료되었습니다.")
    finally:
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video()
