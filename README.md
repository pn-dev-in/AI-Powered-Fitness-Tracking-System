# AI Fitness Tracker (Computer Vision–Based Form Correction)

A real-time **computer vision system** that analyzes human pose through a webcam to **count exercise repetitions and provide corrective feedback** during workouts.  
The project focuses on **applied CV, motion analysis, and real-time performance**, not just library usage.

---

## 🔍 What This Project Demonstrates
- Applied computer vision using human pose estimation  
- Joint-angle computation and biomechanics-based logic  
- State-machine driven repetition counting  
- Real-time video processing with performance optimizations  
- End-to-end ML-integrated web application (CV + backend + UI)

---

## 📌 Overview
The AI Fitness Tracker uses **MediaPipe Pose** and **OpenCV** to track body landmarks, compute joint angles, and validate exercise form in real time.  
Only correctly performed movements are counted, and users receive **instant visual feedback** to reduce injury risk and improve workout quality.

This application is designed for **local execution**, where real-time computer vision can directly access webcam hardware.

---

## ✨ Key Features

### Pose & Motion Analysis
- 33-point human pose tracking using MediaPipe Pose  
- Joint-angle calculation for form validation and motion detection  

### Rep Counting & Feedback
- State-machine based repetition counting (up/down stages)  
- Live, on-screen corrective feedback for improper form  

### Performance Optimization
- Frame skipping to reduce computational load  
- Resolution downscaling for smooth, low-latency video streaming  

---

## ✔️ Supported Exercises (10)
- Bicep Curl  
- Squat  
- Push Up  
- Tricep Extension  
- Shoulder Press  
- Forward Lunge  
- Deadlift  
- Leg Raise (Abs)  
- Lateral Raise  
- Plank (time-based)

Each exercise uses **custom joint-angle thresholds and validation logic**.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|--------|-----------|--------|
| Backend | Python 3.x, Flask | Routing, APIs, session handling |
| Computer Vision | MediaPipe Pose | Human pose estimation |
| Video Processing | OpenCV (cv2) | Webcam capture & frame processing |
| Frontend | HTML, CSS, JavaScript | UI rendering & interaction |
| Data Storage | JSON Files | User and workout persistence |
| Production Server | Gunicorn | Application serving |

---

## 🚀 Getting Started (Local Development)

> ⚠️ **Important:**  
> This application must be run **locally** to access your webcam.  
> Remote servers cannot access local hardware.

### Prerequisites
- Python 3.8+
- Webcam

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/ai-fitness-tracker.git
cd ai-fitness-tracker
2️⃣ Set Up Virtual Environment
python -m venv venv
Activate:

Linux / macOS

source venv/bin/activate
Windows

venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run the Application
python app.py
5️⃣ Access the App
Open your browser:

http://127.0.0.1:5000
Demo Credentials

Email: demo@fit.com

Password: password

```
🧠 System Design & Core Logic
Core File: app.py

## 📷 Screenshots
![Login/Signup Page](https://github.com/user-attachments/assets/1daf0ed3-6a1d-4eb0-97ff-ed861cb4e622)

![Dashboard](https://github.com/user-attachments/assets/f789ccf4-b858-4f51-8f75-b3fef4263b80)

![Tracking Page](https://github.com/user-attachments/assets/f3ef0bca-13f3-4b8f-800b-29a3eb867a6b)

![Activity_Page](https://github.com/user-attachments/assets/74ceda3b-ca0c-476f-84ef-fed386d3e4b5)


Component	Description
generate_frames()	Captures webcam frames, runs pose detection, applies rep logic, and streams video
Optimization	Uses FRAME_SKIP_FACTOR = 3 and frame resizing for reduced latency
calculate_angle(a, b, c)	Computes joint angles (degrees) from pose landmarks
Rep Counting Logic	State machine using stage (up / down) to ensure valid repetitions
API Endpoints	/set_exercise, /reset_workout, /video_feed
UI Overlay	Rep count, feedback, and stats rendered directly on frames using OpenCV

🚀 Deployment Notes
This application can be deployed on platforms like Heroku (PaaS) for demonstration purposes.

Important limitation:
Remote deployments cannot access local webcams via:

cv2.VideoCapture(0)
As a result, all real-time computer vision functionality works only during local execution.

🎯 Intended Role Fit
Computer Vision Engineer (Entry-Level)

AI/ML Engineer (Applied Systems)

Software Engineer with ML integration

🤝 Contribution
Contributions are welcome:

Improve form validation logic

Add new exercises

Optimize performance

Fix bugs or refactor code

Feel free to open an issue or submit a pull request.

⚠️ Disclaimer
This project is intended for educational and experimental use.
It is not certified for medical, rehabilitation, or professional fitness applications.


