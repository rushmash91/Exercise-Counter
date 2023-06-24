import cv2
import numpy as np
import PoseModule as pm_modified

video_capture = cv2.VideoCapture(0)
pose_detector = pm_modified.PoseDetectorModified()
counter = 0
correct_form = 0
exercise_feedback = "Fix Form"

while video_capture.isOpened():
    success, frame = video_capture.read()
    video_width = video_capture.get(3)
    video_height = video_capture.get(4)

    frame = pose_detector.findPose(frame, False)
    landmarks_list = pose_detector.findPosition(frame, False)

    if len(landmarks_list) != 0:
        hip_angle = pose_detector.findAngle(frame, 11, 23, 25, landmarks_list)
        knee_angle = pose_detector.findAngle(frame, 23, 25, 27, landmarks_list)

        progress_percentage = np.interp(knee_angle, (150, 90), (0, 100))
        progress_bar = np.interp(knee_angle, (150, 90), (380, 50))

        if hip_angle > 100 and knee_angle < 150:
            correct_form = 1

        if correct_form == 1:
            if progress_percentage == 0:
                if knee_angle >= 150 and hip_angle > 100:
                    exercise_feedback = "Up"
                    counter += 0.5
                else:
                    exercise_feedback = "Fix Form"

            if progress_percentage == 100:
                if knee_angle <= 90 and hip_angle > 100:
                    exercise_feedback = "Down"
                    counter += 0.5
                else:
                    exercise_feedback = "Fix Form"

        print(counter)

        if correct_form == 1:
            cv2.rectangle(frame, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(frame, (580, int(progress_bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{int(progress_percentage)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.rectangle(frame, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, str(int(counter)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        cv2.rectangle(frame, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, exercise_feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow('Deadlift Counter', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
