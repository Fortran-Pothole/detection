import smbus2
import time

# MPU6050 Registers and Address
MPU6050_ADDR = 0x68  # I2C address of the MPU-6050
PWR_MGMT_1 = 0x6B    # Power management register
GYRO_XOUT_H = 0x43   # Gyroscope X-axis high byte register
GYRO_YOUT_H = 0x45   # Gyroscope Y-axis high byte register
GYRO_ZOUT_H = 0x47   # Gyroscope Z-axis high byte register
GYRO_CONFIG = 0x1B   # Gyroscope configuration register

# Initialize I2C (SMBus)
bus = smbus2.SMBus(1)  # I2C bus number. Use 0 if necessary for your Pi

# Function to initialize MPU6050
def init_mpu6050():
    try:
        bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)  # Wake up the MPU-6050
        bus.write_byte_data(MPU6050_ADDR, GYRO_CONFIG, 0x00)  # Set gyro sensitivity to ±250°/s
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

# Function to read gyroscope data for X, Y, Z axes
def read_gyro():
    gyro_x = read_word_2c(GYRO_XOUT_H)
    gyro_y = read_word_2c(GYRO_YOUT_H)
    gyro_z = read_word_2c(GYRO_ZOUT_H)
    print(f"Gyro X: {gyro_x}, Gyro Y: {gyro_y}, Gyro Z: {gyro_z}")
    return gyro_x, gyro_y, gyro_z

# Function to detect jolts based on gyro readings
def detect_jolt():
    current_gyro = read_gyro()
    # You can add jolt detection logic here
    # For example, compare current_gyro values with previous values
    return current_gyro

# Main loop
def main():
    init_mpu6050()
    try:
        while True:
            detect_jolt()
            time.sleep(0.5)  # Delay to avoid flooding the console
    except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
    main()
