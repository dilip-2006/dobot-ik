# © 2025 Dilip Kumar S and Gokul S. All Rights Reserved.
# Authors: Dilip Kumar S , Gokul S

import cv2
import numpy as np
import json

# Load Homography Matrix
homography_matrix = np.load('cam_to_dobot_matrix.npy')

# Load taught colors
with open('color d&t/taught_colors.json', 'r') as f:
    taught_colors = json.load(f)

# Initialize video
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Could not open camera.")
    exit()

# Read a single frame
ret, frame = cap.read()
cap.release()
cv2.destroyAllWindows()

if not ret:
    print("❌ Failed to grab frame")
    exit()

frame = cv2.resize(frame, (640, 480))
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

detected_objects = []

for color_name, ranges in taught_colors.items():
    lower = np.array(ranges["lower"])
    upper = np.array(ranges["upper"])

    color_mask = cv2.inRange(hsv, lower, upper)
    color_mask = cv2.erode(color_mask, None, iterations=2)
    color_mask = cv2.dilate(color_mask, None, iterations=2)

    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for idx, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 500:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                pixel_point = np.array([[[cx, cy]]], dtype='float32')
                world_point = cv2.perspectiveTransform(pixel_point, homography_matrix)
                x_dobot, y_dobot = world_point[0][0]

                label = f"{color_name}{idx + 1}"  # e.g., b1, b2, g1, etc.
                object_data = {
                    "color": color_name,
                    "label": label,
                    "x": round(float(x_dobot), 2),
                    "y": round(float(y_dobot), 2),
                    "z": -26.0,
                    "r": 0.0
                }

                detected_objects.append(object_data)
                print(f"✅ Detected {label}: (x={object_data['x']}, y={object_data['y']})")

# Save to JSON
if detected_objects:
    with open('inverse/detected_positions.json', 'w') as f:
        json.dump(detected_objects, f, indent=4)
    print(f"📁 Saved {len(detected_objects)} object(s) to 'detected_positions.json'")
else:
    print("⚠️ No objects detected.")

print("👋 Done.")
