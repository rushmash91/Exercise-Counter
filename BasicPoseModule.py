import cv2
import mediapipe as mp


class PoseDetectorModified():

    def __init__(self, mode=False, complexity=1, smooth_landmarks=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detectionCon=0.5, trackCon=0.5):
        """
            Initializes a new instance of the PoseDetectorModified class.

            Args:
                mode (bool): Whether to use the upper-body-only pose landmark model or the full-body pose landmark model.
                complexity (int): Complexity of the pose landmark model (must be between 0 and 2).
                smooth_landmarks (bool): Whether to smooth the pose landmarks or not.
                enable_segmentation (bool): Whether to enable person segmentation or not.
                smooth_segmentation (bool): Whether to smooth the person segmentation or not.
                detectionCon (float): Minimum confidence value (between 0 and 1) for the detection to be considered successful.
                trackCon (float): Minimum confidence value (between 0 and 1) for the tracking to be considered successful.
        """

        self.mode = mode
        self.complexity = complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth_landmarks,
                                     self.enable_segmentation, self.smooth_segmentation,
                                     self.detectionCon, self.trackCon)

    def find_pose(self, img, draw=True):
        """
        Finds the pose landmarks and connections in an image or a video frame.

        Args:
            img (numpy.ndarray): The input image or video frame.
            draw (bool): Whether to draw the pose landmarks and connections on the image or not.

        Returns:
            The input image with the pose landmarks and connections drawn on it (if `draw` is True).
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)

        return img

    def find_position(self, img, draw=True):
        """
            Finds the pose landmark positions in an image or a video frame.

            Args:
                img (numpy.ndarray): The input image or video frame.
                draw (bool): Whether to draw the pose landmark positions on the image or not.

            Returns:
                A list containing the landmark ID, X and Y positions for each landmark in the pose.
        """
        lm_list = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lm_list


def main():
    detector = PoseDetectorModified()
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, img = cap.read()
        if ret:
            img = detector.find_pose(img)
            cv2.imshow('Pose Detection', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
