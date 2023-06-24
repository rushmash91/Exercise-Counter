import cv2  # Import the OpenCV library for computer vision tasks
import numpy as np  # Import the NumPy library for numerical operations
import PoseModule as pm_modified  # Import the custom PoseModule for pose estimation

video_capture = cv2.VideoCapture('./videos/pushups.mp4')  # Initialize video capture using the video file
frame_delay = int(1000 / video_capture.get(cv2.CAP_PROP_FPS))  # Calculate frame delay based on the video's frame rate
pose_detector = pm_modified.PoseDetectorModified()  # Create a pose detector object from the custom PoseModule
counter = 0  # Initialize the pushup counter to 0
movement_dir = 0  # Initialize the movement direction variable (0 for down, 1 for up)
correct_form = 0  # Initialize the correct form variable (0 for incorrect, 1 for correct)
exercise_feedback = "Fix Form"  # Initialize the exercise feedback message with "Fix Form"
#video_up_keypoints = [96.23996392481831,99.9061358608237,
#99.7472679832047,100.0,94.33463239592275,97.17810556811733,94.23820815651499,91.50191442704605,89.18551831095405,90.92741170936307,94.66137022270865,93.46785086219123,96.11721744886003]
while video_capture.isOpened():  # Loop while the video capture is open
    success, frame = video_capture.read()  # Read each frame from the video capture
    video_width = video_capture.get(3)  # Get the video width
    video_height = video_capture.get(4)  # Get the video height

    frame = pose_detector.findPose(frame, False)  # Find the pose in the frame without drawing landmarks
    landmarks_list = pose_detector.findPosition(frame, False)  # Get the list of landmarks without drawing them

    if len(landmarks_list) != 0:
        elbow_angle = pose_detector.findAngle(frame, 11, 13, 15, landmarks_list)  # Calculate elbow angle
        shoulder_angle = pose_detector.findAngle(frame, 13, 11, 23, landmarks_list)  # Calculate shoulder angle
        hip_angle = pose_detector.findAngle(frame, 11, 23, 25, landmarks_list)  # Calculate hip angle

        progress_percentage = np.interp(elbow_angle, (90, 150), (0, 100))  # Calculate progress percentage
        progress_bar = np.interp(elbow_angle, (90, 150), (380, 50))  # Calculate progress bar position

        if elbow_angle > 120 and shoulder_angle > 40 and hip_angle > 160:  # Check if the form is correct
            correct_form = 1

        if correct_form == 1:
            if progress_percentage == 0:  # Check if the pushup is at the top position
                #print(f'Elbow angle: {elbow_angle}, Shoulder angle: {shoulder_angle}, hip_angle:{hip_angle},Progress percentage: {progress_percentage}, Movement:{movement_dir}')
                if elbow_angle <= 90 and hip_angle > 160:
                    exercise_feedback = "Down"
                    if movement_dir == 0:
                        #print("Up")
                        counter += 0.5
                        movement_dir = 1
                    #print(counter)
                else:
                    exercise_feedback = "Fix Form"
            #print(progress_percentage)
            if progress_percentage == 100:  # Check if the pushup is at the bottom position
                #print(f'Elbow angle: {elbow_angle}, Shoulder angle: {shoulder_angle}, hip_angle:{hip_angle},Progress percentage: {progress_percentage}, Movement:{movement_dir}')
                if elbow_angle > 150 and shoulder_angle > 40 and hip_angle > 160:
                    exercise_feedback = "Up"
                    if movement_dir == 1:
                        #print("Down")
                        counter += 0.5
                        movement_dir = 0
                else:
                    exercise_feedback = "Fix Form"
          # Print the pushup counter

        if correct_form == 1: # Draw progress bar if the form is correct
            cv2.rectangle(frame, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(frame, (580, int(progress_bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{int(progress_percentage)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.rectangle(frame, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, str(int(counter)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        cv2.rectangle(frame, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, exercise_feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow('Pushup counter', frame)  # Show the frame with the pushup counter and feedback
    if cv2.waitKey(frame_delay) & 0xFF == ord('q'):  # Break the loop if 'q' is pressed
        break

video_capture.release()  # Release the video capture
cv2.destroyAllWindows()  # Close all OpenCV windows
