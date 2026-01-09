🏋️ AI Fitness Tracker – Real-Time Form Correction & Rep Counter

An innovative web-based fitness application built using Python and Computer Vision that provides real-time exercise form correction and automatic repetition counting through a webcam feed.
The system uses pose estimation and joint-angle analysis to track workouts accurately while delivering instant feedback to help users maintain proper form and reduce injury risk.

✨ Features

Real-Time Pose Detection
Tracks 33 human body landmarks using MediaPipe Pose.

10 Supported Exercises
Accurate rep counting and form logic for:

Bicep Curl

Squat

Push Up

Tricep Extension

Shoulder Press

Forward Lunge

Deadlift

Leg Raise (Abs)

Lateral Raise

Plank (time-based)

Live Form Feedback
Displays instant on-screen guidance such as:
“FIX: Keep Back Straight”

Automated Rep Counting
Uses joint-angle thresholds and a state-machine approach to ensure only valid reps are counted.

Performance Optimized
Frame skipping and resolution downscaling provide smooth, low-latency video streaming.

Authentication & Persistence
User signup/login with workout history stored in JSON files.

Visually Engaging UI
Full-screen webcam feed with overlayed stats, rep count, and feedback banner.

🛠️ Technology Stack
Component	Technology	Purpose
Backend	Python 3.x, Flask	Routing, APIs, session handling
Computer Vision	MediaPipe Pose	Human pose estimation
Video Processing	OpenCV (cv2)	Webcam capture & frame processing
Frontend	HTML, CSS, JavaScript	UI rendering & user interaction
Data Storage	JSON Files	User and workout persistence
Production Server	Gunicorn	Production deployment (Heroku)
🚀 Getting Started (Local Development)

⚠️ Important:
This application must be run locally to access your webcam. Remote servers cannot access local hardware.

Prerequisites

Python 3.8+

Webcam

1️⃣ Clone the Repository
git clone https://github.com/your-username/ai-fitness-tracker.git
cd ai-fitness-tracker

2️⃣ Set Up Virtual Environment
python -m venv venv


Activate the environment:

Linux / macOS

source venv/bin/activate


Windows

venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Application
python app.py

5️⃣ Access the App

Open your browser and visit:

🌐 http://127.0.0.1:5000

Demo Credentials

Email: demo@fit.com

Password: password

💻 Code Structure & Highlights
Core File: app.py
Component	Description
generate_frames()	Captures webcam frames, runs pose detection, applies rep logic, and streams video
Optimization	Uses FRAME_SKIP_FACTOR = 3 and frame resizing for reduced latency
calculate_angle(a, b, c)	Computes joint angles in degrees from landmark coordinates
Rep Counting Logic	State machine using stage (up / down) to ensure full motion
API Endpoints	/set_exercise, /reset_workout, /video_feed
UI Overlay	Stats and feedback rendered directly on frames using OpenCV
🏋️ Supported Exercises (10 Total)

Each exercise uses custom joint-angle thresholds for accuracy.

Bicep Curl

Squat

Push Up

Tricep Extension

Shoulder Press

Forward Lunge

Deadlift

Leg Raise

Lateral Raise

Plank (time-based)
Deployment (Heroku)

This application is deployable on Heroku (PaaS).

❌ Netlify is not supported — it cannot run Python servers or access hardware.

Deployment Requirements

gunicorn included in requirements.txt

Procfile:

web: gunicorn app:app


Set SECRET_KEY as an environment variable in Heroku

Deployment Method

Connect GitHub repository to Heroku

Enable automatic deployments

⚠️ Important Note on Webcam Access

When deployed remotely (e.g., on Heroku), the application cannot access your local webcam using:

cv2.VideoCapture(0)


✔️ All real-time Computer Vision features work only in local execution.

🤝 Contribution

Contributions are welcome!

Report bugs

Improve form logic

Add new exercises

Optimize performance

Feel free to open an issue or submit a pull request.

<img width="1366" height="564" alt="image" src="https://github.com/user-attachments/assets/762b8e86-c9bb-47b6-9628-42ce32380801" />

<img width="1366" height="564" alt="image" src="https://github.com/user-attachments/assets/7947b0b1-b25d-44fd-af37-ddabebadcfc0" />

<img width="1364" height="579" alt="image" src="https://github.com/user-attachments/assets/e065c785-7f19-4264-b8f5-e9fb6b1ff091" />

<img width="1365" height="601" alt="image" src="https://github.com/user-attachments/assets/cccfaf87-6ac1-4855-ab98-c64fbf0a9892" />
