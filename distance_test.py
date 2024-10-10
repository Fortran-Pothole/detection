import RPi.GPIO as GPIO
import time

# 핀 번호 설정 (TRIG와 ECHO는 각자 연결된 핀 번호로 변경하세요)
TRIG = 23  # Trigger 핀
ECHO = 24  # Echo 핀

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# 초음파 거리 측정 함수
def get_ultrasonic_distance():
    # Trigger를 짧게 HIGH 상태로 유지하여 초음파 신호 전송
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 마이크로초 유지
    GPIO.output(TRIG, False)

    # Echo 핀에서 신호가 돌아올 때까지 대기
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # 초음파가 돌아오는 시간 계산
    pulse_duration = pulse_end - pulse_start

    # 초음파 신호를 통해 거리 계산 (음속 34300 cm/s 사용)
    distance = pulse_duration * 17150
    distance = round(distance, 2)  # 소수점 두 자리까지 반올림

    return distance

try:
    while True:
        dist = get_ultrasonic_distance()
        print(f"Measured Distance = {dist} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
