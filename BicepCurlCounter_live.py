import cv2
import numpy as np
import PoseModule as pm_modified

video_capture = cv2.VideoCapture(0)
pose_detector = pm_modified.PoseDetectorModified()
counter = 0
movement_dir = 0
correct_form = 0
exercise_feedback = "Fix Form"

while video_capture.isOpened():
    success, frame = video_capture.read()
    video_width = video_capture.get(3)
    video_height = video_capture.get(4)

    #print(frame)
    frame = pose_detector.findPose(frame, False)
    landmarks_list = pose_detector.findPosition(frame, False)
    #print("length:{}".format(len(landmarks_list)))
    if len(landmarks_list) != 0:
        elbow_angle = pose_detector.findAngle(frame, 11, 13, 15, landmarks_list)
        shoulder_angle = pose_detector.findAngle(frame, 23, 11, 13, landmarks_list)

        progress_percentage = np.interp(elbow_angle, (50, 160), (0, 100))
        progress_bar = np.interp(elbow_angle, (50, 160), (380, 50))

        if elbow_angle < 150 and shoulder_angle > 150:
            correct_form = 1

        if correct_form == 1:
            print("Form is Correct")
            print("progress_percentage: {} , elbow_angle:{} , movement_dir: {}".format(progress_percentage,elbow_angle,movement_dir))
            if progress_percentage == 100:
                if elbow_angle >= 160:
                    print("Check")
                    exercise_feedback = "Up"
                    if movement_dir == 0:
                        counter += 0.5
                        movement_dir = 1
                else:
                    exercise_feedback = "Fix Form"

            if progress_percentage == 0:
                if elbow_angle < 50 and shoulder_angle > 150:
                    exercise_feedback = "Down"
                    if movement_dir == 1:
                        counter += 0.5
                        movement_dir = 0
                else:
                    exercise_feedback = "Fix Form"

        #print(counter)

        if correct_form == 1:
            cv2.rectangle(frame, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(frame, (580, int(progress_bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{int(progress_percentage)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.rectangle(frame, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, str(int(counter)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        cv2.rectangle(frame, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, exercise_feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow('Bicep Curls Counter', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
