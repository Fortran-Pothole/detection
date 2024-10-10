import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
TRIG = 21
ECHO = 20

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# 타임아웃 값 설정 (초 단위)
TIMEOUT = 1

def get_ultrasonic_distance():
    # 초음파 신호 전송
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 마이크로초 동안 신호 전송
    GPIO.output(TRIG, False)

    # Echo 핀에서 신호가 들어오기 전까지 대기
    pulse_start = time.time()
    timeout_start = pulse_start
    
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start - timeout_start > TIMEOUT:
            print("Echo signal timeout")
            return None  # 타임아웃 발생 시 None 반환

    # Echo 핀에서 신호가 들어온 시점 기록
    pulse_end = time.time()
    timeout_end = pulse_end
    
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end - timeout_end > TIMEOUT:
            print("Echo signal timeout")
            return None  # 타임아웃 발생 시 None 반환

    # 초음파 신호가 돌아오는 시간 계산
    pulse_duration = pulse_end - pulse_start

    # 음속을 이용해 거리 계산 (cm)
    distance = pulse_duration * 17150
    return round(distance, 2)  # 소수점 두 자리까지 반올림

try:
    while True:
        dist = get_ultrasonic_distance()
        if dist is not None:
            print(f"Measured Distance = {dist} cm")
        else:
            print("Failed to measure distance")
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
