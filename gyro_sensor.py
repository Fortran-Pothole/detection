import smbus2
import time

# MPU6050 register addresses
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Initialize MPU6050 (wake up from sleep mode)
def init_mpu6050():
    try:
        bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)  # Wake up MPU6050
        print("MPU6050 initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize MPU6050: {e}")

# Function to read raw data from a 16-bit register
def read_word_2c(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

# Function to read gyroscope data for X axis and convert it to degrees/s
def read_gyro():
    gyro_x = read_word_2c(GYRO_XOUT_H)
    return gyro_x / 131.0  # Convert raw data to degrees/second

# Thresholds for jolt detection
MILD_JOLT_THRESHOLD = 50    # Level 1: Mild jolt
SEVERE_JOLT_THRESHOLD = 100  # Level 2: Severe jolt

# Initialize baseline gyro
baseline_gyro = 0

# Function to detect jolt based on gyroscope data
def detect_jolt():
    global baseline_gyro

    while True:
        # Read current gyroscope data
        current_gyro = read_gyro()

        # Calculate the change in gyroscope data
        delta_gyro = abs(current_gyro - baseline_gyro)

        # Detect level of jolt
        if delta_gyro > SEVERE_JOLT_THRESHOLD:
            print(f"Shaking a lot! {delta_gyro:.2f} degree/s")
        elif delta_gyro > MILD_JOLT_THRESHOLD:
            print(f"Shaking a little! {delta_gyro:.2f} degree/s")
        else:
            print(f"Shaking slightly more than before! {delta_gyro:.2f} degree/s")

        # Update baseline gyro using a simple moving average
        baseline_gyro = (baseline_gyro * 0.9) + (current_gyro * 0.1)

        # Add a small delay to avoid flooding the console
        time.sleep(0.1)

# Main function to initialize sensor and start jolt detection
if __name__ == "__main__":
    init_mpu6050()
    try:
        detect_jolt()
    except KeyboardInterrupt:
        print("Program terminated.")
