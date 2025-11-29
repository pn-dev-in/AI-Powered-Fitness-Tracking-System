from flask import Flask, render_template, Response, request, jsonify, redirect, url_for, session
import cv2
import mediapipe as mp
import numpy as np
import time
import json
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secure_fitness_tracker_key_2025' # REQUIRED for sessions/login

# ---------------- File Persistence Setup ----------------
USER_DATA_FILE = 'users.json'
HISTORY_FILE = 'workout_history.json'
USERS = {} # Will be loaded in main

def load_user_data():
    """Loads all user data from the JSON file."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_user_data(users):
    """Saves the current dictionary of users back to the JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# ---------------- Mediapipe setup ----------------
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose_model = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# ---------------- Global variables ----------------
current_exercise = "none"
rep_counter = 0
stage = None
form_feedback = "SELECT AN EXERCISE"
session_start_time = None
calories_burned = 0.0

# Exercise configurations (10 EXERCISES)
EXERCISE_CONFIG = {
    "bicep_curl": {"name": "Bicep Curl", "calories_per_rep": 0.5},
    "squat": {"name": "Squat", "calories_per_rep": 1.2},
    "pushup": {"name": "Push Up", "calories_per_rep": 1.0},
    "tricep_ext": {"name": "Tricep Ext.", "calories_per_rep": 0.6},
    "shoulder_press": {"name": "Shoulder Press", "calories_per_rep": 0.8},
    "lunge": {"name": "Forward Lunge", "calories_per_rep": 1.0},
    "deadlift": {"name": "Deadlift", "calories_per_rep": 1.5},
    "leg_raise": {"name": "Leg Raise (Abs)", "calories_per_rep": 0.7},
    "lateral_raise": {"name": "Lateral Raise", "calories_per_rep": 0.4},
    "plank": {"name": "Plank (Time)", "calories_per_rep": 0.0}
}

# ---------------- Utility functions ----------------
def calculate_angle(a, b, c):
    """Calculates angle (in degrees) between three 2D points."""
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180 else angle

def load_workout_history():
    """Loads history from JSON file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try: return json.load(f)
            except json.JSONDecodeError: return []
    return []

def save_workout_session():
    """Save current session to history file."""
    global rep_counter, current_exercise, calories_burned
    
    if rep_counter > 0 and current_exercise != "plank":
        is_valid_session = True
    elif current_exercise == "plank" and get_session_duration() >= 15:
        is_valid_session = True
    else:
        return False
    
    if is_valid_session:
        session_data = {
            "exercise": current_exercise,
            "reps": rep_counter,
            "calories": round(calories_burned, 2),
            "duration": get_session_duration(),
            "timestamp": datetime.now().isoformat()
        }
        history = load_workout_history()
        history.insert(0, session_data)
        
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump(history, f, indent=4)
        except:
            pass
        return True
    return False

def get_session_duration():
    """Calculate session duration in seconds"""
    if session_start_time:
        return int(time.time() - session_start_time)
    return 0

def calculate_calories():
    """Calculate calories burned based on exercise and reps/time"""
    global calories_burned, rep_counter, current_exercise
    if current_exercise == "plank":
        duration_seconds = get_session_duration()
        calories_burned = (duration_seconds // 10) * 0.1
    elif current_exercise in EXERCISE_CONFIG:
        calories_burned = rep_counter * EXERCISE_CONFIG[current_exercise]["calories_per_rep"]
    return calories_burned

# ---------------- Authentication Decorator ----------------
def login_required(f):
    """Decorator to protect routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('signin'))
        return f(*args, **kwargs)
    return decorated_function


