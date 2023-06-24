import cv2
import mediapipe as mp
import math


class PoseDetectorModified:

    def __init__(self, mode=False, complexity=1, smooth_landmarks=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detectionCon=0.5, trackCon=0.5):
        """
        Initializes the PoseDetectorModified class with the required parameters.

        Args:
            mode (bool): Whether to run in static or video mode.
            complexity (int): The complexity of the model to be used for pose estimation.
            smooth_landmarks (bool): Whether to smooth the pose landmarks.
            enable_segmentation (bool): Whether to enable body segmentation.
            smooth_segmentation (bool): Whether to smooth the body segmentation.
            detectionCon (float): Detection confidence threshold.
            trackCon (float): Tracking confidence threshold.
        """
        self.mode = mode
        self.complexity = complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils  # The drawing utility of the MediaPipe library
        self.mpPose = mp.solutions.pose  # The pose estimation of the MediaPipe library
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth_landmarks,
                                     self.enable_segmentation, self.smooth_segmentation,
                                     self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True):
        """
        Finds the pose landmarks in an image or a video frame.

        Args:
            img (numpy.ndarray): The input image or video frame.
            draw (bool): Whether to draw the pose landmarks on the image or not.

        Returns:
            The input image or video frame with or without the drawn pose landmarks.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition(self, img, draw=True):
        """
        Finds the pose landmark positions in an image or a video frame.

        Args:
            img (numpy.ndarray): The input image or video frame.
            draw (bool): Whether to draw the pose landmark positions on the image or not.

        Returns:
            A list containing the landmark ID, X and Y positions for each landmark in the pose.
        """
        landmarks_list = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return landmarks_list

    def findAngle(self, img, p1, p2, p3, landmarks_list, draw=True):
        """
        Calculates the angle between three landmarks in an image or a video frame.

        Args:
            img (numpy.ndarray): The input image or video frame.
            p1 (int): The index of the first landmark.
            p2 (int): The index of the second landmark.
            p3 (int): The index of the third landmark.
            landmarks_list (list): The list of pose landmark positions in the frame.
            draw (bool): Whether to draw the angle and lines on the image or not.

        Returns:
            The angle between the three landmarks in degrees.
        """
        # Get the coordinates
        x1, y1 = landmarks_list[p1][1:]
        x2, y2 = landmarks_list[p2][1:]
        x3, y3 = landmarks_list[p3][1:]

        # Calculate the angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle


def main():
    detector = PoseDetectorModified()
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, img = cap.read()
        if ret:
            img = detector.findPose(img)
            cv2.imshow('Pose Detection', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

