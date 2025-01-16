# Person Detection and Overcrowding Alarm System

This Flask application uses the YOLOv8 object detection model to monitor a live video feed from a webcam and detect the number of people in the frame. If the number of detected people exceeds a specified threshold (`max_people`), an alarm sound is played to indicate overcrowding.

## Features

- Live video feed with real-time person detection using YOLOv8.
- Adjustable maximum number of people before the alarm triggers.
- Overcrowding alarm with a sound that repeats every 5 seconds.
- Web interface to change the `max_people` threshold and view the live feed.
- Option to stop the alarm via a separate route.

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/person-detection-alarm.git
    cd person-detection-alarm
    ```

2. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` should include:
    ```plaintext
    Flask
    opencv-python
    numpy
    ultralytics
    playsound
    ```

3. Download the YOLOv8 model and place it in the working directory:

    ```bash
    wget https://github.com/ultralytics/yolov5/releases/download/v8.0/yolov8n.pt
    ```

4. Run the application:

    ```bash
    python app.py
    ```

5. Open your web browser and go to `http://localhost:5000` to access the application.

## Usage

- Adjust the maximum people limit on the homepage and click 'Submit' to update.
- The live feed displays the number of detected people in real-time.
- If the person count exceeds the specified limit, an alarm sound plays.
- Use the `/stop_alarm` route to stop the alarm.


