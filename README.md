# Exercise Counter with Pose Estimation

This project uses the power of computer vision to track and count various exercises in real-time. It is built using the mediapipe library for pose estimation and OpenCV for image processing.

## Features

- Real-time exercise check and counter for push-ups, squats, bicep curls and pull-ups.
- Visual feedback on the user's form (correct or needs fixing)
- Progress bar indicating the completion of each exercise
- Percentage display of exercise progress

## Installation

To set up the environment and install the required libraries, follow the steps below:

1. Clone the repository

2. Create a virtual environment (Optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

3. Install the required libraries:

```bash
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```bash
python name of the .py file of the excercise you want to check
```

The application will access your webcam and start detecting and counting exercises in real-time. The exercise counter will be displayed at the bottom-left corner of the screen, and the progress bar and percentage display will appear for each exercise. The specific exercise being counted can be changed in the code by selecting the corresponding exercise function in the main function.

## Method

This project is a real-time exercise counter using computer vision. It employs the mediapipe library for pose estimation and OpenCV for image processing.

The exercise counter has four Python files: pushupcounter.py, bicep_curl_counter.py, pullup_counter.py, and squatCounter.py. The main files capture the webcam feed, count exercises in real-time, and provide visual feedback on the user's form (correct or needs fixing). The PoseModule.py file is a custom module that extends the functionalities of the mediapipe library for these projects.

The algorithm used in these projects involves calculating the angles between different body landmarks to determine the user's form during an exercise. The angle calculations are based on the findAngle method in the PoseDetectorModified class of PoseModule.py. The method calculates the angle formed by three points, p1, p2, and p3, based on their landmark IDs.

The main logic of the exercise counters is in the pushupcounter.py, bicep_curl_counter.py, pullup_counter.py, and squat_counter.py files. They initialize a video capture object, a pose detector object, and variables to keep track of exercise counts and movement direction. The program reads frames from the webcam, processes the pose estimation, and extracts the landmark positions.

With the landmark positions, the program calculates the angle of various body parts, depending on the exercise type. It then checks if the user's form is correct based on these angles. The progress of each exercise is represented as a percentage and is used to determine whether the user is in the "Up" or "Down" position. The counter increases when the user moves from one position to the other. Moreover, the program provides real-time feedback on the user's form, indicating if it needs fixing.

The PoseModule.py file contains a class PoseDetectorModified that wraps the mediapipe library's functionalities, making it easier to use in the main exercise counter program. It provides methods like findPose, findPosition, and findAngle, which are crucial to the main algorithm.

In summary, these projects combine pose estimation using the mediapipe library and image processing using OpenCV to create real-time exercise counters that also provide feedback on the user's form. They achieve this by analyzing the angles between specific body landmarks and counting the exercises as the user moves between the "Up" and "Down" positions.
