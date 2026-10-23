# Human Activity Recognition and Fall Detection

## 1. Project Overview

This project uses Python, OpenCV, and MediaPipe Pose to analyse a live webcam feed, detect body landmarks, and estimate basic human postures. It is a prototype intended as a starting point for fall detection.

## 2. Objectives

- Capture live video using a webcam.
- Detect human body landmarks.
- Estimate standing, sitting, and possibly lying-down postures.
- Establish a foundation for future fall-detection development.

## 3. Technologies Used

- Python
- OpenCV
- MediaPipe Pose

## 4. Project Structure

```text
02_Human_Activity_Fall_Detection/
├── dataset/
├── results/
├── src/
│   └── main.py
├── README.md
└── requirements.txt
```

## 5. Installation

Install the dependencies using:

```bash
python -m pip install -r requirements.txt
```

## 6. How to Run

From the project root directory, run:

```bash
python src/main.py
```

The webcam window displays the detected body landmarks and estimated posture. Press **Q** to quit.

## 7. Current Features

- Live webcam input
- Human pose landmark detection
- Basic posture estimation
- On-screen activity labels
- Webcam frame retry handling

## 8. Limitations and Future Improvements

The current posture classifier is experimental. It may misclassify postures when the full body is not visible or when the camera angle changes. A lying-down posture is not sufficient to confirm a fall.

Future improvements include temporal fall detection, posture-transition analysis, dataset-based evaluation, and optional alerts.

This prototype is not intended for medical or emergency safety use.
