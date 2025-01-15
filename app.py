from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import threading
import time 
import os
from playsound import playsound
app = Flask(__name__)

model = YOLO('yolov8n.pt')

max_people = 5
alarm_playing = False

def play_alarm():
    global alarm_playing
    while alarm_playing:
        playsound(r'/Users/tc/Downloads/alert-109578.mp3', block=False)
        time.sleep(5) 

@app.route('/', methods=['GET', 'POST'])
def index():
    global max_people
    if request.method == 'POST':
        max_people = int(request.form.get('max_people'))
        return redirect(url_for('detection'))
    return render_template('index.html')

def generate_frames():
    global alarm_playing
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detections = results[0].boxes.data.numpy()

        person_count = sum(1 for detection in detections if int(detection[5]) == 0)

        for detection in detections:
            x1, y1, x2, y2, conf, cls = detection
            if int(cls) == 0:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        if person_count > max_people and not alarm_playing:
            alarm_playing = True
            threading.Thread(target=play_alarm).start()
            cv2.putText(frame, "OVERLOADED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.putText(frame, f"Count: {person_count}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

@app.route('/stop_alarm', methods=['POST'])
def stop_alarm():
    global alarm_playing
    alarm_playing = False
    return jsonify({"message": "Alarm stopped"})

@app.route('/detection')
def detection():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
