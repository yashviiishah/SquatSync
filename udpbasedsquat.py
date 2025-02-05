import cv2
import mediapipe as mp
import numpy as np
import socket
TF_ENABLE_ONEDNN_OPTS=0


# Calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# UDP socket setup
UDP_IP = "127.0.0.1"  # Localhost
UDP_PORT = 5005       # Port to send to
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Squat counter variables
counter = 0 
stage = None

# Setup MediaPipe Pose instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        # Process the image and get the pose results
        results = pose.process(image)
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract pose landmarks and calculate the squat angle
        try:
            landmarks = results.pose_landmarks.landmark
            # Get coordinates of landmarks for hip, knee, and ankle
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            # Calculate angle
            angle = calculate_angle(hip, knee, ankle)

            if angle > 160:
                stage = "up"
            if angle < 100 and stage == 'up':
                stage = "down"
                counter += 1
                print(counter)

                # Send the squat count and message to Unity client via UDP
                udp_socket.sendto(f"Data received, squat count: {counter}".encode('utf-8'), (UDP_IP, UDP_PORT))
                # Send the squat count and message to Unity client via UDP
                print(f"Sent squat count: {counter} to {UDP_IP}:{UDP_PORT}")  # Debugging print

                udp_socket.sendto(b'is_squat', (UDP_IP, UDP_PORT))
                print("Sent 'is_squat' signal")  # Debugging print

        except:
            pass

        # Render squat counter and stage on the image
        cv2.rectangle(image, (0,0), (225,90), (245,117,16), -1)
        cv2.putText(image, 'REPS', (15,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (15,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, 'STAGE', (130,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, (130,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        # Draw the landmarks and connections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

        # Display the image
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
udp_socket.close()
cv2.destroyAllWindows()
