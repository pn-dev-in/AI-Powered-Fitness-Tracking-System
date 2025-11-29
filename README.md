# AI POWERED FITNESS TRACKING SYSTEM
An innovative web application built with Python and Computer Vision (CV) to provide real-time form correction and automated repetition counting using a webcam feed.

✨ Features
Real-time Pose Detection: Utilizes MediaPipe to track 33 key body landmarks.
10 Supported Exercises: Accurate tracking logic for a variety of workouts (Bicep Curl, Squat, Push Up, Tricep Extension, Shoulder Press, Forward Lunge, Deadlift, Leg Raise, Lateral Raise, Plank).
Live Form Feedback: Provides instant textual feedback (e.g., "FIX: Keep Back Straight") directly on the video screen.
Automated Rep Counting: Uses joint angle logic and a state machine to accurately count repetitions.
Performance Optimization: Employs frame skipping and processing downscaling to ensure a smooth, low-latency video stream.
Authentication & Persistence: User login/signup system with workout history logging to JSON files.
Visually Attractive UI: Full-screen video feed with prominent stats overlay and feedback banner.
🛠️ Technology Stack
Component	Technology	Role
Backend Framework	Python 3.x, Flask	Handles routing, API endpoints, and web serving.
Computer Vision	MediaPipe Pose	Provides the core Pose Estimation model.
Video Processing	OpenCV (cv2)	Manages webcam input, image manipulation, and streaming.
Production Server	Gunicorn	Required for robust production deployment (e.g., Heroku).
Frontend	HTML, CSS, JavaScript	Renders the interface and manages API communication.
Database	JSON Files	Simple persistence for user data and workout history.
🚀 Getting Started (Local Development)
The application must be run locally to access the computer vision features, as the remote server cannot access your webcam.

Prerequisites
You need Python 3.8+ installed on your system.

1. Clone the repository
git clone <repository-url>
cd ai-fitness-tracker
2. Set up a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies:

python -m venv venv
# Activate on Linux/macOS
source venv/bin/activate
# Activate on Windows
venv\Scripts\activate
3. Install Dependencies
Install all necessary packages, including Flask, MediaPipe, and OpenCV, from the requirements.txt file:

pip install -r requirements.txt
4. Run the Application
Start the Flask server:

python app.py
5. Access the App
Open your web browser and navigate to:

🌐 http://127.0.0.1:5000

(You can use the demo user: Email: demo@fit.com / Password: password)

💻 Code Structure & Highlights
The core logic resides in app.py, which integrates the web framework with the CV pipeline.

app.py Key Components
Component	Description	Highlight
generate_frames()	The primary function that captures video, runs pose detection, applies logic, and streams the output.	Optimization: Uses FRAME_SKIP_FACTOR = 3 and downscaling to reduce processing latency.
calculate_angle(a, b, c)	A utility function that converts landmark coordinates into a human-readable joint angle (in degrees).	Basis of Form Logic: Used to detect joint positions for rep counting and form checking.
Rep Counting Logic	A state machine using the global stage variable ("up" or "down") to track movement completion and increment rep_counter.	Accuracy: Ensures a full range of motion is achieved before a rep is counted.
API Endpoints	/set_exercise, /reset_workout, /video_feed	Persistence: /set_exercise and /reset_workout automatically call save_workout_session() to log data.
UI Overlay	OpenCV functions (cv2.putText, cv2.rectangle)	Live Feedback: The live stats, reps, and feedback banner are drawn directly onto the video frame by the backend for minimal latency.
Exercise List (10 Total)
The application supports tracking for the following exercises, each with its own specific angle logic:

Bicep Curl
Squat
Push Up
Tricep Extension
Shoulder Press
Forward Lunge
Deadlift
Leg Raise (Abs)
Lateral Raise
Plank (Time-based duration tracking)
☁️ Deployment (Heroku)
This application is designed to be deployed on Heroku, a Platform as a Service (PaaS). Netlify cannot be used as it is for static sites and cannot run a long-lived Python web server or access local hardware.

Heroku Deployment Steps
Dependencies: Ensure gunicorn is included in requirements.txt.
Procfile: The file contains the startup command: web: gunicorn app:app.
Security: Set the SECRET_KEY environment variable on Heroku's dashboard to secure user sessions.
Deployment: Connect your GitHub repository to Heroku for continuous deployment.
⚠️ IMPORTANT: Remote Webcam Access
Please note that when deployed remotely (e.g., on Heroku), the application cannot access your local computer's webcam (cv2.VideoCapture(0)). The real-time Computer Vision features are only functional when the application is running locally.

🤝 Contribution
Contributions are welcome! If you find a bug or have an idea for a new feature (e.g., adding more exercises, improving angle logic), please open an issue or submit a pull request.

<img width="1366" height="564" alt="image" src="https://github.com/user-attachments/assets/762b8e86-c9bb-47b6-9628-42ce32380801" />

<img width="1366" height="564" alt="image" src="https://github.com/user-attachments/assets/7947b0b1-b25d-44fd-af37-ddabebadcfc0" />

<img width="1364" height="579" alt="image" src="https://github.com/user-attachments/assets/e065c785-7f19-4264-b8f5-e9fb6b1ff091" />

<img width="1365" height="601" alt="image" src="https://github.com/user-attachments/assets/cccfaf87-6ac1-4855-ab98-c64fbf0a9892" />
