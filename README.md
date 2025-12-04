# 🤖 Dobot IK — Camera-to-Robot Coordinate Mapping using Homography Matrix

This repository implements a **complete inverse kinematics (IK) solver for the Dobot Magician**, with a system that **matches camera pixel coordinates to robot coordinates** using a **homography transformation**.

The goal is to enable the Dobot to **interact with objects detected by a camera** by converting their **image-plane location** into **real-world robotic workspace coordinates**, and then computing **joint angles using IK** to reach them.

---

## 🎯 Core Objectives

✔ Establish a mapping between **camera pixels → Dobot workspace coordinates**  
✔ Implement **inverse kinematics** for the Dobot Magician  
✔ Allow the robot to **reach objects tracked via computer vision**  
✔ Maintain **precision during pick-and-place tasks** without manual calibration

---

## 🔍 How It Works

### 1️⃣ Camera Coordinate Recognition  
A camera detects an object and extracts its **pixel location `(u, v)`**.

### 2️⃣ Homography Matrix Transformation  
Using perspective transformation, `(u, v)` is converted to **Dobot coordinate space (x, y)**:


The homography matrix **H** is calibrated using reference points from the workspace.

### 3️⃣ Inverse Kinematics (IK)  
With the target position known, the Dobot’s **joint angles (θ1, θ2, θ3...)** are computed to reach the point safely while respecting link constraints.

### 4️⃣ Robot Execution  
The computed joints are sent as robot commands for final placement or grasping action.

---

## 🧠 Key Features

| Capability | Description |
|-----------|-------------|
| Homography Calibration | Maps camera pixels to real-world Dobot workspace coordinates |
| Forward & Inverse Kinematics | Full IK pipeline for precise target positioning |
| Camera-to-Robot Sync | Automatic pose correction from detected object to reachable coordinates |
| High Accuracy | Reduces manual alignment and improves repeatability |
| Modular Code | Easy to expand for grasping, sorting or AI vision apps |

---

## 🚀 Applications

This repository is designed for robotics & automation research involving:

- Object pick-and-place using vision
- Color/shape-based sorting
- Human–robot interaction demos
- Autonomous tabletop manipulation
- Robo-lab educational experiments

---

## 🧩 Requirements

- Python
- OpenCV (camera coordinate extraction)
- Dobot SDK / serial API
- Numpy (matrix operations)
- Calibrated workspace reference points

---

## 🤝 Contribution

Issues, improvements and discussions are welcome.  
If you implement support for additional robot arms or perception modules, feel free to open a PR.

---

## 👤 Author

**Dilip Kumar S**  
📧 `letsmaildilip@gmail.com`  
🔗 GitHub: `https://github.com/dilip-2006`

If this work was helpful for your robotics journey,  
⭐ **Star the repository to support continued development!**
