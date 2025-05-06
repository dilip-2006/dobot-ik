import cv2
import numpy as np
import json


# Load Homography Matrix (assumed you calibrated earlier and saved as 'cam_to_dobot_matrix.npy')
homography_matrix = np.load('cam_to_dobot_matrix.npy')

# Load taught colors from JSON file
with open('color d&t/taught_colors.json', 'r') as f:
    taught_colors = json.load(f)

# Open Camera (adjust index if needed)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Could not open camera.")
    exit()

# Storage for Detected Positions


print("📷 Press 's' to save cube position, 'q' to quit...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    # Resize and convert the frame to HSV for better color detection
    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Initialize mask for detection
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)

    # Iterate over the taught colors for detection
    for color_name, ranges in taught_colors.items():
        lower = np.array(ranges["lower"])
        upper = np.array(ranges["upper"])

        # Create mask for the color
        color_mask = cv2.inRange(hsv, lower, upper)
        color_mask = cv2.erode(color_mask, None, iterations=2)  # Clean the mask
        color_mask = cv2.dilate(color_mask, None, iterations=2)

        # Combine the current mask with the detected color mask
        mask = cv2.bitwise_or(mask, color_mask)

        # Find contours of the detected cubes
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:  # Only process large enough contours
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])  # Pixel center x
                    cy = int(M["m01"] / M["m00"])  # Pixel center y

                    # Draw center point on the frame for visualization
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                    cv2.putText(frame, f"{color_name}: ({cx}, {cy})", (cx + 10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                    # Handle the saving process on key press
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('s'):  # Press 's' to save
                        pixel_point = np.array([[[cx, cy]]], dtype='float32')
                        world_point = cv2.perspectiveTransform(pixel_point, homography_matrix)
                        x_dobot, y_dobot = world_point[0][0]

                        # Default Z (height) and R (rotation angle)
                        z_dobot = -26.0  # Set to the height you want for picking
                        r_dobot = 0.0    # Adjust rotation as needed

                        # Save detected data
                        cube_data = [round(float(x_dobot), 2), round(float(y_dobot), 2), z_dobot, r_dobot]
                        detected_data = cube_data
                        print(f"✅ Saved {color_name}: {cube_data}")

    # Show the current frame and mask
    cv2.imshow("Camera View", frame)
    cv2.imshow("Mask", mask)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save the detected positions as JSONs
with open('inverse/detected_positions.json', 'w') as f:
    json.dump(detected_data, f, indent=4)

cap.release()
cv2.destroyAllWindows()
print("📁 Detected positions saved as 'detected_positions.json'")