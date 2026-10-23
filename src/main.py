
import cv2
import time
import math
import mediapipe as mp


# ==========================================
# 1. CALCULATE ANGLE BETWEEN BODY LANDMARKS
# ==========================================

def calculate_angle(a, b, c):
    angle1 = math.atan2(a.y - b.y, a.x - b.x)
    angle2 = math.atan2(c.y - b.y, c.x - b.x)

    angle = abs(math.degrees(angle1 - angle2))

    if angle > 180:
        angle = 360 - angle

    return angle


# ==========================================
# 2. CLASSIFY BASIC HUMAN POSTURE
# ==========================================

def classify_activity(landmarks):
    mp_pose = mp.solutions.pose

    required_points = [
        mp_pose.PoseLandmark.LEFT_SHOULDER,
        mp_pose.PoseLandmark.RIGHT_SHOULDER,
        mp_pose.PoseLandmark.LEFT_HIP,
        mp_pose.PoseLandmark.RIGHT_HIP,
        mp_pose.PoseLandmark.LEFT_KNEE,
        mp_pose.PoseLandmark.RIGHT_KNEE,
        mp_pose.PoseLandmark.LEFT_ANKLE,
        mp_pose.PoseLandmark.RIGHT_ANKLE,
    ]

    points = [landmarks[p.value] for p in required_points]

    if any(point.visibility < 0.5 for point in points):
        return "Body Not Fully Visible"

    ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    lh = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    rh = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

    lk = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    rk = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
    la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

    shoulder_x = (ls.x + rs.x) / 2
    shoulder_y = (ls.y + rs.y) / 2
    hip_x = (lh.x + rh.x) / 2
    hip_y = (lh.y + rh.y) / 2

    # Approximate torso orientation.
    dx = shoulder_x - hip_x
    dy = shoulder_y - hip_y
    torso_angle = abs(math.degrees(math.atan2(dy, dx)))

    if torso_angle < 30 or torso_angle > 150:
        return "Possibly Lying Down"

    left_angle = calculate_angle(lh, lk, la)
    right_angle = calculate_angle(rh, rk, ra)
    average_knee_angle = (left_angle + right_angle) / 2

    if average_knee_angle < 125:
        return "Possibly Sitting"

    return "Possibly Standing"


# ==========================================
# 3. OPEN WEBCAM USING MSMF
# ==========================================

def open_camera():
    print("Opening webcam using Media Foundation...")

    camera = cv2.VideoCapture(0, cv2.CAP_MSMF)

    if not camera.isOpened():
        camera.release()
        print("ERROR: Could not open webcam.")
        return None

    # Allow the camera time to initialise.
    time.sleep(3)

    # Retry reading frames during startup.
    for attempt in range(20):
        success, frame = camera.read()

        if success and frame is not None:
            print("SUCCESS: Camera frame received using MSMF!")
            return camera

        print(f"Waiting for camera frame: {attempt + 1}/20")
        time.sleep(0.3)

    camera.release()
    print("ERROR: Could not receive camera frames.")
    return None


# ==========================================
# 4. MAIN ACTIVITY RECOGNITION PROGRAM
# ==========================================

def main():
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    camera = open_camera()

    if camera is None:
        print("Close other camera apps and try again.")
        return

    consecutive_failures = 0
    max_failures = 10

    try:
        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as pose:

            print("Activity recognition running. Press Q to quit.")

            while True:
                success, frame = camera.read()

                if not success or frame is None:
                    consecutive_failures += 1
                    print(
                        f"Camera frame lost: "
                        f"{consecutive_failures}/{max_failures}"
                    )

                    if consecutive_failures >= max_failures:
                        print("Camera repeatedly failed. Stopping.")
                        break

                    time.sleep(0.2)
                    continue

                consecutive_failures = 0

                # Mirror the webcam image.
                frame = cv2.flip(frame, 1)

                # Convert image from BGR to RGB.
                rgb_frame = cv2.cvtColor(
                    frame, cv2.COLOR_BGR2RGB
                )

                rgb_frame.flags.writeable = False
                results = pose.process(rgb_frame)

                activity = "No Person Detected"

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS
                    )

                    activity = classify_activity(
                        results.pose_landmarks.landmark
                    )

                # Draw activity label.
                cv2.rectangle(
                    frame,
                    (10, 10),
                    (frame.shape[1] - 10, 65),
                    (0, 0, 0),
                    -1
                )

                cv2.putText(
                    frame,
                    "Activity: " + activity,
                    (20, 45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA
                )

                cv2.imshow(
                    "Human Activity Recognition and Fall Detection",
                    frame
                )

                # Press Q to exit.
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        camera.release()
        cv2.destroyAllWindows()

    print("Program finished.")


if __name__ == "__main__":
    main()