# ---------------- Video Generator (PERFORMANCE OPTIMIZED) ----------------
def generate_frames():
    global current_exercise, rep_counter, stage, form_feedback, session_start_time, calories_burned
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened(): return

    # Set high resolution for the output stream
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # --- Performance Optimization Variables ---
    FRAME_SKIP_FACTOR = 3 # Process MediaPipe every 3rd frame
    frame_counter = 0
    last_results = None 
    landmarks = None # Most recently computed landmarks

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            success, frame = cap.read()
            if not success: break
            
            frame_counter += 1
            height, width, _ = frame.shape
            
            # --- 1. PERFORMANCE OPTIMIZATION (MediaPipe Processing) ---
            if frame_counter % FRAME_SKIP_FACTOR == 0:
                # Resize for much faster processing (640x360 is common low-res processing size)
                process_frame = cv2.resize(frame, (640, 360))
                
                image_rgb = cv2.cvtColor(process_frame, cv2.COLOR_BGR2RGB)
                image_rgb.flags.writeable = False
                results = pose.process(image_rgb)
                image_rgb.flags.writeable = True
                
                last_results = results # Cache the results for use on all frames
                
            # Use cached landmarks for drawing and logic on every frame
            if last_results and last_results.pose_landmarks:
                landmarks = last_results.pose_landmarks.landmark
            else:
                landmarks = None # No landmarks available

            # --- 2. DRAWING (on the original full-resolution frame) ---
            if landmarks:
                # Draw landmarks using the cached results
                mp_drawing.draw_landmarks(frame, last_results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                          mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                          mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

            # --- 3. EXERCISE LOGIC (Runs on every frame for responsive reps) ---
            try:
                if landmarks and current_exercise != "none":
                    
                    # --- Get Key Coordinates ---
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]


                    if current_exercise == 'bicep_curl':
                        bicep_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                        shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
                        
                        if shoulder_angle > 45: form_feedback = "FIX: Keep Elbow Close"
                        else:
                            form_feedback = "CORRECT"
                            if bicep_angle > 160: stage = "down"
                            if bicep_angle < 30 and stage == "down":
                                stage = "up"
                                rep_counter += 1
                                calculate_calories()

                    elif current_exercise == 'squat':
                        knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                        back_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                        
                        if back_angle < 150: form_feedback = "FIX: Keep Back Straight"
                        else:
                            form_feedback = "CORRECT"
                            if knee_angle > 160: stage = "up"
                            if knee_angle < 90 and stage == "up":
                                stage = "down"
                                rep_counter += 1
                                calculate_calories()

                    elif current_exercise == 'pushup':
                        elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                        body_angle = calculate_angle(left_shoulder, left_hip, left_ankle)
                        
                        if body_angle < 160: form_feedback = "FIX: Keep Body Straight"
                        else:
                            form_feedback = "CORRECT"
                            if elbow_angle > 160: stage = "up"
                            if elbow_angle < 90 and stage == "up":
                                stage = "down"
                                rep_counter += 1
                                calculate_calories()

                    elif current_exercise == 'tricep_ext':
                        tricep_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
                        elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                        
                        if tricep_angle > 50: form_feedback = "FIX: Raise Elbows Higher"
                        else:
                            form_feedback = "CORRECT"
                            if elbow_angle > 160: stage = "up"
                            if elbow_angle < 90 and stage == "up":
                                stage = "down"
                                rep_counter += 1
                                calculate_calories()
                    
                    elif current_exercise == 'shoulder_press':
                        elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                        
                        if elbow_angle < 90: form_feedback = "FIX: Too Low"
                        else:
                            form_feedback = "CORRECT"
                            if elbow_angle < 100: stage = "down"
                            if elbow_angle > 160 and stage == "down":
                                stage = "up"
                                rep_counter += 1
                                calculate_calories()

                    elif current_exercise == 'lunge':
                        front_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                        
                        if front_knee_angle > 160: stage = "up"
                        if front_knee_angle < 100 and stage == "up":
                            stage = "down"
                            rep_counter += 1
                            calculate_calories()
                            form_feedback = "CORRECT"
                        else:
                            form_feedback = "FIX: Lower deeper (Knee to 90)"

                    elif current_exercise == 'deadlift':
                        hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                        
                        if hip_angle > 160: stage = "up"
                        if hip_angle < 100 and stage == "up":
                            stage = "down"
                            rep_counter += 1
                            calculate_calories()
                            form_feedback = "CORRECT"
                        else:
                            form_feedback = "FIX: Hinge at the hip"
                    
                    elif current_exercise == 'leg_raise':
                        hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                        
                        if hip_angle > 160: stage = "down"
                        if hip_angle < 100 and stage == "down":
                            stage = "up"
                            rep_counter += 1
                            calculate_calories()
                            form_feedback = "CORRECT"
                        else:
                            form_feedback = "FIX: Control the lift"

                    elif current_exercise == 'lateral_raise':
                        elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                        
                        if elbow_angle < 160: form_feedback = "FIX: Straighten Arm"
                        else:
                            if left_wrist[1] < left_shoulder[1] - 0.15: 
                                stage = "up"
                                form_feedback = "CORRECT"
                            if left_wrist[1] > left_shoulder[1] - 0.05 and stage == "up": 
                                stage = "down"
                                rep_counter += 1
                                calculate_calories()
                    
                    elif current_exercise == 'plank':
                        body_angle = calculate_angle(left_shoulder, left_hip, left_ankle)
                        calculate_calories()
                        
                        if body_angle < 160: form_feedback = "FIX: Keep Body Straight (Plank)"
                        else: form_feedback = "HOLD STEADY"
                        rep_counter = get_session_duration()

                elif current_exercise != "none":
                    form_feedback = "POSITION: Ensure full body is visible"
                
            except Exception as e:
                # This catches errors if landmarks are partially detected or corrupted
                form_feedback = "Place entire body in view"
                
            # --- 4. UI OVERLAY (Draw on the original frame) ---
            
            # 1. Semi-transparent black overlay for stats background (top-left)
            cv2.rectangle(frame, (0, 0), (int(width*0.35), int(height*0.25)), (20, 20, 20), -1)
            
            # 2. Top-Left Stats
            TEXT_Y = 40
            cv2.putText(frame, f'EXERCISE: {EXERCISE_CONFIG.get(current_exercise, {"name": "NONE"})["name"].upper()}', (15, TEXT_Y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            cv2.putText(frame, f'REPS/TIME: {rep_counter}', (15, TEXT_Y + 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            cv2.putText(frame, f'CALORIES: {calories_burned:.1f}', (15, TEXT_Y + 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 215, 0), 2)
            
            # 3. Top-Right Time
            duration = get_session_duration()
            mins = duration // 60
            secs = duration % 60
            cv2.putText(frame, f'TIME: {mins:02d}:{secs:02d}', (width-180, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # 4. Large Bottom Feedback Banner
            cv2.rectangle(frame, (0, height - 80), (width, height), (20, 20, 20), -1)
            
            feedback_color = (0, 255, 0) if form_feedback == "CORRECT" or form_feedback == "HOLD STEADY" else (0, 0, 255)
            
            (text_w, text_h), _ = cv2.getTextSize(form_feedback, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            text_x = int((width - text_w) / 2)
            text_y = height - 30 
            
            cv2.putText(frame, form_feedback, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, feedback_color, 2)

            # Encode frame for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

# ---------------- Flask Routes (Authentication & Main) ----------------

@app.route('/')
def index():
    return redirect(url_for('signin')) if 'user' not in session else redirect(url_for('dashboard'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if email in USERS:
            return render_template('signup.html', error="Email already registered. Please sign in.")
        
        USERS[email] = {"name": name, "password": password}
        save_user_data(USERS) 

        session['user'] = {"name": name, "email": email}
        return redirect(url_for('dashboard'))
        
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = USERS.get(email)
        
        if user and user['password'] == password:
            session['user'] = {"name": user['name'], "email": email}
            return redirect(url_for('dashboard'))
        
        return render_template('signin.html', error="Invalid email or password.")
        
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('signin'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session.get('user'))

@app.route('/planner')
@login_required
def planner():
    return render_template("planner.html", user=session.get('user'))

@app.route('/workout')
@login_required
def workout():
    exercises = [{"key": k, "name": v["name"]} for k, v in EXERCISE_CONFIG.items()]
    return render_template('workout.html', exercises=exercises)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# ---------------- API Endpoints ----------------

@app.route('/set_exercise', methods=['POST'])
@login_required
def set_exercise():
    global current_exercise, rep_counter, stage, form_feedback, session_start_time, calories_burned
    
    if current_exercise != "none":
        save_workout_session()
    
    current_exercise = request.form['exercise']
    rep_counter = 0
    stage = None
    calories_burned = 0.0
    session_start_time = time.time()
    form_feedback = "START YOUR WORKOUT" if current_exercise != "plank" else "HOLD POSITION"
    
    return jsonify({
        'status': 'success',
        'exercise': current_exercise,
        'message': f'Started {current_exercise}'
    })

@app.route('/get_stats')
@login_required
def get_stats():
    duration = get_session_duration()
    return jsonify({
        'exercise': current_exercise,
        'reps': rep_counter,
        'calories': round(calories_burned, 2),
        'duration': duration,
        'form_feedback': form_feedback,
        'stage': stage
    })

@app.route('/reset_workout', methods=['POST'])
@login_required
def reset_workout():
    global rep_counter, stage, calories_burned, session_start_time, current_exercise, form_feedback
    
    if current_exercise != "none":
        save_workout_session()
    
    current_exercise = "none"
    rep_counter = 0
    stage = None
    calories_burned = 0.0
    session_start_time = None
    form_feedback = "SELECT AN EXERCISE"

    return jsonify({'status': 'reset', 'reps': 0})

@app.route('/get_history')
@login_required
def get_history():
    history = load_workout_history()
    return jsonify(history)

@app.route('/get_full_report')
@login_required
def get_full_report():
    
    history_list = load_workout_history()

    total_reps = sum(item.get('reps', 0) for item in history_list if item.get('exercise') != 'plank')
    total_calories = sum(item.get('calories', 0.0) for item in history_list)
    
    focus_counts = {}
    for item in history_list:
        focus = item.get('exercise', 'Unknown')
        focus_counts[focus] = focus_counts.get(focus, 0) + 1
        
    most_frequent = max(focus_counts, key=focus_counts.get) if focus_counts else "None"

    report_data = {
        "user_name": session['user']['name'],
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "total_sessions": len(history_list),
        "total_reps": total_reps,
        "total_calories": round(total_calories, 2),
        "most_frequent_exercise": most_frequent,
        "detailed_history": history_list 
    }
    
    return jsonify(report_data)


# ---------------- Run ----------------
if __name__ == '__main__':
    USERS = load_user_data() 
    
    if not USERS:
        print("Creating demo user: demo@fit.com / password")
        USERS["demo@fit.com"] = {"name": "Demo User", "password": "password"}
        save_user_data(USERS)
        
    app.run(debug=True, threaded=True)