import math

# Camera parameters
CAMERA_FOV_HORIZONTAL = 75  # Camera horizontal field of view (in degrees)
IMAGE_WIDTH = 640  # Width of the image in pixels
IMAGE_HEIGHT = 480  # Height of the image in pixels

# Ultrasonic sensor distance to the pothole (in meters)
def get_ultrasonic_distance():
    # This function should return the distance measured by the ultrasonic sensor
    # Placeholder for the actual sensor reading
    return 1.5  # Example: 1.5 meters (replace with actual sensor reading)

# Calculate the real-world size of the pothole using bounding box and distance
def calculate_pothole_size(bbox, ultrasonic_distance):
    # Bounding box coordinates (x1, y1, x2, y2)
    x1, y1, x2, y2 = bbox
    
    # Pothole width and height in pixels
    bbox_width_px = x2 - x1
    bbox_height_px = y2 - y1

    # Convert FOV to radians
    fov_horizontal_rad = math.radians(CAMERA_FOV_HORIZONTAL)
    
    # Calculate the real-world width of the pothole
    real_width = 2 * ultrasonic_distance * math.tan(fov_horizontal_rad / 2) * (bbox_width_px / IMAGE_WIDTH)
    
    # Assuming the same logic for height based on a fixed field of view
    real_height = 2 * ultrasonic_distance * math.tan(fov_horizontal_rad / 2) * (bbox_height_px / IMAGE_HEIGHT)
    
    return real_width, real_height

# Example usage
bbox = (100, 150, 300, 350)  # Example bounding box coordinates from YOLO (x1, y1, x2, y2)
ultrasonic_distance = get_ultrasonic_distance()  # Get the sensor distance to the pothole

# Calculate real-world pothole dimensions
pothole_width, pothole_height = calculate_pothole_size(bbox, ultrasonic_distance)

print(f"Pothole real-world width: {pothole_width:.2f} meters")
print(f"Pothole real-world height: {pothole_height:.2f} meters")
