import smbus2
import time

# MPU6050 register addresses
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

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

# Function to read gyroscope data for X, Y, and Z axes and convert to degrees/s
def read_gyro():
    gyro_x = read_word_2c(GYRO_XOUT_H) / 131.0
    gyro_y = read_word_2c(GYRO_YOUT_H) / 131.0
    gyro_z = read_word_2c(GYRO_ZOUT_H) / 131.0
    return gyro_x, gyro_y, gyro_z

# Thresholds for jolt detection (less sensitive)
MILD_JOLT_THRESHOLD = 30    # Level 1: Mild jolt (increased sensitivity threshold)
SEVERE_JOLT_THRESHOLD = 60  # Level 2: Severe jolt (increased sensitivity threshold)

# Initialize baseline gyro values
baseline_gyro_x = 0
baseline_gyro_y = 0
baseline_gyro_z = 0

# Function to detect jolt based on gyroscope data
def detect_jolt():
    global baseline_gyro_x, baseline_gyro_y, baseline_gyro_z

    while True:
        # Read current gyroscope data for all three axes
        gyro_x, gyro_y, gyro_z = read_gyro()

        # Calculate the change in gyroscope data for each axis
        delta_gyro_x = abs(gyro_x - baseline_gyro_x)
        delta_gyro_y = abs(gyro_y - baseline_gyro_y)
        delta_gyro_z = abs(gyro_z - baseline_gyro_z)

        # Determine the largest delta across all axes
        max_delta = max(delta_gyro_x, delta_gyro_y, delta_gyro_z)

        # Detect level of jolt based on the largest delta
        if max_delta > SEVERE_JOLT_THRESHOLD:
            print(f"Shaking a lot! {max_delta:.2f} degree/s")
        elif max_delta > MILD_JOLT_THRESHOLD:
            print(f"Shaking a little! {max_delta:.2f} degree/s")

        # Update baseline gyros using a simple moving average
        baseline_gyro_x = (baseline_gyro_x * 0.9) + (gyro_x * 0.1)
        baseline_gyro_y = (baseline_gyro_y * 0.9) + (gyro_y * 0.1)
        baseline_gyro_z = (baseline_gyro_z * 0.9) + (gyro_z * 0.1)

        # Add a small delay to avoid flooding the console
        time.sleep(0.1)

# Main function to initialize sensor and start jolt detection
if __name__ == "__main__":
    init_mpu6050()
    try:
        detect_jolt()
    except KeyboardInterrupt:
        print("Program terminated.")
