import smbus2
import time
import math

# MPU6050 레지스터 주소
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43

# I2C 버스 초기화
bus = smbus2.SMBus(1)

# MPU6050 전원 켜기
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

# 자이로 데이터 읽기 함수
def read_gyro():
    gyro_x = read_word_2c(GYRO_XOUT_H)
    return gyro_x / 131.0  # 각속도 (degree/s)로 변환

# 16-bit 두 바이트를 하나로 합쳐주는 함수
def read_word_2c(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr+1)
    val = (high << 8) + low
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

# 기준 설정
mild_jolt_threshold = 50  # 1번: 약한 덜컹 (각속도 변화 임계값)
severe_jolt_threshold = 100  # 2번: 심한 덜컹 (각속도 변화 임계값)
baseline_gyro = 0  # 초기 기준 각속도 (평균값으로 업데이트)

def detect_jolt():
    global baseline_gyro
    
    while True:
        # 자이로 데이터를 읽음
        current_gyro = read_gyro()
        
        # 평소의 기울기와 차이를 계산
        delta_gyro = abs(current_gyro - baseline_gyro)
        
        # 덜컹임 단계 감지
        if delta_gyro > severe_jolt_threshold:
            print(f"2번 심한 덜컹 감지! 변화량: {delta_gyro} degree/s")
        elif delta_gyro > mild_jolt_threshold:
            print(f"1번 약한 덜컹 감지! 변화량: {delta_gyro} degree/s")
        
        # 평소의 각속도를 업데이트 (단순 이동 평균)
        baseline_gyro = (baseline_gyro * 0.9) + (current_gyro * 0.1)
        
        # 약간의 지연
        time.sleep(0.1)

# 덜컹임 감지 실행
try:
    detect_jolt()
except KeyboardInterrupt:
    print("프로그램 종료")
